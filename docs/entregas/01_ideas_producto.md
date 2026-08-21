# Entrega 1 - Propuesta inicial de ideas de producto

## Criterio de selección

Las tres propuestas se han elegido por su relevancia en Cataluña y por su viabilidad para un Trabajo Final de Máster de alcance controlado. Todas pueden desarrollarse con datos abiertos, sin necesitar datos personales ni acuerdos con organizaciones, y permiten combinar análisis exploratorio, visualización y modelos predictivos sencillos.

No se pretende resolver por completo problemas estructurales como la crisis de vivienda, la sequía o la siniestralidad vial. El objetivo es crear un producto de datos que ayude a identificar prioridades y respalde decisiones concretas.

---

## Idea 1 - Observatorio de asequibilidad del alquiler en Cataluña

### Problema que resuelve

El acceso a una vivienda de alquiler se ha convertido en una dificultad relevante para muchas personas en Cataluña. El precio medio del alquiler varía de forma importante entre municipios y evoluciona con el tiempo, lo que dificulta que la ciudadanía, las entidades sociales y las administraciones puedan identificar con claridad dónde existe una mayor presión residencial.

El problema no consiste únicamente en conocer el precio medio de un municipio. Es necesario detectar los lugares en los que los precios crecen con más intensidad, compararlos con la renta disponible o con otros indicadores socioeconómicos y observar si existe una brecha territorial de asequibilidad. Esta información puede ayudar a priorizar políticas de vivienda, orientación social o análisis posteriores más detallados.

La solución propuesta es un observatorio interactivo que permita consultar la evolución del alquiler por municipio o comarca, comparar territorios y generar un indicador simple de presión residencial. Como extensión, se puede estimar el precio medio del siguiente trimestre mediante modelos de series temporales sencillos.

### Motivación para realizar el proyecto

La vivienda es una problemática social, económica y generacional de gran relevancia en Cataluña. Un producto transparente y fácil de consultar puede convertir datos dispersos en información útil para comprender las diferencias entre territorios.

El proyecto permite aplicar contenidos del máster como limpieza de datos, análisis exploratorio, creación de indicadores, visualización geográfica y predicción básica de series temporales. La disponibilidad de estadísticas oficiales de alquiler facilita un desarrollo reproducible y realista sin tratar datos personales.

### A quién impacta

- Personas que buscan vivienda de alquiler y quieren comparar zonas.
- Ayuntamientos y consejos comarcales que necesitan identificar áreas con mayor presión residencial.
- Entidades sociales y periodistas que analizan desigualdades territoriales.
- Investigadores o responsables de políticas públicas de vivienda.

### Por qué tiene valor

- Facilita una lectura clara de la evolución y las diferencias territoriales de los alquileres.
- Ayuda a priorizar territorios para análisis, medidas de acompañamiento o políticas de vivienda.
- Mejora la transparencia al hacer accesibles datos oficiales mediante un cuadro de mando comprensible.
- Permite entrenar un modelo predictivo modesto y explicable, sin presentar sus resultados como una estimación individual de alquileres.

### Alcance inicial viable

El producto se limitaría a datos agregados de alquiler por municipio o comarca y a un periodo temporal definido. La primera versión incluiría un mapa, gráficos de evolución, un ranking de presión residencial y una predicción a corto plazo para territorios con suficiente historial. No analizaría anuncios individuales ni decidiría la elegibilidad de personas para ayudas.

### Posibles datos

- Estadística de contratos y precio medio de alquiler de Incasòl e Idescat.
- Datos territoriales de municipios y comarcas de la Generalitat.
- Indicadores socioeconómicos públicos, si se incorporan en una fase posterior.

---

## Idea 2 - Monitor de consumo de agua y detección de anomalías municipales

### Problema que resuelve

La gestión eficiente del agua es esencial en Cataluña, especialmente tras periodos recientes de sequía. Los municipios y las entidades suministradoras deben vigilar los consumos para detectar aumentos inesperados, planificar medidas de ahorro y comunicar mejor la situación a la población.

El consumo puede variar por estacionalidad, temperatura, población estacional, actividad económica o incidencias en la red. Revisar manualmente tablas mensuales dificulta identificar qué cambios son normales y cuáles merecen atención. El problema, por tanto, es apoyar el seguimiento de los consumos con una herramienta que muestre tendencias y avise de desviaciones relevantes.

La propuesta consiste en un cuadro de mando para explorar el consumo por municipio y periodo, compararlo con referencias históricas y marcar posibles anomalías. De forma opcional, se podría predecir el consumo del mes siguiente a partir del historial y variables meteorológicas públicas.

### Motivación para realizar el proyecto

El agua es un recurso limitado cuyo uso eficiente tiene impacto ambiental, social y económico. Un proyecto centrado en seguimiento y prevención es útil sin necesitar gestionar directamente una red de abastecimiento.

Desde el punto de vista técnico, permite trabajar series temporales, calidad de datos, tratamiento de valores ausentes, detección de anomalías, visualización y análisis geoespacial. La Agencia Catalana del Agua publica datos y herramientas de consulta que hacen posible un prototipo con información real.

### A quién impacta

- Personal técnico de ayuntamientos y entidades suministradoras.
- Responsables municipales de sostenibilidad y emergencias.
- Ciudadanía, al disponer de información más comprensible sobre el uso del agua en su municipio.
- Organizaciones ambientales interesadas en el seguimiento del recurso hídrico.

