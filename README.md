# Filtro de Kalman

## ¿Qué es?

El filtro de Kalman es un algoritmo matemático utilizado para estimar el estado de un sistema dinámico a partir de mediciones ruidosas o incompletas. Combina predicciones de un modelo matemático con observaciones reales para obtener una estimación más precisa.

## Idea básica

Supongamos que quieres conocer la posición de un automóvil:

- Un modelo físico predice dónde debería estar.
- Un GPS mide dónde está, pero con errores.

El filtro de Kalman combina ambas fuentes para producir una mejor estimación.

## Funcionamiento

### 1. Predicción

Usa el modelo del sistema para estimar el siguiente estado.

Ejemplo:

- Posición actual: 100 m
- Velocidad: 10 m/s

Después de 1 segundo:

- Posición estimada: 110 m

También estima la incertidumbre de esta predicción.

### 2. Corrección

Llega una nueva medición.

Ejemplo:

- GPS: 112 m

El filtro combina:

- Predicción: 110 m
- Medición: 112 m

Resultado:

- Estimación final: 111.4 m

## Ganancia de Kalman

La ganancia de Kalman (K) determina cuánto confiar en:

- El modelo matemático.
- La medición.

Si la medición es muy confiable, el filtro le dará más peso.

## Fórmula principal

```math
x = x_pred + K(z - Hx_pred)
```

Donde:

- x: estado corregido.
- x_pred: estado predicho.
- z: medición.
- H: matriz de observación.
- K: ganancia de Kalman.

## Aplicaciones

### Navegación GPS

- Smartphones
- Drones
- Vehículos autónomos
- Aviones

### Robótica

- Localización
- Estimación de velocidad
- Fusión de sensores

### Finanzas

- Filtrado de ruido
- Detección de tendencias
- Trading cuantitativo

### Procesamiento de señales

- Eliminación de ruido
- Seguimiento de señales

### Industria aeroespacial

- Satélites
- Navegación espacial
- Sistemas de aterrizaje

## Ventajas

- Alta eficiencia computacional.
- Funciona en tiempo real.
- Integra múltiples sensores.
- Produce estimaciones óptimas bajo ciertas condiciones.

## Limitaciones

El filtro clásico asume:

- Sistemas lineales.
- Ruido gaussiano.

Para sistemas más complejos existen variantes como:

- Extended Kalman Filter (EKF)
- Unscented Kalman Filter (UKF)
- Particle Filter

## Analogía

Imagina que caminas en medio de una niebla:

- Tu experiencia te indica hacia dónde crees que avanzas.
- De vez en cuando observas referencias borrosas.

El filtro de Kalman combina ambas fuentes para estimar tu posición real con la mayor precisión posible.

## Conclusión

El filtro de Kalman es una herramienta fundamental para estimar estados ocultos en sistemas dinámicos. Su capacidad para combinar predicciones y observaciones lo convierte en una pieza clave en navegación, robótica, finanzas y muchas otras disciplinas.

---

## Ejemplo práctico: CO2 en Mauna Loa (`kalman_co2_mauna_loa.py`)

### Descripción

Script que aplica el filtro de Kalman a datos reales de concentración atmosférica de CO2 medidos mensualmente en el Observatorio de Mauna Loa (NOAA). Demuestra cómo el filtro estima una señal más estable eliminando el ruido estacional y el ruido de medición inherente a los instrumentos.

### Datos de entrada

- **Archivo:** `co2_mauna_loa_monthly.csv`
- **Fuente original:** NOAA Global Monitoring Laboratory / *Trends in Atmospheric Carbon Dioxide*
- **Columnas usadas:**
  - `Date`: fecha mensual en formato `YYYY-MM`
  - `Average`: concentración de CO2 en ppm
  - `Uncertainty`: incertidumbre instrumental de cada medición

### Modelo de Kalman utilizado

El filtro implementa un **modelo de velocidad constante en 1D** con un vector de estado de dos componentes:

```
x = [nivel_CO2 (ppm), cambio_mensual_CO2 (ppm/mes)]
```

Ecuaciones de transición:

```
nivel[t]         = nivel[t-1] + cambio_mensual[t-1]
cambio_mensual[t] = cambio_mensual[t-1]
```

Solo el nivel de CO2 es observable; la tasa de cambio mensual es una variable **latente** estimada por el filtro.

### Parámetros principales

