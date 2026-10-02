# Catálogo de AnchorPS5

**Español** · [English](README.en.md)

Lista oficial de homebrew que muestra [AnchorPS5](https://github.com/Kuroge/AnchorPS5),
el gestor de homebrew para PS5. La app descarga este [`catalog.json`](catalog.json) y,
para cada app, saca los ficheros descargables (con su SHA-256) de las **releases de su
propio repo de GitHub**. Aquí solo está la lista: no se alojan binarios.

| Fichero | Qué es |
|---|---|
| [`catalog.json`](catalog.json) | La lista de apps. **Es el único que se edita.** |
| [`releases.json`](releases.json) | Índice de releases (ver abajo). Se genera solo: no lo edites. |
| [`catalog.schema.json`](catalog.schema.json) | El formato de `catalog.json`. |

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

## Índice de releases

Para no depender del límite de consultas de GitHub (60 por hora sin sesión), este repo
publica [`releases.json`](releases.json): las últimas releases de cada app del catálogo,
con sus ficheros, tamaños y SHA-256. Lo genera una tarea automática
([`scripts/indice.py`](scripts/indice.py)) **cada hora** y cada vez que cambia
`catalog.json`, y solo se guarda si algo ha cambiado.

AnchorPS5, si no has iniciado sesión en GitHub, descarga este único fichero en lugar de
preguntar a GitHub app por app. Por eso una release recién publicada puede tardar hasta
una hora en aparecer en el índice. Con sesión, la app pregunta a GitHub directamente y
el índice queda de respaldo.

## Créditos

- **Huertas34**, de [elotrolado.net](https://www.elotrolado.net), por la sugerencia inicial del catálogo.
- Gracias a los autores de cada app: aquí solo se enlazan sus releases.
