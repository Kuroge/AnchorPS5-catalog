# AnchorPS5 catalog

[Español](README.md) · **English**

Official homebrew list shown by [AnchorPS5](https://github.com/Kuroge/AnchorPS5), the
homebrew manager for PS5. The app downloads this [`catalog.json`](catalog.json) and, for
each app, gets the downloadable files (with their SHA-256) from the **releases of the
app's own GitHub repository**. Only the list lives here: no binaries are hosted.

| File | What it is |
|---|---|
| [`catalog.json`](catalog.json) | The app list. **It's the only one you edit.** |
| [`releases.json`](releases.json) | Release index (see below). Generated automatically: don't edit it. |
| [`catalog.schema.json`](catalog.schema.json) | The format of `catalog.json`. |

## What goes into the catalog

PS5 homebrew: servers (FTP, web…), utilities, save data managers, media players, etc.

## Want to add an app?

Read the [contributing guide](CONTRIBUTING.md). Everything is done from the GitHub
website, and there is an [AI prompt](AI-PROMPT.md) that prepares the entry from the
app's link.

## Format

Each app in the `apps` list:

| Field | Required | What it is |
|---|---|---|
| `id` | Yes | `github:` + the repo, e.g. `github:ps5-payload-dev/ftpsrv` |
| `name` | Yes | Display name |
| `author` | Yes | Author (usually the repo owner) |
| `repo` | Yes | GitHub repo with the releases: `owner/name` |
| `description` | Yes | Text or translations: `{ "es": "…", "en": "…" }` (always with `es`) |
| `iconUrl` | No | `https://` image (e.g. `https://github.com/owner.png?size=256`) |
| `assets` | No | Rules for the release files: `match` (with `*` and `?`), `label`, `description`, `hidden` |

The full format is in [`catalog.schema.json`](catalog.schema.json) and every change is
checked automatically by [`scripts/validar.py`](scripts/validar.py).

## Release index

To avoid depending on GitHub's request limit (60 per hour without a session), this repo
publishes [`releases.json`](releases.json): the latest releases of every catalog app,
with their files, sizes and SHA-256. An automatic task
([`scripts/indice.py`](scripts/indice.py)) is scheduled **every hour** (GitHub usually delays it, so in practice it runs every few
hours) and also runs every time `catalog.json` changes; it's only saved if something changed.

When you're not signed in to GitHub, AnchorPS5 downloads this single file instead of
asking GitHub app by app. That's why a just-published release may take a few hours to
show up in the index. Signed in, the app asks GitHub directly and the index is the
fallback.

## Credits

- **Huertas34**, from [elotrolado.net](https://www.elotrolado.net), for the initial catalog suggestion.
- Thanks to the authors of each app: this repo only links to their releases.