| Parámetro | Valor por defecto | Descripción |
|---|---|---|
| `process_var_level` | `0.04` | Varianza del proceso para el nivel de CO2 |
| `process_var_velocity` | `0.005` | Varianza del proceso para la tasa mensual |
| `measurement_uncertainty` | columna `Uncertainty` del CSV | Incertidumbre de cada medición (o 5% de la desviación estándar si no se provee) |

### Salidas generadas

- **`co2_mauna_loa_kalman_result.csv`** — CSV con columnas adicionales:
  - `Kalman_CO2_ppm`: nivel de CO2 filtrado
  - `Kalman_Monthly_Change_ppm`: tasa de cambio mensual estimada
  - `Residual_ppm`: diferencia entre medición real y estimación Kalman
- **`kalman_co2_resultado.png`** — Gráfico (160 dpi) comparando CO2 medido vs. CO2 estimado

### Cómo ejecutar

1. Coloca `co2_mauna_loa_monthly.csv` en la misma carpeta que el script.
2. Instala las dependencias:

```bash
pip install numpy pandas matplotlib
```

3. Ejecuta el script:

```bash
python kalman_co2_mauna_loa.py
```

La consola imprimirá un resumen con la última fecha procesada, el valor medido, el valor estimado y la tasa de cambio mensual.

### Casos de uso similares

El mismo patrón es aplicable a:

- Suavizado de lecturas de sensores IoT
- Filtrado de telemetría ambiental
- Suavizado de series de tiempo de negocio (ventas, demanda, etc.)

---

## Ejemplos reales del Filtro de Kalman

### Navegación GPS

El filtro de Kalman es el núcleo de los sistemas GPS. Combina la señal satelital (ruidosa por interferencias atmosféricas y multitrayectoria) con modelos de movimiento del vehículo para producir una posición suave y continua. Todos los smartphones, drones y vehículos autónomos lo usan en tiempo real.

### Navegación en túneles (GPS-denied)

Cuando un vehículo entra a un túnel y pierde señal GPS, el filtro de Kalman integra datos de la IMU (acelerómetro + giroscopio) y del odómetro para estimar la posición sin señal externa. Al salir del túnel, el filtro fusiona nuevamente con GPS corrigiendo la deriva acumulada.

### Vuelo de aeronaves y misiles

En aviación, el filtro de Kalman fusiona datos de giroscopios, acelerómetros, altímetros y GPS para estimar la actitud (roll, pitch, yaw) y posición del avión. Fue uno de los primeros usos del algoritmo, introducido en los años 60 durante el programa Apollo de la NASA.

### Vehículos autónomos

Los autos sin conductor combinan LIDAR, cámaras, radar y GPS. El filtro de Kalman (o su variante extendida, EKF) fusiona todas estas fuentes heterogéneas para mantener una estimación coherente del entorno y la posición del vehículo.

### Robótica móvil (SLAM)

En robots móviles, la técnica SLAM (Simultaneous Localization and Mapping) usa el filtro de Kalman para construir un mapa del entorno y localizar al robot dentro de él al mismo tiempo, corrigiendo errores de odometría con sensores externos.

### Seguimiento de objetos en visión por computadora

En video y cámaras de seguridad, el filtro de Kalman predice la posición de un objeto entre fotogramas, permitiendo rastrear personas, vehículos o pelotas incluso cuando la detección falla temporalmente (oclusión).

### Finanzas y trading algorítmico

Se aplica para estimar la tendencia subyacente de una serie de precios, filtrando el ruido de mercado. Permite detectar señales de compra/venta sin reaccionar a fluctuaciones aleatorias de corto plazo.

### Medicina y señales biomédicas

En electrocardiogramas (ECG) y electroencefalogramas (EEG), el filtro de Kalman elimina ruido eléctrico e interferencias musculares para obtener señales limpias que permitan diagnósticos más precisos.

### Meteorología y predicción numérica

Los modelos meteorológicos usan variantes del filtro de Kalman (como el EnKF, Ensemble Kalman Filter) para asimilar datos de estaciones, satélites y radiosondas, mejorando continuamente las predicciones del tiempo.

### Monitoreo ambiental (como este ejemplo)

La estimación de CO2 atmosférico en Mauna Loa es un caso directo: el filtro separa la tendencia real de largo plazo del ruido estacional e instrumental, produciendo una señal limpia y una tasa de cambio mensual estimada.

---

*Desarrollado por: Jose Alfredo Sanchez*
