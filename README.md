# reservas-demo

API de reservas de mesas del restaurante ficticio **Casa Demo**: mesas, franjas horarias,
reservas, cancelaciones y reglas sencillas de disponibilidad.

## Requisitos

- Python 3.12 (declarado en `.python-version`).
- [uv](https://docs.astral.sh/uv/) para gestionar el entorno y las dependencias (`uv.lock`).

No hace falta ningún servicio externo: los datos se guardan en un fichero SQLite
(`reservas.db` por defecto, configurable con `RESERVAS_DATABASE_URL`; ver `.env.example`).

## Puesta en marcha

```bash
uv sync --locked                     # instala dependencias exactas del lock
uv run python -m reservas.seed       # (opcional) carga las mesas de demostración
uv run uvicorn reservas.main:app --reload --port 8000
```

La documentación interactiva queda en <http://localhost:8000/docs>.
Las tablas se crean solas al arrancar (todavía no hay migraciones).

## Comandos habituales

| Tarea | Comando |
| --- | --- |
| Lint | `uv run ruff check` |
| Comprobar formato | `uv run ruff format --check` |
| Formatear | `uv run ruff format` |
| Pruebas | `uv run pytest` |
| Empaquetar | `uv build` |

## Reglas del restaurante

Definidas en `src/reservas/rules.py`:

- Servicios: comida de 13:00 a 15:30 y cena de 20:00 a 22:30, en franjas de 30 minutos.
- Cada reserva ocupa la mesa 90 minutos.
- Los lunes el restaurante cierra.
- Se reserva con un máximo de 60 días de antelación y nunca en el pasado.
- Se puede cancelar hasta 2 horas antes de la hora reservada.
- Si no se indica mesa, se asigna la mesa libre más pequeña en la que caben los comensales.

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/salud` | Estado y versión del servicio |
| GET, POST | `/mesas` | Listar y crear mesas |
| GET | `/mesas/{id}` | Detalle de una mesa |
| POST | `/mesas/{id}/desactivar` | Retirar una mesa de la sala |
| GET | `/franjas?fecha=&comensales=` | Franjas del día con mesas libres |
| GET, POST | `/reservas` | Listar (filtro `fecha`) y crear reservas |
| GET | `/reservas/{id}` | Detalle de una reserva |
| POST | `/reservas/{id}/cancelar` | Cancelar una reserva |
| GET | `/resumen?fecha=` | Resumen del día para cocina |

## Estructura

```
src/reservas/
  main.py          aplicación FastAPI y registro de routers
  config.py        configuración por variables de entorno
  db.py            motor SQLAlchemy y sesiones
  models.py        modelos ORM (Mesa, Reserva)
  schemas.py       cuerpos de petición y respuesta
  rules.py         reglas de negocio del restaurante
  availability.py  cálculo de mesas libres
  clock.py         hora actual como dependencia (congelable en pruebas)
  seed.py          datos de demostración
  routers/         endpoints por recurso
tests/             pruebas con pytest (SQLite en memoria)
```

## Cómo contribuir

El proyecto sigue **Git Flow**. Lee [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir una PR.
