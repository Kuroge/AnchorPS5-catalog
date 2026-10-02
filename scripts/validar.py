"""
Comprueba catalog.json antes de aceptar un cambio · Checks catalog.json before accepting a change:
  1. Es JSON válido y cumple catalog.schema.json · Valid JSON that follows catalog.schema.json.
  2. Sin ids ni repos repetidos; el id es "github:" + repo · No duplicate ids/repos; id is "github:" + repo.
  3. Cada repo existe y tiene alguna release publicada · Each repo exists and has a published release.

Uso · Usage: python scripts/validar.py [catalog.json] [--sin-red]
Con GITHUB_TOKEN las consultas a GitHub no se quedan sin cupo · GITHUB_TOKEN avoids GitHub rate limits.
Cada mensaje sale en español y en inglés · Every message is printed in Spanish and English.
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
    errors = []  # pares (español, inglés)

    try:
        with open(path, encoding="utf-8") as f:
            catalog = json.load(f)
    except json.JSONDecodeError as error:
        print(f"❌ catalog.json no es un JSON válido (línea {error.lineno}, columna {error.colno}).")
        print("   Suele ser una coma que sobra o que falta, o unas comillas sin cerrar.")
        print(f"❌ catalog.json is not valid JSON (line {error.lineno}, column {error.colno}).")
        print("   It's usually a comma too many or missing, or some unclosed quotes.")
        return 1

    with open(os.path.join(ROOT, "catalog.schema.json"), encoding="utf-8") as f:
        schema = json.load(f)

    for error in sorted(Draft202012Validator(schema).iter_errors(catalog), key=lambda e: [str(p) for p in e.path]):
        (where_es, where_en), (what_es, what_en) = where(catalog, error.path), explain(error)
        errors.append((f"{where_es}: {what_es}", f"{where_en}: {what_en}"))

    if errors:
        report(errors)
        return 1

    ids, repos = {}, {}
    for i, app in enumerate(catalog["apps"]):
        es, en = f"App nº {i + 1} «{app['name']}»", f'App #{i + 1} "{app["name"]}"'
        app_id, repo = app["id"].lower(), app["repo"].lower()
        if app_id in ids:
            errors.append((f"{es}: el id {app['id']} ya está en la {ids[app_id][0]}", f"{en}: the id {app['id']} is already in {ids[app_id][1]}"))
        if repo in repos:
            errors.append((f"{es}: el repo {app['repo']} ya está en la {repos[repo][0]}", f"{en}: the repo {app['repo']} is already in {repos[repo][1]}"))
        ids.setdefault(app_id, (es, en))
        repos.setdefault(repo, (es, en))
        if app_id != "github:" + repo:
            errors.append((f'{es}: el id debe ser "github:{app["repo"]}"', f'{en}: the id must be "github:{app["repo"]}"'))

    if not errors and "--sin-red" not in sys.argv:
        for app in catalog["apps"]:
            if github(f"repos/{app['repo']}") is None:
                errors.append((f"«{app['name']}»: el repo {app['repo']} no existe o es privado",
                               f'"{app["name"]}": the repo {app["repo"]} doesn\'t exist or is private'))
                continue
            releases = github(f"repos/{app['repo']}/releases?per_page=5") or []
            if not any(not r.get("draft") for r in releases):
                errors.append((f"«{app['name']}»: el repo {app['repo']} no tiene ninguna release publicada",
                               f'"{app["name"]}": the repo {app["repo"]} has no published release'))

    if errors:
        report(errors)
        return 1

    count = len(catalog["apps"])
    print(f"✅ catalog.json es correcto ({count} apps). · catalog.json is correct ({count} apps).")
    return 0


def where(catalog, path):
    """'App nº 4 «nanoDNS» → description' en vez de 'apps/3/description' (es, en)."""
    path = list(path)
    if len(path) >= 2 and path[0] == "apps" and isinstance(path[1], int):
        app = catalog["apps"][path[1]]
        name = app.get("name") if isinstance(app, dict) else None
        rest = "/".join(str(p) for p in path[2:])
        suffix = f" → {rest}" if rest else ""
        return (f"App nº {path[1] + 1}" + (f" «{name}»" if name else "") + suffix,
                f"App #{path[1] + 1}" + (f' "{name}"' if name else "") + suffix)
    plain = "/".join(str(p) for p in path) or "catalog.json"
    return plain, plain


FORMATS = {
    "id": ('tiene que ser "github:" + el repo, p. ej. "github:ps5-payload-dev/ftpsrv"',
           'must be "github:" + the repo, e.g. "github:ps5-payload-dev/ftpsrv"'),
    "repo": ('tiene que ser "autor/nombre-del-repo", p. ej. "ps5-payload-dev/ftpsrv"',
             'must be "owner/repo-name", e.g. "ps5-payload-dev/ftpsrv"'),
    "iconUrl": ("tiene que ser un enlace que empiece por https://", "must be a link starting with https://"),
}

TYPES = {
    "string": ("un texto entre comillas", "a text in quotes"),
    "array": ("una lista [ … ]", "a list [ … ]"),
    "object": ("un objeto { … }", "an object { … }"),
    "boolean": ("true o false", "true or false"),
}


def explain(error):
    """Qué está mal y cómo arreglarlo, en español y en inglés (jsonschema solo lo da en inglés)."""
    field = str(error.path[-1]) if error.path else ""
    kind = error.validator
    if kind == "required":
        missing = ", ".join(f'"{p}"' for p in error.validator_value if p not in error.instance)
        return f"falta el campo obligatorio {missing}", f"missing required field {missing}"
    if kind == "additionalProperties":
        extra = ", ".join(f'"{p}"' for p in error.instance if p not in error.schema.get("properties", {}))
        return f"campo desconocido {extra} (¿está mal escrito?)", f"unknown field {extra} (misspelled?)"
    if kind == "minLength":
        return "no puede estar vacío", "can't be empty"
    if kind == "maxLength":
        n = error.validator_value
        return f"es demasiado largo (máximo {n} caracteres)", f"is too long ({n} characters at most)"
    if kind == "pattern":
        return FORMATS.get(field, ("no tiene el formato correcto", "doesn't have the right format"))
    if kind == "oneOf":
        return ('tiene que ser un texto o { "es": "…", "en": "…" } (siempre con "es")',
                'must be a text or { "es": "…", "en": "…" } (always with "es")')
    if kind == "const":
        return f"tiene que ser {error.validator_value}", f"must be {error.validator_value}"
    if kind == "type":
        es, en = TYPES.get(error.validator_value, (str(error.validator_value),) * 2)
        return f"tiene que ser {es}", f"must be {en}"
    return error.message, error.message


def report(errors):
    print("❌ Hay que corregir catalog.json · catalog.json needs fixing:")
    for es, en in errors:
        print("   - " + es)
        print("     " + en)


if __name__ == "__main__":
    sys.exit(main())
