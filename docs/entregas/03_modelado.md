# Entrega 03 — Modelado y aprendizaje automático

**Proyecto:** Observatorio de la asequibilidad del alquiler en Cataluña  
**Fase:** 2 — Modelado  
**Estado:** ejecutado y validado con el conjunto Oro disponible en el repositorio local.

## 1. Objetivo

Entrenar y comparar modelos para estimar la renta mensual del alquiler por municipio y periodo, usando una separación temporal que reserve los periodos más recientes para evaluación.

## 2. Datos utilizados

El modelado parte de `data/gold/alquiler_municipios_dataset.csv`, generado a partir de la estadística municipal de alquiler descrita en la [Entrega 02](./02_datos_y_preparacion.md).

La preparación considera únicamente filas con fecha interpretable y renta mensual positiva. Las rentas anonimizadas o ausentes se mantienen como ausentes y no se usan como objetivo de entrenamiento. Para interpretar las fechas, el proceso de datos reconoce los periodos catalanes publicados —por ejemplo, `gener-març`, `abril-juny` y `gener-desembre`— y los asigna al inicio del trimestre correspondiente.

## 3. Variables y modelos

- **Variable objetivo:** `renta_euros_mes`.
- **Variables de entrada:** código territorial del municipio, año y trimestre.
- **Modelos comparados:**
  - **Ridge**, con `alpha=1.0`.
  - **HistGradientBoosting**, con los parámetros fijados en el script de entrenamiento.
  - **Referencia por municipio:** mediana histórica de la renta municipal, con la mediana global como respaldo.

El código de entrenamiento y evaluación se centraliza en `src/models/train_models.py`. El notebook [03_modelado.ipynb](../../notebooks/03_modelado.ipynb) permite inspeccionar los datos y ejecutar el mismo proceso sin duplicar la lógica.

## 4. Evaluación

La partición es temporal: se ordenan los periodos, se usan aproximadamente los primeros cuatro quintos para entrenamiento y se reservan los más recientes para prueba.

| Indicador | Resultado |
|---|---:|
| Filas del conjunto Oro | 47.541 |
| Municipios | 945 |
| Fechas interpretables | 47.541 |
| Rentas positivas | 26.594 |
| Rentas ausentes | 20.947 |
| Periodos usados por el modelo | 42 |
| Filas de entrenamiento | 20.475 |
| Filas de prueba | 6.119 |
| Fecha de corte | 2024-04-01 |

### Métricas en el conjunto de prueba

| Modelo | MAE (euros) | RMSE (euros) | MAPE (%) |
|---|---:|---:|---:|
| Ridge | **75,32** | **108,38** | **10,13** |
| HistGradientBoosting | 111,94 | 147,24 | 16,48 |
| Referencia por municipio | 123,53 | 149,76 | 17,74 |

Ridge obtiene el menor MAE entre los modelos evaluados y se guarda como modelo para el MVP. Estas métricas corresponden a la versión local del conjunto de datos y pueden variar si se descarga una versión actualizada.

## 5. Artefactos generados

- `models/modelo_alquiler.joblib`: pipeline Ridge entrenado.
- `models/metadatos_modelo.json`: modelo seleccionado, variables, fecha de corte y tamaños de los conjuntos.
- `reports/metricas_modelos.csv`: comparación completa de métricas.
- `reports/predicciones_test.csv`: valores reales y predichos para el conjunto de prueba.
- `reports/real_vs_predicho.png` y `reports/evolucion_test.png`: gráficos de evaluación.

## 6. Reproducibilidad

Desde la raíz del proyecto y con las dependencias instaladas, ejecutar:

```powershell
.\.venv\Scripts\python.exe src\data\download_data.py
.\.venv\Scripts\python.exe src\data\clean_data.py
.\.venv\Scripts\python.exe src\data\build_dataset.py
.\.venv\Scripts\python.exe src\models\train_models.py
```

También se puede inspeccionar y ejecutar el entrenamiento desde `notebooks/03_modelado.ipynb`. La evaluación usa una partición temporal; no sustituye una validación con datos futuros ni demuestra por sí sola que el modelo generalice igual a todos los municipios.