### Por qué tiene valor

- Reduce el tiempo necesario para revisar consumos y comparar municipios.
- Ayuda a priorizar la revisión de incrementos atípicos que podrían requerir una comprobación técnica.
- Favorece una planificación más informada de campañas de ahorro y medidas preventivas.
- Ofrece visualizaciones transparentes sin atribuir automáticamente una anomalía a una fuga o a un incumplimiento.

### Alcance inicial viable

La primera versión se centrará en una selección de municipios con series suficientemente completas. Incluirá evolución temporal, comparación por habitante cuando esté disponible, detección estadística de valores atípicos y una predicción de corto plazo. Se documentará que los datos reportados pueden contener valores parciales o revisiones; el producto es una herramienta de apoyo y no un sistema de diagnóstico de fugas.

### Posibles datos

- Datos de dotación y consumo municipal publicados por la Agencia Catalana del Agua.
- Reservas de embalses, precipitación y otras variables hidrológicas públicas de la ACA.
- Datos meteorológicos abiertos, si son necesarios para mejorar el análisis.

---

## Idea 3 - Mapa de riesgo de accidentes de tráfico para usuarios vulnerables

### Problema que resuelve

Los accidentes de tráfico con víctimas continúan afectando a conductores, peatones, ciclistas y, de forma especial, a motoristas. La peligrosidad no es homogénea: puede concentrarse en determinados tramos, municipios, franjas horarias, tipos de vía o condiciones temporales.

Sin una visualización y análisis territorial adecuados, resulta más difícil identificar dónde se concentran los accidentes graves y qué patrones son recurrentes. El problema no es predecir con certeza un accidente individual, sino facilitar que los responsables de movilidad prioricen puntos y situaciones que requieren análisis o medidas preventivas.

La solución será un mapa interactivo y un modelo de clasificación o puntuación de riesgo que analice accidentes históricos con víctimas graves o mortales. Permitirá filtrar por territorio, tipo de usuario, día de la semana, franja horaria y características de la vía, además de señalar zonas con alta concentración de siniestros.

### Motivación para realizar el proyecto

La seguridad vial tiene un impacto directo sobre la salud y la calidad de vida. Un análisis basado en datos puede ayudar a orientar intervenciones, campañas de prevención y revisiones de infraestructuras de una forma más objetiva.

Es una propuesta técnica viable porque existen datos abiertos históricos sobre accidentes graves y mortales en Cataluña. Permite aplicar geolocalización, análisis exploratorio, ingeniería de variables, evaluación de modelos y visualización en mapas. Además, se puede completar con una primera versión puramente descriptiva si el modelo predictivo no aporta una mejora suficiente.

### A quién impacta

- Servei Català de Trànsit y policías locales.
- Ayuntamientos y responsables de movilidad urbana.
- Asociaciones de motoristas, ciclistas y peatones.
- Ciudadanía que utiliza la red viaria catalana.

### Por qué tiene valor

- Hace visibles concentraciones y patrones de accidentalidad que no se aprecian en tablas.
- Ayuda a priorizar auditorías de seguridad, señalización, campañas o intervenciones urbanas.
- Permite analizar de forma específica a los usuarios vulnerables en lugar de tratar todos los accidentes como un único grupo.
- Ofrece un resultado visual y comprensible para usuarios no técnicos.

### Alcance inicial viable

La primera versión se limitará a accidentes con víctimas graves o mortales registrados en Cataluña desde un año de inicio definido. Se construirán un mapa de puntos o zonas de concentración, filtros temporales y un análisis descriptivo de factores asociados. Si la calidad y las variables lo permiten, se añadirá una puntuación de riesgo por tramo o zona, evitando usar el resultado para sancionar conductores o tomar decisiones automatizadas sobre personas.

### Posibles datos

- Datos abiertos del Servei Català de Trànsit sobre accidentes con personas muertas o heridas graves.
- Datos de exposición al riesgo de la red viaria catalana.
- Cartografía de carreteras y límites administrativos abiertos.

---

## Comparativa y siguiente paso recomendado

| Idea | Datos abiertos | Complejidad técnica | Riesgo de privacidad | Producto final posible |
| --- | --- | --- | --- | --- |
| Observatorio de alquiler | Alta | Baja-media | Bajo | Cuadro de mando territorial y previsión básica |
| Monitor de consumo de agua | Alta, con posibles datos incompletos | Media | Bajo | Panel de seguimiento y detección de anomalías |
| Mapa de riesgo vial | Alta | Media | Bajo | Mapa interactivo y análisis de zonas de riesgo |

Las tres son candidatas adecuadas para continuar en la siguiente entrega. La recomendación inicial es priorizar el **Observatorio de asequibilidad del alquiler**: tiene el alcance más fácil de acotar, datos agregados comprensibles y permite aportar valor con un análisis y una visualización sólidos incluso sin un modelo predictivo complejo.

## Referencias iniciales

- [Idescat - Lloguer d'habitatges: contractes i preu mitjà](https://www.idescat.cat/indicadors/?id=basics&n=22279&t=202504)
- [Agència Catalana de l'Aigua - Dades de consum](https://aca.gencat.cat/ca/laigua/portal-sequera/estat-actual/dades-consum/)
- [Servei Català de Trànsit - Dades obertes d'accidents](https://transit.gencat.cat/ca/seguretat_viaria/observatori/dades-obertes/)