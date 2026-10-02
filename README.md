# Catálogo de AnchorPS5

**Español** · [English](README.en.md)

Lista oficial de homebrew que muestra [AnchorPS5](https://github.com/Kuroge/AnchorPS5),
el gestor de homebrew para PS5. La app descarga este [`catalog.json`](catalog.json) y,
para cada app, saca los ficheros descargables (con su SHA-256) de las **releases de su
propio repo de GitHub**. Aquí solo está la lista: no se alojan binarios.

## Qué entra en el catálogo

Homebrew para PS5: servidores (FTP, web…), utilidades, gestores de partidas guardadas, reproductores, etc.

## ¿Quieres añadir una app?

Lee la [guía para contribuir](CONTRIBUIR.md). Se hace todo desde la web de GitHub y hay
un [prompt para IA](PROMPT-IA.md) que te prepara la entrada a partir del enlace de la app.

## Formato

Cada app de la lista `apps`:

| Campo | Obligatorio | Qué es |
|---|---|---|
| `id` | Sí | `github:` + el repo, p. ej. `github:ps5-payload-dev/ftpsrv` |
| `name` | Sí | Nombre que se muestra |
| `author` | Sí | Autor (normalmente el dueño del repo) |
| `repo` | Sí | Repo de GitHub con las releases: `autor/nombre` |
| `description` | Sí | Texto o traducciones: `{ "es": "…", "en": "…" }` (siempre con `es`) |
| `iconUrl` | No | Imagen `https://` (p. ej. `https://github.com/autor.png?size=256`) |
| `assets` | No | Reglas para los ficheros de la release: `match` (con `*` y `?`), `label`, `description`, `hidden` |

El formato completo está en [`catalog.schema.json`](catalog.schema.json) y cada cambio se
comprueba automáticamente con [`scripts/validar.py`](scripts/validar.py).

## Créditos

- **Huertas34**, de [elotrolado.net](https://www.elotrolado.net), por la sugerencia inicial del catálogo.
- Gracias a los autores de cada app: aquí solo se enlazan sus releases.
