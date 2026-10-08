## Qué cambia

<!-- Describe el cambio en una o dos frases. -->

## Tipo de rama

- [ ] `feature/*` → `develop`
- [ ] `release/*` → `main` (y después a `develop`)
- [ ] `hotfix/*` → `main` (y después a `develop`)

## Comprobaciones

- [ ] `uv run ruff format --check` y `uv run ruff check` sin errores
- [ ] `uv run pytest` en verde
- [ ] Pruebas nuevas o actualizadas para el cambio
- [ ] `CHANGELOG.md` actualizado si cambia el comportamiento visible
