# Entrega 02 — Datos y preparación

**Proyecto:** Observatorio de la asequibilidad del alquiler en Cataluña  
**Fase:** 1 — Preparación de datos  
**Estado:** pipeline implementado, ejecutado y validado con los datos disponibles localmente.

## 1. Objetivo
Obtener una base municipal y temporal del mercado del alquiler en Cataluña, conservar el archivo original, normalizar variables y generar un conjunto analítico reproducible para la exploración y el modelado posterior.

## 2. Fuente de datos
- **Nombre:** Precio medio del alquiler de viviendas por municipio.
- **Productor:** Generalitat de Cataluña; estadística basada en el registro de fianzas de INCASÒL.
- **Portal:** Datos Abiertos de Cataluña.
- **Identificador:** `qww9-bvhh`.
- **Ficha:** https://analisi.transparenciacatalunya.cat/Habitatge/Preu-mitj-del-lloguer-d-habitatges-per-municipi/qww9-bvhh
- **Descarga CSV:** https://analisi.transparenciacatalunya.cat/api/v3/views/qww9-bvhh/export.csv?accessType=DOWNLOAD
- **Periodicidad:** anual en los primeros años disponibles y con periodos trimestrales y acumulados en los años recientes.
- **Cobertura:** municipios de Cataluña.
- **Variables:** ámbito territorial, código territorial, nombre del territorio, año, periodo, contratos, renta media mensual y tramo de precios.

La estadística se basa en contratos con fianza depositada en INCASÒL. La renta puede aparecer anonimizada en municipios o periodos con menos de seis contratos. Se trata como dato ausente, nunca como cero.

## 3. Arquitectura del proceso
```text
Fuente CSV oficial
      ↓
src/data/download_data.py
      ↓
data/bronze/alquiler_municipios_original.csv
      ↓ src/data/clean_data.py
data/silver/alquiler_municipios_limpio.csv
      ↓ src/data/build_dataset.py
data/gold/alquiler_municipios_dataset.csv
```

### Bronce
Copia de la descarga original, sin transformaciones, para mantener la trazabilidad.

### Plata
- Renombrado de columnas a nombres consistentes en español.
- Código municipal conservado como texto de cinco dígitos.
- Conversión de año, contratos y renta a tipos numéricos.
- Marcadores de confidencialidad/no disponibilidad tratados como ausentes.
- Filtro del ámbito territorial `Municipi`.
- Eliminación de duplicados por código municipal, año y periodo.
- Rentas no positivas invalidadas.

### Oro
| Variable | Descripción |
|---|---|
| `codigo_territorial` | Código INE municipal, texto de 5 dígitos |
| `municipio` | Nombre del municipio |
| `anio` | Año de referencia |
| `periodo` | Periodo original publicado |
| `fecha_periodo` | Inicio de trimestre inferido |
| `contratos` | Número de contratos registrados |
| `renta_euros_mes` | Renta media mensual en euros |
| `tramo_precios` | Tramo de precios publicado |

`fecha_periodo` se calcula interpretando las etiquetas catalanas publicadas —como `gener-març`, `abril-juny` y `gener-desembre`— y se asigna al inicio del trimestre correspondiente. En la ejecución documentada se interpretaron todas las fechas.

## 4. Ejecución
Desde PowerShell, en la raíz del proyecto y con las dependencias instaladas:
```powershell
.\.venv\Scripts\python.exe src\data\download_data.py
.\.venv\Scripts\python.exe src\data\clean_data.py
.\.venv\Scripts\python.exe src\data\build_dataset.py
```

## 5. Validaciones y limitaciones
- Confirmar que las columnas de origen siguen siendo las esperadas.
- Comprobar filas y municipios en Plata y Oro.
- Revisar el porcentaje de rentas ausentes o anonimizadas.
- Verificar que los códigos territoriales conservan los ceros iniciales.
- Confirmar que todos los periodos esperados se han convertido en `fecha_periodo`.
- La renta media corresponde a contratos con fianza registrada; no representa necesariamente todos los alquileres ni los precios de anuncios.
- No interpretar rentas anonimizadas como cero ni imputarlas sin justificación metodológica.

## 6. Resultados tras la ejecución
| Indicador | Resultado |
|---|---|
| Filas Bronce | 47.541 |
| Filas Plata | 47.541 |
| Filas Oro | 47.541 |
| Municipios distintos | 945 |
| Rentas ausentes/anonimizadas | 20.947 |
| Periodos no interpretados | 0 |

## 7. Reproducibilidad
Los scripts están en `src/data/`. La fuente se identifica con `qww9-bvhh`. Los datos de `data/` están excluidos del control de versiones; descarga de nuevo la fuente para reproducir las capas. Anota la fecha de descarga en la revisión final, porque el portal actualiza los datos.
