"""Entrena, compara y guarda modelos para estimar la renta mensual del alquiler."""
from pathlib import Path
import json
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

RAIZ = Path(__file__).resolve().parents[2]
ARCHIVO_DATOS = RAIZ / "data" / "gold" / "alquiler_municipios_dataset.csv"
CARPETA_MODELOS = RAIZ / "models"
CARPETA_REPORTS = RAIZ / "reports"
OBJETIVO = "renta_euros_mes"
CATEGORICAS = ["codigo_territorial"]
NUMERICAS = ["anio", "trimestre"]


def preparar_datos():
    """Carga el conjunto gold y deriva variables temporales."""
    if not ARCHIVO_DATOS.exists():
        raise FileNotFoundError(
            f"No se encuentra {ARCHIVO_DATOS}. Ejecuta primero el proceso de la Fase 1."
        )
    data = pd.read_csv(ARCHIVO_DATOS, dtype={"codigo_territorial": "string"})
    necesarias = {"codigo_territorial", "municipio", "fecha_periodo", OBJETIVO}
    faltantes = necesarias.difference(data.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas en el conjunto gold: {sorted(faltantes)}")
    data["fecha_periodo"] = pd.to_datetime(data["fecha_periodo"], errors="coerce")
    data[OBJETIVO] = pd.to_numeric(data[OBJETIVO], errors="coerce")
    data = data.dropna(subset=["codigo_territorial", "fecha_periodo", OBJETIVO]).copy()
    data = data[data[OBJETIVO] > 0].copy()
    if data.empty:
        raise ValueError(
            "No quedan registros con fecha y renta positiva. Revisa fecha_periodo "
            "y renta_euros_mes en data/gold."
        )
    data["anio"] = data["fecha_periodo"].dt.year.astype(int)
    data["trimestre"] = data["fecha_periodo"].dt.quarter.astype(int)
    return data.sort_values(["fecha_periodo", "codigo_territorial"]).reset_index(drop=True)


def separar_por_fecha(data, proporcion=0.8):
    """Usa los periodos antiguos para entrenar y los más recientes para probar."""
    periodos = np.array(sorted(data["fecha_periodo"].unique()))
    if len(periodos) < 4:
        raise ValueError(
            f"Solo hay {len(periodos)} periodos válidos. Se necesitan al menos 4. "
            "Comprueba la conversión de periodos de la Fase 1."
        )
    posicion = min(max(int(np.floor(len(periodos) * proporcion)), 1), len(periodos) - 1)
    fecha_corte = pd.Timestamp(periodos[posicion])
    entrenamiento = data[data["fecha_periodo"] < fecha_corte].copy()
    prueba = data[data["fecha_periodo"] >= fecha_corte].copy()
    if entrenamiento.empty or prueba.empty:
        raise ValueError("La separación temporal ha generado un conjunto vacío.")
    return entrenamiento, prueba, fecha_corte


def crear_preprocesador():
    """Codifica municipios y escala año y trimestre."""
    return ColumnTransformer(
        transformers=[
            ("municipio", OneHotEncoder(handle_unknown="ignore", sparse_output=False),
             CATEGORICAS),
            ("tiempo", Pipeline([
                ("imputar", SimpleImputer(strategy="median")),
                ("escalar", StandardScaler()),
            ]), NUMERICAS),
        ],
        remainder="drop",
    )


def metricas(nombre, reales, predichos):
    reales = np.asarray(reales, dtype=float)
    predichos = np.asarray(predichos, dtype=float)
    mape = np.mean(np.abs((reales - predichos) / reales)) * 100
    return {
        "modelo": nombre,
        "MAE_euros": mean_absolute_error(reales, predichos),
        "RMSE_euros": np.sqrt(mean_squared_error(reales, predichos)),
        "MAPE_porcentaje": mape,
        "observaciones_prueba": len(reales),
    }


def guardar_graficos(predicciones):
    CARPETA_REPORTS.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.scatter(predicciones["renta_real"], predicciones["renta_predicha"], alpha=0.4)
    minimo = min(predicciones["renta_real"].min(), predicciones["renta_predicha"].min())
    maximo = max(predicciones["renta_real"].max(), predicciones["renta_predicha"].max())
    plt.plot([minimo, maximo], [minimo, maximo], "--")
    plt.xlabel("Renta real (euros/mes)")
    plt.ylabel("Renta estimada (euros/mes)")
    plt.title("Renta real frente a renta estimada")
    plt.tight_layout()
    plt.savefig(CARPETA_REPORTS / "real_vs_predicho.png", dpi=150)
    plt.close()

    resumen = predicciones.groupby("fecha_periodo", as_index=False)[
        ["renta_real", "renta_predicha"]
    ].mean()
    plt.figure(figsize=(10, 5))
    plt.plot(resumen["fecha_periodo"], resumen["renta_real"], marker="o", label="Real")
    plt.plot(resumen["fecha_periodo"], resumen["renta_predicha"],
             marker="o", label="Estimación")
    plt.xlabel("Periodo")
    plt.ylabel("Renta media (euros/mes)")
    plt.title("Evolución de la renta en el conjunto de prueba")
    plt.legend()
    plt.xticks(rotation=35)
    plt.tight_layout()
    plt.savefig(CARPETA_REPORTS / "evolucion_test.png", dpi=150)
    plt.close()


def main():
    CARPETA_MODELOS.mkdir(parents=True, exist_ok=True)
    CARPETA_REPORTS.mkdir(parents=True, exist_ok=True)
    data = preparar_datos()
    entrenamiento, prueba, fecha_corte = separar_por_fecha(data)

    columnas = CATEGORICAS + NUMERICAS
    x_train, y_train = entrenamiento[columnas], entrenamiento[OBJETIVO]
    x_test, y_test = prueba[columnas], prueba[OBJETIVO]

    # Referencia sencilla: mediana histórica por municipio, con respaldo global.
    mediana_global = float(y_train.median())
    medianas = entrenamiento.groupby("codigo_territorial")[OBJETIVO].median()
    predicciones = {
        "Referencia_mediana_municipal":
            x_test["codigo_territorial"].map(medianas).fillna(mediana_global).to_numpy()
    }
    resultados = [metricas("Referencia_mediana_municipal", y_test,
                           predicciones["Referencia_mediana_municipal"])]
    models = {}

    candidatos = {
        "Ridge": Ridge(alpha=1.0),
        "HistGradientBoosting": HistGradientBoostingRegressor(
            max_iter=150, learning_rate=0.08, max_leaf_nodes=15,
            l2_regularization=1.0, random_state=42
        ),
    }
    for nombre, estimador in candidatos.items():
        modelo = Pipeline([
            ("preparacion", crear_preprocesador()),
            ("estimador", estimador),
        ])
        modelo.fit(x_train, y_train)
        pred = modelo.predict(x_test)
        models[nombre] = modelo
        predicciones[nombre] = pred
        resultados.append(metricas(nombre, y_test, pred))

    tabla = pd.DataFrame(resultados).sort_values("MAE_euros")
    tabla.to_csv(CARPETA_REPORTS / "metricas_modelos.csv", index=False, encoding="utf-8")

    # La referencia no se puede cargar como un estimador estándar en el MVP.
    # Si gana la referencia, se conserva el mejor estimador ML entrenado.
    ganador = tabla.iloc[0]["modelo"]
    modelo_guardado = ganador if ganador in models else (
        tabla[tabla["modelo"].isin(models)].iloc[0]["modelo"]
    )
    joblib.dump(models[modelo_guardado], CARPETA_MODELOS / "modelo_alquiler.joblib")

    salida = prueba[["codigo_territorial", "municipio", "fecha_periodo", OBJETIVO]].copy()
    salida = salida.rename(columns={OBJETIVO: "renta_real"})
    salida["renta_predicha"] = predicciones[modelo_guardado]
    salida["modelo"] = modelo_guardado
    salida.to_csv(CARPETA_REPORTS / "predicciones_test.csv", index=False, encoding="utf-8")
    guardar_graficos(salida)

    metadatos = {
        "modelo_guardado": modelo_guardado,
        "modelo_con_menor_mae_incluida_referencia": ganador,
        "fecha_corte": fecha_corte.strftime("%Y-%m-%d"),
        "variable_objetivo": OBJETIVO,
        "variables_categoricas": CATEGORICAS,
        "variables_numericas": NUMERICAS,
        "filas_entrenamiento": int(len(entrenamiento)),
        "filas_prueba": int(len(prueba)),
        "periodos_totales": int(data["fecha_periodo"].nunique()),
        "nota": "Si gana la referencia, se guarda el mejor modelo ML para poder cargarlo como estimador en el MVP. La comparación completa está en reports/metricas_modelos.csv."
    }
    (CARPETA_MODELOS / "metadatos_modelo.json").write_text(
        json.dumps(metadatos, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\\nComparación de modelos:")
    print(tabla.to_string(index=False))
    print(f"\\nFecha de corte temporal: {fecha_corte.date()}")
    print(f"Modelo guardado para el MVP: {modelo_guardado}")


if __name__ == "__main__":
    main()
