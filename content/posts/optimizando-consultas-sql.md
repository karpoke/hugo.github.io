---
title: "Optimizando consultas SQL: De 5 segundos a 50ms"
date: 2024-02-10T14:30:00+01:00
draft: false
tags: ["sql", "bases-de-datos", "optimización", "performance"]
slug: optimizando-consultas-sql
description: "Cómo optimicé una consulta SQL que tardaba 5 segundos reduciéndola a 50ms usando índices y análisis de query plans."
---

## El problema

Hace unas semanas me enfrenté a un problema clásico: una consulta SQL que funcionaba perfectamente con 1000 registros empezó a tardar **más de 5 segundos** cuando la tabla creció a 500,000 registros.

La consulta original era algo así:

```sql
SELECT 
    u.id,
    u.nombre,
    u.email,
    COUNT(p.id) as total_pedidos,
    SUM(p.total) as suma_total
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id
WHERE u.fecha_registro >= '2023-01-01'
    AND p.estado IN ('completado', 'enviado')
GROUP BY u.id, u.nombre, u.email
ORDER BY suma_total DESC
LIMIT 50;
```

## Diagnóstico: EXPLAIN es tu amigo

Lo primero que hice fue usar `EXPLAIN ANALYZE`:

```sql
EXPLAIN ANALYZE
SELECT ...
```

El resultado mostró:

- **Sequential Scan** en la tabla usuarios (500K filas escaneadas)
- **Sequential Scan** en pedidos (1.2M filas)
- No había índices en las columnas de filtrado

## La solución

### 1. Crear índices estratégicos

```sql
-- Índice en fecha_registro para el WHERE
CREATE INDEX idx_usuarios_fecha_registro 
ON usuarios(fecha_registro);

-- Índice compuesto en pedidos
CREATE INDEX idx_pedidos_usuario_estado 
ON pedidos(usuario_id, estado);

-- Índice para el JOIN
CREATE INDEX idx_pedidos_usuario_id 
ON pedidos(usuario_id);
```

### 2. Reescribir la consulta

```sql
SELECT 
    u.id,
    u.nombre,
    u.email,
    COALESCE(stats.total_pedidos, 0) as total_pedidos,
    COALESCE(stats.suma_total, 0) as suma_total
FROM usuarios u
LEFT JOIN (
    SELECT 
        usuario_id,
        COUNT(*) as total_pedidos,
        SUM(total) as suma_total
    FROM pedidos
    WHERE estado IN ('completado', 'enviado')
    GROUP BY usuario_id
) stats ON u.id = stats.usuario_id
WHERE u.fecha_registro >= '2023-01-01'
ORDER BY stats.suma_total DESC NULLS LAST
LIMIT 50;
```

## Resultados

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Tiempo de ejecución | 5200ms | 48ms | **108x más rápido** |
| Filas escaneadas | 1.7M | 12K | 99% reducción |
| Uso de índices | 0 | 3 | ✅ |

## Lecciones aprendidas

1. **EXPLAIN es obligatorio**: Nunca optimices sin entender qué está pasando
2. **Índices compuestos**: Son más efectivos que múltiples índices simples
3. **Subqueries estratégicas**: A veces ayudan al optimizador
4. **Medir siempre**: Lo que no se mide no se puede mejorar

## Código Python para benchmark

Si quieres hacer tus propios benchmarks:

```python
import time
import psycopg2

def benchmark_query(conn, query, iterations=10):
    """Ejecuta una query múltiples veces y devuelve estadísticas."""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        with conn.cursor() as cur:
            cur.execute(query)
            cur.fetchall()
        
        end = time.perf_counter()
        times.append((end - start) * 1000)  # ms
    
    return {
        'min': min(times),
        'max': max(times),
        'avg': sum(times) / len(times),
        'median': sorted(times)[len(times) // 2]
    }

# Uso
conn = psycopg2.connect("dbname=mydb user=postgres")
stats = benchmark_query(conn, "SELECT ...")
print(f"Tiempo promedio: {stats['avg']:.2f}ms")
```

## Recursos adicionales

- [Use The Index, Luke](https://use-the-index-luke.com/) - Guía completa sobre índices
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [MySQL Query Optimization](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)

## Conclusión

La optimización de queries es un arte y una ciencia. Con las herramientas adecuadas (EXPLAIN, índices, reescrituras) puedes lograr mejoras dramáticas en el rendimiento.

¿Has tenido que optimizar consultas lentas? ¿Qué técnicas te han funcionado mejor?
