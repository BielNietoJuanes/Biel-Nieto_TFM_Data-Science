"""Construye la capa Oro a partir de los datos de la capa Plata."""
from pathlib import Path
import re
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
ORIGEN = RAIZ / "data" / "silver" / "alquiler_municipios_limpio.csv"
DESTINO = RAIZ / "data" / "gold" / "alquiler_municipios_dataset.csv"


def inicio_trimestre(anio, periodo):
    """Devuelve la fecha inicial del trimestre si el periodo se puede interpretar."""
    if pd.isna(anio) or pd.isna(periodo):
        return pd.NA
    coincidencia = re.search(r"(?:T|Q)([1-4])|([1-4])(?:T|Q)", str(periodo).strip().upper())
    if not coincidencia:
        return pd.NA
    trimestre = int(coincidencia.group(1) or coincidencia.group(2))
    mes = (trimestre - 1) * 3 + 1
    return f"{int(anio):04d}-{mes:02d}-01"


def main():
    if not ORIGEN.exists():
        raise FileNotFoundError(f"No existe {ORIGEN}. Ejecuta primero descarga y limpieza.")
    datos = pd.read_csv(ORIGEN, dtype={"codigo_territorial": "string"})
    datos["fecha_periodo"] = [inicio_trimestre(a, p) for a, p in zip(datos["anio"], datos["periodo"])]
    datos["fecha_periodo"] = pd.to_datetime(datos["fecha_periodo"], errors="coerce")
    datos["renta_euros_mes"] = pd.to_numeric(datos["renta_euros_mes"], errors="coerce")
    datos["contratos"] = pd.to_numeric(datos["contratos"], errors="coerce").astype("Int64")
    columnas = ["codigo_territorial", "municipio", "anio", "periodo", "fecha_periodo",
                "contratos", "renta_euros_mes", "tramo_precios"]
    oro = datos[columnas].sort_values(["codigo_territorial", "fecha_periodo"])
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    oro.to_csv(DESTINO, index=False, encoding="utf-8", date_format="%Y-%m-%d")
    print(f"Conjunto final guardado: {DESTINO}")
    print(f"Filas: {len(oro):,}")
    print(f"Municipios: {oro['codigo_territorial'].nunique():,}")
    print(f"Periodos interpretados: {oro['fecha_periodo'].notna().sum():,}/{len(oro):,}")
    print(f"Rentas disponibles: {oro['renta_euros_mes'].notna().sum():,}/{len(oro):,}")


if __name__ == "__main__":
    main()
