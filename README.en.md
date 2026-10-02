# AnchorPS5 catalog

[Español](README.md) · **English**

Official homebrew list shown by [AnchorPS5](https://github.com/Kuroge/AnchorPS5), the
homebrew manager for PS5. The app downloads this [`catalog.json`](catalog.json) and, for
each app, gets the downloadable files (with their SHA-256) from the **releases of the
app's own GitHub repository**. Only the list lives here: no binaries are hosted.

## What goes into the catalog

- ✅ PS5 homebrew that runs on a console **already in homebrew mode**: servers (FTP,
  web…), utilities, save data managers, media players, etc.
- ❌ Exploits, jailbreaks and tools that put the console into homebrew mode.
- ❌ Piracy: copying, dumping or loading commercial games or their backups.
- ❌ Bypassing DRM, licenses or accounts.

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
