# Observatorio de la asequibilidad del alquiler en Cataluña

Proyecto del Trabajo Final de Máster para explorar la evolución de la renta media del alquiler por municipio en Cataluña y preparar un modelo predictivo reproducible.

## Estado del proyecto

| Fase | Contenido | Estado |
|---|---|---|
| Propuesta | Comparación de tres ideas de producto y selección del observatorio del alquiler | Completada — [Entrega 01](docs/entregas/01_ideas_producto.md) |
| Preparación de datos | Descarga, limpieza y construcción de las capas Bronze, Silver y Gold | Implementada y ejecutada — [Entrega 02](docs/entregas/02_datos_y_preparacion.md) |
| Modelado | Comparación de modelos con partición temporal y guardado del modelo seleccionado | Implementada y ejecutada — [Entrega 03](docs/entregas/03_modelado.md) |
| Aplicación | Cuadro de mando para explorar los resultados | Pendiente |

El proyecto está actualmente en la fase de modelado. El prototipo de aplicación todavía no está implementado.

## Fuente y alcance de los datos

Se utiliza el conjunto oficial [Precio medio del alquiler de viviendas por municipio](https://analisi.transparenciacatalunya.cat/Habitatge/Preu-mitj-del-lloguer-d-habitatges-per-municipi/qww9-bvhh), basado en los contratos con fianza depositada en INCASÒL.

Los datos son agregados por municipio y periodo; no representan los precios de anuncios ni necesariamente todos los alquileres del mercado. Algunas rentas no se publican por motivos de confidencialidad. Se conservan como valores ausentes, nunca como cero.

## Proceso de datos y modelado

```text
Fuente oficial
    ↓ src/data/download_data.py
data/bronze/alquiler_municipios_original.csv
    ↓ src/data/clean_data.py
data/silver/alquiler_municipios_limpio.csv
    ↓ src/data/build_dataset.py
data/gold/alquiler_municipios_dataset.csv
    ↓ src/models/train_models.py
models/ y reports/
```

- **Bronze:** conserva la descarga original.
- **Silver:** normaliza los nombres y tipos de las columnas, conserva el código municipal como texto y trata marcadores de confidencialidad como ausentes. Se filtran los registros cuyo ámbito es `Municipi`.
- **Gold:** genera `fecha_periodo` a partir de los periodos publicados, incluyendo etiquetas como `gener-març`, `abril-juny` y `gener-desembre`.
- **Modelado:** utiliza `renta_euros_mes` como objetivo y el municipio, año y trimestre como variables de entrada. Compara Ridge, HistGradientBoosting y una referencia basada en la mediana histórica municipal. La evaluación reserva los periodos más recientes para prueba.

Los datos de `data/` y los modelos de `models/` se generan localmente y están excluidos del control de versiones por `.gitignore`. Hay que ejecutar el proceso de datos para reconstruirlos.

## Resultados de la última ejecución

Resultados calculados sobre los archivos disponibles localmente; pueden cambiar al descargar una actualización de la fuente.

| Indicador | Resultado |
|---|---:|
| Filas en Bronze, Silver y Gold | 47.541 |
| Municipios | 945 |
| Fechas interpretables en Gold | 47.541 |
| Rentas positivas | 26.594 |
| Rentas ausentes | 20.947 |
| Periodos usados por el modelo | 42 |
| Filas de entrenamiento / prueba | 20.475 / 6.119 |
| Fecha de corte temporal | 2024-04-01 |

### Métricas en el conjunto de prueba

| Modelo | MAE (euros) | RMSE (euros) | MAPE (%) |
|---|---:|---:|---:|
| Ridge | **75,32** | **108,38** | **10,13** |
| HistGradientBoosting | 111,94 | 147,24 | 16,48 |
| Referencia por municipio | 123,53 | 149,76 | 17,74 |

Ridge obtuvo el menor MAE en esta partición y se guardó como modelo para el MVP. La evaluación temporal no garantiza el mismo rendimiento en datos futuros ni en todos los municipios.

## Requisitos

- Python 3.14; el entorno local se validó con Python 3.14.3.
- Dependencias de [`requirements.txt`](requirements.txt).
- Para ejecutar los notebooks, Jupyter está incluido en las dependencias.

### Preparar el entorno en Windows

Desde PowerShell, en la raíz del proyecto:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si `py` no está disponible, crea el entorno desde VS Code con **Python: Create Environment** y selecciona el intérprete instalado. Después, puedes seguir utilizando `.\.venv\Scripts\python.exe` en los comandos siguientes, incluso si el comando global `python` no se reconoce.

## Ejecución completa

Descarga y procesa los datos, y después entrena los modelos:

```powershell
.\.venv\Scripts\python.exe src\data\download_data.py
.\.venv\Scripts\python.exe src\data\clean_data.py
.\.venv\Scripts\python.exe src\data\build_dataset.py
.\.venv\Scripts\python.exe src\models\train_models.py
```

Si ya existe una capa Gold actualizada, se puede ejecutar solo el entrenamiento:

```powershell
.\.venv\Scripts\python.exe src\models\train_models.py
```

También se puede abrir [`notebooks/03_modelado.ipynb`](notebooks/03_modelado.ipynb), seleccionar el entorno `.venv` como kernel y ejecutar sus celdas. El notebook reutiliza el mismo script de entrenamiento.

## Artefactos del entrenamiento

- `models/modelo_alquiler.joblib`: pipeline Ridge para su carga en la futura aplicación.
- `models/metadatos_modelo.json`: resumen del modelo y de la partición temporal.
- `reports/metricas_modelos.csv`: métricas comparativas.
- `reports/predicciones_test.csv`: predicciones sobre el conjunto de prueba.
- `reports/real_vs_predicho.png` y `reports/evolucion_test.png`: gráficos de evaluación.

## Estructura principal

```text
app/                         futura aplicación; pendiente de implementar
data/bronze/                 descarga original
data/silver/                 datos normalizados
data/gold/                   conjunto listo para análisis y modelado
docs/entregas/               documentación de las fases
models/                      modelos y metadatos generados
notebooks/03_modelado.ipynb  inspección de datos y ejecución del entrenamiento
reports/                     métricas, predicciones y gráficos
src/data/                    descarga, limpieza y construcción del dataset
src/models/                  entrenamiento y evaluación
tests/                       reservado para pruebas automatizadas
```
