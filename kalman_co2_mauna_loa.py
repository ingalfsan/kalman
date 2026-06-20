"""
Filtro de Kalman aplicado a datos reales de CO2 de Mauna Loa.

Aplicación real:
- Las mediciones atmosféricas mensuales tienen variación estacional y ruido.
- El filtro de Kalman estima una señal latente más estable y una tasa de cambio mensual.
- Útil como patrón para suavizar sensores IoT, lecturas ambientales, telemetría o series de tiempo de negocio.

Data incluida:
- co2_mauna_loa_monthly.csv
- Fuente original: NOAA Global Monitoring Laboratory / Trends in Atmospheric Carbon Dioxide.
- Dataset CSV publicado por DataHub/GitHub a partir de NOAA.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def kalman_filter_1d_constant_velocity(
    measurements: np.ndarray,
    measurement_uncertainty: np.ndarray | None = None,
    process_var_level: float = 0.04,
    process_var_velocity: float = 0.005,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Filtro de Kalman 1D con modelo de velocidad constante.

    Estado:
        x = [nivel_CO2, cambio_mensual_CO2]

    Modelo:
        nivel[t] = nivel[t-1] + cambio_mensual[t-1]
        cambio_mensual[t] = cambio_mensual[t-1]

    Parámetros:
        measurements: mediciones observadas, por ejemplo CO2 ppm mensual.
        measurement_uncertainty: incertidumbre de cada medición.
        process_var_level: cuánto permitimos que cambie el nivel entre meses.
        process_var_velocity: cuánto permitimos que cambie la tasa mensual.

    Retorna:
        states: matriz n x 2 con nivel filtrado y cambio mensual estimado.
        covariances: covarianzas de cada paso.
    """
    measurements = np.asarray(measurements, dtype=float)
    n = len(measurements)

    if measurement_uncertainty is None:
        measurement_uncertainty = np.full(n, np.nanstd(measurements) * 0.05)
    else:
        measurement_uncertainty = np.asarray(measurement_uncertainty, dtype=float)

    # Estado inicial: primera medición y primer cambio observado.
    initial_velocity = measurements[1] - measurements[0] if n > 1 else 0.0
    x = np.array([[measurements[0]], [initial_velocity]], dtype=float)

    # Incertidumbre inicial alta: el filtro arranca flexible.
    P = np.array([[10.0, 0.0], [0.0, 1.0]], dtype=float)

    # Transición de estado: nivel + velocidad.
    F = np.array([[1.0, 1.0], [0.0, 1.0]], dtype=float)

    # Observamos solo el nivel, no la velocidad.
    H = np.array([[1.0, 0.0]], dtype=float)

    # Ruido del proceso.
    Q = np.array([[process_var_level, 0.0], [0.0, process_var_velocity]], dtype=float)

    I = np.eye(2)

    states = []
    covariances = []

    for i, z in enumerate(measurements):
        # 1) Predicción
        x = F @ x
        P = F @ P @ F.T + Q

        # 2) Corrección con medición real
        R = np.array([[max(float(measurement_uncertainty[i]) ** 2, 0.01)]])
        y = np.array([[z]]) - H @ x
        S = H @ P @ H.T + R
        K = P @ H.T @ np.linalg.inv(S)

        x = x + K @ y
        P = (I - K @ H) @ P

        states.append(x.flatten())
        covariances.append(P.copy())

    return np.array(states), np.array(covariances)


def main() -> None:
    current_dir = Path(__file__).resolve().parent
    csv_path = current_dir / "co2_mauna_loa_monthly.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"No encontré {csv_path.name}. Coloca el CSV en la misma carpeta que este script."
        )

    df = pd.read_csv(csv_path)

    # Convertimos fechas mensuales tipo YYYY-MM a datetime.
    df["Date"] = pd.to_datetime(df["Date"] + "-01")

    # Quitamos filas sin dato válido, por si cambias el CSV por el dataset completo.
    df = df[df["Average"] > 0].copy()
    df = df.sort_values("Date").reset_index(drop=True)

    states, _ = kalman_filter_1d_constant_velocity(
        measurements=df["Average"].to_numpy(),
        measurement_uncertainty=df["Uncertainty"].to_numpy(),
        process_var_level=0.04,
        process_var_velocity=0.005,
    )

    df["Kalman_CO2_ppm"] = states[:, 0]
    df["Kalman_Monthly_Change_ppm"] = states[:, 1]
    df["Residual_ppm"] = df["Average"] - df["Kalman_CO2_ppm"]

    output_csv = current_dir / "co2_mauna_loa_kalman_result.csv"
    output_png = current_dir / "kalman_co2_resultado.png"

    df.to_csv(output_csv, index=False)

    plt.figure(figsize=(11, 6))
    plt.plot(df["Date"], df["Average"], marker="o", markersize=3, linewidth=1, label="CO2 medido")
    plt.plot(df["Date"], df["Kalman_CO2_ppm"], linewidth=2.5, label="CO2 estimado con Kalman")
    plt.title("Filtro de Kalman aplicado a CO2 mensual en Mauna Loa")
    plt.xlabel("Fecha")
    plt.ylabel("CO2 atmosférico, ppm")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_png, dpi=160)

    last = df.iloc[-1]
    print("Archivo de resultados:", output_csv.name)
    print("Gráfico generado:", output_png.name)
    print()
    print("Última fecha:", last["Date"].date())
    print(f"CO2 medido: {last['Average']:.2f} ppm")
    print(f"CO2 estimado con Kalman: {last['Kalman_CO2_ppm']:.2f} ppm")
    print(f"Cambio mensual estimado: {last['Kalman_Monthly_Change_ppm']:.3f} ppm/mes")


if __name__ == "__main__":
    main()
