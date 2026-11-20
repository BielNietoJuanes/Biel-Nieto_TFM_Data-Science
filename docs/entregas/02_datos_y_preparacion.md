# Entrega 02 — Datos y preparación

**Proyecto:** Observatorio de la asequibilidad del alquiler en Cataluña  
**Fase:** 1 — Preparación de datos  
**Estado:** código preparado; pendiente de ejecución y comprobación de resultados en el repositorio local.

## 1. Objetivo
Obtener una base municipal y temporal del mercado del alquiler en Cataluña, conservar el archivo original, normalizar variables y generar un conjunto analítico reproducible para la exploración y el modelado posterior.

## 2. Fuente de datos
- **Nombre:** Precio medio del alquiler de viviendas por municipio.
- **Productor:** Generalitat de Cataluña; estadística basada en el registro de fianzas de INCASÒL.
- **Portal:** Datos Abiertos de Cataluña.
- **Identificador:** `qww9-bvhh`.
- **Ficha:** https://analisi.transparenciacatalunya.cat/Habitatge/Preu-mitj-del-lloguer-d-habitatges-per-municipi/qww9-bvhh
- **Descarga CSV:** https://analisi.transparenciacatalunya.cat/api/v3/views/qww9-bvhh/export.csv?accessType=DOWNLOAD
- **Periodicidad:** trimestral.
- **Cobertura:** municipios de Cataluña.
- **Variables:** ámbito territorial, código territorial, nombre del territorio, año, periodo, contratos, renta media mensual y tramo de precios.

La estadística se basa en contratos con fianza depositada en INCASÒL. La renta puede aparecer anonimizada en municipios o periodos con menos de seis contratos. Se trata como dato ausente, nunca como cero.

## 3. Arquitectura del proceso
```text
Fuente CSV oficial
      ↓
datos/bronce/alquiler_municipios_original.csv
      ↓ descargar_datos.py
datos/plata/alquiler_municipios_limpio.csv
      ↓ limpiar_datos.py
datos/oro/alquiler_municipios_dataset.csv
      ↑ crear_dataset.py
```

### Bronce
Copia de la descarga original, sin transformaciones, para mantener la trazabilidad.

### Plata
- Renombrado de columnas a nombres consistentes en español.
- Código municipal conservado como texto de cinco dígitos.
- Conversión de año, contratos y renta a tipos numéricos.
- Marcadores de confidencialidad/no disponibilidad tratados como ausentes.
- Filtro del ámbito municipal.
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

`fecha_periodo` se calcula si el formato permite identificar el trimestre; de lo contrario queda vacío y habrá que revisar el formato de origen.

## 4. Ejecución
Con el entorno virtual activado y las dependencias instaladas:
```bash
python src/datos/descargar_datos.py
python src/datos/limpiar_datos.py
python src/datos/crear_dataset.py
```

## 5. Validaciones y limitaciones
- Confirmar que las columnas de origen siguen siendo las esperadas.
- Comprobar filas y municipios en Plata y Oro.
- Revisar el porcentaje de rentas ausentes o anonimizadas.
- Verificar que los códigos territoriales conservan los ceros iniciales.
- Revisar periodos que no se han convertido en `fecha_periodo`.
- La renta media corresponde a contratos con fianza registrada; no representa necesariamente todos los alquileres ni los precios de anuncios.
- No interpretar rentas anonimizadas como cero ni imputarlas sin justificación metodológica.

## 6. Resultados tras la ejecución
| Indicador | Resultado |
|---|---|
| Filas Bronce | Pendiente de ejecución |
| Filas Plata | Pendiente de ejecución |
| Filas Oro | Pendiente de ejecución |
| Municipios distintos | Pendiente de ejecución |
| Rentas ausentes/anonimizadas | Pendiente de ejecución |
| Periodos no interpretados | Pendiente de ejecución |

## 7. Reproducibilidad
Los scripts están en `src/datos/`. La fuente se identifica con `qww9-bvhh`. Anota la fecha de descarga en la revisión final, porque el portal actualiza los datos trimestralmente.
