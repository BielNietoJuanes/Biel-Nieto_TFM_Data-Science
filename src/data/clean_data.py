"""Limpia y normaliza la capa Bronce para generar la capa Plata."""
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
ORIGEN = RAIZ / "data" / "bronze" / "alquiler_municipios_original.csv"
DESTINO = RAIZ / "data" / "silver" / "alquiler_municipios_limpio.csv"
RENOMBRAR = {
    "Àmbit territorial": "ambito_territorial", "Codi territorial": "codigo_territorial",
    "Nom territori": "municipio", "Any": "anio", "Període": "periodo",
    "Habitatges": "contratos", "Renda": "renta_euros_mes", "Tram de preus": "tramo_precios",
}
OBLIGATORIAS = list(RENOMBRAR.values())


def convertir_numero(serie):
    """Convierte números con coma decimal y marcadores de confidencialidad en ausentes."""
    texto = (serie.astype("string").str.strip()
             .str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
             .replace({"": pd.NA, "..": pd.NA, "—": pd.NA, "-": pd.NA, "NaN": pd.NA}))
    return pd.to_numeric(texto, errors="coerce")


def main():
    if not ORIGEN.exists():
        raise FileNotFoundError(f"No existe {ORIGEN}. Ejecuta antes descargar_datos.py")
    datos = pd.read_csv(ORIGEN, sep=None, engine="python", dtype={"Codi territorial": "string"})
    datos.columns = [str(col).strip().replace("\ufeff", "") for col in datos.columns]
    datos = datos.rename(columns=RENOMBRAR)
    faltantes = [col for col in OBLIGATORIAS if col not in datos.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas esperadas: {faltantes}. Disponibles: {list(datos.columns)}")
    datos = datos[OBLIGATORIAS].copy()
    datos["codigo_territorial"] = datos["codigo_territorial"].astype("string").str.zfill(5).str.strip()
    for columna in ["municipio", "ambito_territorial", "periodo", "tramo_precios"]:
        datos[columna] = datos[columna].astype("string").str.strip()
    datos["anio"] = convertir_numero(datos["anio"]).astype("Int64")
    datos["contratos"] = convertir_numero(datos["contratos"]).astype("Int64")
    datos["renta_euros_mes"] = convertir_numero(datos["renta_euros_mes"])
    datos = datos[datos["ambito_territorial"].str.casefold().eq("municipi")].copy()
    datos = datos.drop_duplicates(subset=["codigo_territorial", "anio", "periodo"], keep="last")
    datos = datos.sort_values(["codigo_territorial", "anio", "periodo"])
    datos.loc[datos["contratos"] < 0, "contratos"] = pd.NA
    datos.loc[datos["renta_euros_mes"] <= 0, "renta_euros_mes"] = pd.NA
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    datos.to_csv(DESTINO, index=False, encoding="utf-8")
    print(f"Datos limpios guardados: {DESTINO}")
    print(f"Filas: {len(datos):,}")
    print(f"Rentas ausentes/anonimizadas: {datos['renta_euros_mes'].isna().sum():,}")
    print(f"Contratos ausentes: {datos['contratos'].isna().sum():,}")


if __name__ == "__main__":
    main()
