"""
Genera releases.json: las últimas releases de cada app del catálogo, con sus ficheros,
tamaños y SHA-256. La app descarga este único fichero en vez de preguntar a GitHub app
por app, así que no gasta el límite de consultas de quien la usa.

Generates releases.json: the latest releases of every catalog app, with their files,
sizes and SHA-256. The app downloads this single file instead of asking GitHub app by
app, so it doesn't use up its users' request limit.

Uso · Usage: python scripts/indice.py   (con GITHUB_TOKEN · with GITHUB_TOKEN)
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PER_REPO = 20  # las mismas que pide la app a la API · same as the app asks the API for
RELEASE_FIELDS = ("tag_name", "name", "draft", "prerelease", "published_at", "html_url")
ASSET_FIELDS = ("name", "size", "browser_download_url", "digest")


def github(path):
    request = urllib.request.Request("https://api.github.com/" + path, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with open(os.path.join(ROOT, "catalog.json"), encoding="utf-8") as f:
        catalog = json.load(f)

    output = os.path.join(ROOT, "releases.json")
    previous = {}
    if os.path.exists(output):
        with open(output, encoding="utf-8") as f:
            previous = json.load(f).get("repos", {})

    repos, failed = {}, []
    for repo in sorted({app["repo"] for app in catalog["apps"] if app.get("repo")}, key=str.lower):
        try:
            releases = github(f"repos/{repo}/releases?per_page={PER_REPO}")
        except (urllib.error.URLError, TimeoutError) as error:
            # Si GitHub falla con un repo, se conserva lo de la última vez · keep last data on failure.
            failed.append(f"{repo}: {error}")
            if repo in previous:
                repos[repo] = previous[repo]
            continue

        repos[repo] = [
            {**{k: r.get(k) for k in RELEASE_FIELDS},
             "assets": [{k: a.get(k) for k in ASSET_FIELDS} for a in r.get("assets", [])]}
            for r in releases
            if not r.get("draft")
        ]

    # Solo cambia la fecha si cambia el contenido: sin commits vacíos cada hora.
    # The date only changes if the content does: no empty commits every hour.
    if repos == previous and os.path.exists(output):
        print(f"Sin cambios · No changes ({len(repos)} repos).")
    else:
        index = {
            "schemaVersion": 1,
            "generatedAt": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
            "repos": repos,
        }
        with open(output, "w", encoding="utf-8", newline="\n") as f:
            json.dump(index, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print(f"releases.json actualizado · updated ({len(repos)} repos).")

    for line in failed:
        print("⚠️ " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
