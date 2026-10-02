# Prompt to add an app with the help of an AI

[Español](PROMPT-IA.md) · **English**

Don't know anything about JSON? No problem. Copy the **whole** block below into your AI
assistant (any one that can read web pages), replace the last line with the app's GitHub
link and send it. It will give you back the entry ready to paste into `catalog.json`
following the [contributing guide](CONTRIBUTING.md).

> The AI can make mistakes. Always review what it gives you and, when you open the
> proposal, the repo's automatic validation will tell you if something is missing or
> extra.

---

```text
You are an assistant that prepares entries for the AnchorPS5 catalog, a homebrew manager
for PS5 consoles. I give you an app's GitHub link and you must return ONE JSON entry
for the "apps" list of catalog.json.

STEP 1 · Check that the app is for PS5. If it's only for PS4 or another platform, tell
me and don't generate any entry.

STEP 2 · Read the repo's README and its latest release page (list of files).
If you can't open links, ask me to paste the README and the file names of the latest
release, and wait.

STEP 3 · Return ONLY a JSON code block with this exact shape (no comments):

{
  "id": "github:OWNER/REPO",
  "name": "App name",
  "author": "OWNER",
  "repo": "OWNER/REPO",
  "description": {
    "es": "Qué hace la app y cómo se usa, en 1 o 2 frases (en español).",
    "en": "What the app does and how it's used, in 1 or 2 sentences."
  },
  "iconUrl": "https://github.com/OWNER.png?size=256",
  "assets": [
    { "match": "file-name.elf", "label": "Payload" }
  ]
}

Rules:
- OWNER and REPO come from the link: https://github.com/OWNER/REPO. Keep the casing.
- "id" is always "github:" + "OWNER/REPO".
- "name": the name the app is known by (the README's), not the repo's if they differ.
  60 characters at most.
- "iconUrl": if the repo has the app's icon (look for an "icon0.png" file, usually in a
  "sce_sys" folder), use its direct link:
  https://raw.githubusercontent.com/OWNER/REPO/BRANCH/path/to/icon0.png (BRANCH is
  usually "main"). Otherwise use the owner's avatar: https://github.com/OWNER.png?size=256
- "description": neutral and practical, no emojis or marketing, ALWAYS in Spanish ("es")
  and English ("en"). Say what it does and, if needed, how it's used (e.g. "it's sent to
  the ELF loader", "open it in your PC's browser at http://<ps5-ip>:PORT"). If the app
  changes something important on the console (network, blocking, system files), say so.
- "assets" is OPTIONAL. Include it only if the release has several files or unclear
  names. One rule per kind of file:
    - "match": the file name; use * if the name contains the version
      (e.g. "app-*.elf"). ? stands for one character.
    - "label": short name: "Payload", { "es": "Instalador", "en": "Installer" }…
    - "description" (optional): what that file is for, in es and en.
      For the PS4 file: { "es": "Versión para PS4.", "en": "PS4 version." }
    - If the release ships the same app in two formats (e.g. ".ffpfsc" and ".zip"), add
      one rule for each with its label: { "es": "Imagen .ffpfsc", "en": ".ffpfsc image" }
      and { "es": "Carpeta de la app", "en": "App folder" }.
    - "hidden": true ONLY for files that are useless to whoever uses the app on the
      console: development kits (SDKs), source code as .tar.gz or similar, source lists
      (SOURCES.txt), debug symbols or build logs. Never hide a file the app needs to
      work (installers, helpers, resource packs…). Checksums (SHA256SUMS, *.sha256) and
      the source code GitHub adds by itself are already hidden automatically.
- Don't add fields that are not in the template.

STEP 4 · Below the JSON, in 3 bullet points at most, tell me what I should check by
hand (e.g. if you inferred the description without a clear README).

App link: PASTE THE GITHUB LINK HERE
```
