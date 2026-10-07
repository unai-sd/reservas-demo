# Cómo contribuir

## Flujo de ramas (Git Flow)

| Rama | Para qué sirve | Nace de | Se integra en |
| --- | --- | --- | --- |
| `main` | Producción. Solo recibe versiones y correcciones urgentes; cada merge lleva etiqueta `vX.Y.Z`. | — | — |
| `develop` | Integración. Es la rama por defecto del repositorio. | `main` | — |
| `feature/<slug>` | Una funcionalidad o mejora. | `develop` | `develop` |
| `release/X.Y.Z` | Preparar una versión: subir versión, CHANGELOG y solo arreglos menores. | `develop` | `main` y `develop` |
| `hotfix/X.Y.Z` | Corrección urgente en producción. | `main` | `main` y `develop` |

Reglas:

- Nunca se hace commit directo en `main` ni en `develop`: todo entra por pull request.
- Las PR se integran con **merge commit** (sin squash ni rebase) para conservar la historia
  de cada rama.
- Las ramas `feature/*` usan un slug corto en minúsculas con guiones,
  p. ej. `feature/lista-de-espera`.
- Al cerrar una `release/*` o un `hotfix/*` se etiqueta el merge en `main` (`vX.Y.Z`,
  etiqueta anotada) y se vuelve a integrar la rama en `develop`.
- La versión vive en `pyproject.toml`; al cambiarla hay que regenerar el lock con `uv lock`.

## Antes de abrir la PR

```bash
uv run ruff format --check
uv run ruff check
uv run pytest
```

La integración continua ejecuta los trabajos `lint` y `test` en cada PR contra `develop`,
`main` o `release/*`. Ambos deben estar en verde para integrar.

## Mensajes de commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/) en español:
`feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `chore: ...`, `ci: ...`.

## Publicar una versión

1. Crear `release/X.Y.Z` desde `develop`.
2. Subir la versión en `pyproject.toml`, ejecutar `uv lock` y completar `CHANGELOG.md`.
3. PR de `release/X.Y.Z` a `main`; tras integrarla, etiquetar `vX.Y.Z` en `main`.
4. PR de `release/X.Y.Z` (o de `main`) a `develop` para devolver los cambios.

Al empujar la etiqueta se lanza el flujo `release`, que empaqueta y simula el despliegue.
