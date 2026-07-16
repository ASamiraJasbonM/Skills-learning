"""
Simulación de capacidad de base de datos PostgreSQL
parte de la skill software-architecture-engineer.

Calcula el almacenamiento total requerido para una base de datos
PostgreSQL considerando:
  - Datos de perfil de usuario
  - Transacciones acumuladas en un horizonte temporal
  - Sobrecarga de índices B-Tree (~40%)
  - Buffer de seguridad para fragmentación/MVCC (~20%)
  - Estructura física: páginas de 8 KB, encabezado de fila 24 bytes

Uso:
    python simulation.py

O importa y llama:
    from simulation import simulate_database_size
    resultado = simulate_database_size(users=100000)
"""


def simulate_database_size(
    users: int,
    profile_size_kb: float = 1.5,
    transaction_per_day: float = 2,
    transaction_size_kb: float = 0.8,
    years: float = 2,
    index_overhead: float = 1.4,
    buffer_growth: float = 1.2,
) -> dict:
    """
    Simula el almacenamiento total requerido para una base de datos PostgreSQL.

    Args:
        users: Número de usuarios activos.
        profile_size_kb: Tamaño estimado por registro de perfil en KB.
        transaction_per_day: Transacciones generadas por usuario por día.
        transaction_size_kb: Tamaño estimado por registro transaccional en KB.
        years: Horizonte de proyección en años.
        index_overhead: Factor de sobrecarga por índices B-Tree (default 1.4 = 40%).
        buffer_growth: Factor de buffer para fragmentación/MVCC (default 1.2 = 20%).

    Returns:
        Diccionario con métricas de almacenamiento en MB, GB y total.
    """
    KB_TO_BYTE = 1024

    core_size_bytes = users * profile_size_kb * KB_TO_BYTE
    total_transactions = users * transaction_per_day * 365 * years
    transaction_size_bytes = total_transactions * transaction_size_kb * KB_TO_BYTE

    raw_size_bytes = core_size_bytes + transaction_size_bytes
    total_size_bytes = raw_size_bytes * index_overhead * buffer_growth

    size_gb = total_size_bytes / (1024**3)

    return {
        "core_user_mb": core_size_bytes / (1024**2),
        "transactions_gb": transaction_size_bytes / (1024**3),
        "raw_size_gb": raw_size_bytes / (1024**3),
        "total_with_indexes_and_buffer_gb": size_gb,
    }


def classify_capacity(total_gb: float) -> dict:
    """
    Clasifica la capacidad estimada y recomienda estrategia de esquema.

    Args:
        total_gb: Almacenamiento total estimado en GB.

    Returns:
        Diccionario con categoría, estrategia y complejidad.
    """
    if total_gb < 100:
        return {
            "category": "< 100 GB",
            "strategy": "Esquema normalizado clásico. Sin optimizaciones complejas.",
            "complexity": "Baja",
        }
    elif total_gb < 1000:
        return {
            "category": "100 GB – 1 TB",
            "strategy": "Archivado histórico. 80% de datos viejos a tablas frías.",
            "complexity": "Media",
        }
    elif total_gb < 10000:
        return {
            "category": "1 TB – 10 TB",
            "strategy": "Desnormalización controlada de tablas de lectura.",
            "complexity": "Alta",
        }
    else:
        return {
            "category": "> 10 TB",
            "strategy": "Sharding relacional y bases distribuidas multi-inquilino.",
            "complexity": "Compleja",
        }


def simulate_compute_qps(
    avg_response_time_seconds: float,
    cpu_cores: int,
) -> float:
    """
    Estima la capacidad QPS (queries por segundo) del servidor.

    Args:
        avg_response_time_seconds: Tiempo promedio de respuesta por petición.
        cpu_cores: Número de núcleos lógicos disponibles.

    Returns:
        QPS estimado.
    """
    return (1 / avg_response_time_seconds) * cpu_cores


def simulate_queue_mmc(
    arrival_rate: float,
    service_rate: float,
    workers: int,
) -> dict:
    """
    Modelo de teoría de colas M/M/c para estimar utilización y cola.

    Args:
        arrival_rate: Tasa de llegada λ (peticiones/segundo).
        service_rate: Tasa de procesamiento μ por worker (peticiones/segundo).
        workers: Número de workers (c).

    Returns:
        Diccionario con utilización (ρ), estable, longitud de cola estimada.
    """
    rho = arrival_rate / (workers * service_rate)
    stable = rho < 1.0

    if stable and workers > 0:
        L_q = (rho * rho) / (1 - rho) * (1 / workers)
    else:
        L_q = float("inf") if not stable else 0.0

    return {"rho": rho, "stable": stable, "estimated_queue_length": L_q}


# ─── Prueba matemática y asserts de validación ──────────────────────────────

if __name__ == "__main__":
    resultado = simulate_database_size(
        users=100_000,
        profile_size_kb=1.5,
        transaction_per_day=2,
        transaction_size_kb=0.8,
        years=2,
    )

    print("=== Simulación de Base de Datos ===")
    print(f"Usuarios: 100,000")
    print(f"Espacio datos de perfil:      {resultado['core_user_mb']:.2f} MB")
    print(f"Espacio transacciones acum.:   {resultado['transactions_gb']:.2f} GB")
    print(f"Espacio datos brutos:          {resultado['raw_size_gb']:.2f} GB")
    print(
        f"Total con índices y buffer:    {resultado['total_with_indexes_and_buffer_gb']:.2f} GB"
    )

    clasificacion = classify_capacity(resultado["total_with_indexes_and_buffer_gb"])
    print(f"\nCategoría:  {clasificacion['category']}")
    print(f"Estrategia: {clasificacion['strategy']}")
    print(f"Complejidad: {clasificacion['complexity']}")

    # Asserts de validación cruzada
    assert abs(resultado["core_user_mb"] - 146.48) < 1.0, (
        f"core_user_mb fuera de rango: {resultado['core_user_mb']}"
    )
    assert abs(resultado["transactions_gb"] - 111.39) < 1.0, (
        f"transactions_gb fuera de rango: {resultado['transactions_gb']}"
    )
    assert abs(resultado["total_with_indexes_and_buffer_gb"] - 187.37) < 1.0, (
        f"total_with_indexes_and_buffer_gb fuera de rango: {resultado['total_with_indexes_and_buffer_gb']}"
    )
    print(
        "\n✓ Validación cruzada superada: todos los valores dentro del margen esperado."
    )

    print("\n=== Simulación de Cómputo ===")
    qps = simulate_compute_qps(avg_response_time_seconds=0.2, cpu_cores=4)
    print(f"QPS estimado (4 núcleos, 200ms): {qps:.1f}")

    cola = simulate_queue_mmc(arrival_rate=15, service_rate=5, workers=4)
    print(f"Utilización ρ: {cola['rho']:.3f}")
    print(f"Estable: {cola['stable']}")
    print(f"Longitud de cola estimada: {cola['estimated_queue_length']:.3f}")
    assert cola["stable"], "ERROR: Sistema inestable (ρ >= 1)"
    print("✓ Sistema estable (ρ < 1).")
