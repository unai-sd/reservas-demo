"""Load the demo tables of Casa Demo: `uv run python -m reservas.seed`."""

from sqlalchemy import select

from reservas.db import SessionLocal, init_db
from reservas.models import Mesa

MESAS_DEMO = [
    ("I1", 2, "interior"),
    ("I2", 2, "interior"),
    ("I3", 4, "interior"),
    ("I4", 4, "interior"),
    ("I5", 6, "interior"),
    ("T1", 2, "terraza"),
    ("T2", 4, "terraza"),
    ("T3", 8, "terraza"),
]


def main() -> None:
    init_db()
    with SessionLocal() as session:
        existentes = set(session.scalars(select(Mesa.nombre)))
        nuevas = [
            Mesa(nombre=nombre, capacidad=capacidad, zona=zona)
            for nombre, capacidad, zona in MESAS_DEMO
            if nombre not in existentes
        ]
        session.add_all(nuevas)
        session.commit()
    print(f"Mesas de demostración cargadas: {len(nuevas)} nuevas")


if __name__ == "__main__":
    main()
