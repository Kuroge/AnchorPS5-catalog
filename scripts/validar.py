"""
Comprueba catalog.json antes de aceptar un cambio:
  1. Es JSON válido y cumple catalog.schema.json.
  2. Sin ids ni repos repetidos; el id es "github:" + repo.
  3. Cada repo existe en GitHub y tiene al menos una release publicada.

Uso: python scripts/validar.py [catalog.json] [--sin-red]
Con la variable GITHUB_TOKEN las consultas a GitHub no se quedan sin cupo.
"""

import json
import os
import sys
import urllib.error
import urllib.request

from jsonschema import Draft202012Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def github(path):
    request = urllib.request.Request("https://api.github.com/" + path, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # emojis también en la consola de Windows
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = files[0] if files else os.path.join(ROOT, "catalog.json")
    errors = []

    try:
        with open(path, encoding="utf-8") as f:
            catalog = json.load(f)
    except json.JSONDecodeError as error:
        print(f"❌ catalog.json no es un JSON válido (línea {error.lineno}, columna {error.colno}): {error.msg}")
        print("   Suele ser una coma que sobra o que falta, o unas comillas sin cerrar.")
        return 1

    with open(os.path.join(ROOT, "catalog.schema.json"), encoding="utf-8") as f:
        schema = json.load(f)

    for error in sorted(Draft202012Validator(schema).iter_errors(catalog), key=lambda e: [str(p) for p in e.path]):
        errors.append(f"{where(catalog, error.path)}: {explain(error)}")

    if errors:
        report(errors)
        return 1

    ids, repos = {}, {}
    for i, app in enumerate(catalog["apps"]):
        name = f"apps/{i} ({app['name']})"
        app_id, repo = app["id"].lower(), app["repo"].lower()
        if app_id in ids:
            errors.append(f"{name}: el id {app['id']} ya está en {ids[app_id]}")
        if repo in repos:
            errors.append(f"{name}: el repo {app['repo']} ya está en {repos[repo]}")
        ids.setdefault(app_id, name)
        repos.setdefault(repo, name)
        if app_id != "github:" + repo:
            errors.append(f"{name}: el id debe ser \"github:{app['repo']}\"")

    if not errors and "--sin-red" not in sys.argv:
        for app in catalog["apps"]:
            info = github(f"repos/{app['repo']}")
            if info is None:
                errors.append(f"{app['name']}: el repo {app['repo']} no existe o es privado")
                continue
            releases = github(f"repos/{app['repo']}/releases?per_page=5") or []
            if not any(not r.get("draft") for r in releases):
                errors.append(f"{app['name']}: el repo {app['repo']} no tiene ninguna release publicada")

    if errors:
        report(errors)
        return 1

    print(f"✅ catalog.json es correcto ({len(catalog['apps'])} apps).")
    return 0


FORMATS = {
    "id": 'tiene que ser "github:" + el repo, p. ej. "github:ps5-payload-dev/ftpsrv"',
    "repo": 'tiene que ser "autor/nombre-del-repo", p. ej. "ps5-payload-dev/ftpsrv"',
    "iconUrl": "tiene que ser un enlace que empiece por https://",
}


def where(catalog, path):
    """'App nº 4 «nanoDNS» → description' en vez de 'apps/3/description'."""
    path = list(path)
    if len(path) >= 2 and path[0] == "apps" and isinstance(path[1], int):
        app = catalog["apps"][path[1]]
        name = app.get("name") if isinstance(app, dict) else None
        label = f"App nº {path[1] + 1}" + (f" «{name}»" if name else "")
        rest = "/".join(str(p) for p in path[2:])
        return label + (f" → {rest}" if rest else "")
    return "/".join(str(p) for p in path) or "catalog.json"


def explain(error):
    """Mensaje en español y con la pista para arreglarlo (los de jsonschema vienen en inglés)."""
    field = str(error.path[-1]) if error.path else ""
    kind = error.validator
    if kind == "required":
        missing = [p for p in error.validator_value if p not in error.instance]
        return "falta el campo obligatorio " + ", ".join(f'"{p}"' for p in missing)
    if kind == "additionalProperties":
        extra = [p for p in error.instance if p not in error.schema.get("properties", {})]
        return "campo desconocido " + ", ".join(f'"{p}"' for p in extra) + " (¿está mal escrito?)"
    if kind == "minLength":
        return "no puede estar vacío"
    if kind == "maxLength":
        return f"es demasiado largo (máximo {error.validator_value} caracteres)"
    if kind == "pattern":
        return FORMATS.get(field, "no tiene el formato correcto")
    if kind == "oneOf":
        return 'tiene que ser un texto o { "es": "…", "en": "…" } (siempre con "es")'
    if kind == "const":
        return f"tiene que ser {error.validator_value}"
    if kind == "type":
        names = {"string": "un texto entre comillas", "array": "una lista [ … ]", "object": "un objeto { … }", "boolean": "true o false"}
        return "tiene que ser " + names.get(error.validator_value, str(error.validator_value))
    return error.message


def report(errors):
    print("❌ Hay que corregir catalog.json:")
    for error in errors:
        print("   - " + error)


if __name__ == "__main__":
    sys.exit(main())
