# How to propose an app

[Español](CONTRIBUIR.md) · **English**

There are two ways. **Both are done from the GitHub website**; you don't need to install
anything or know how to code. You only need a (free) GitHub account.

| | For whom | What you do |
|---|---|---|
| **A. Request it** | If you just want to suggest it | Fill in a form with the link |
| **B. Add it yourself** | If you feel like editing the catalog | Paste the entry into `catalog.json` |

First of all: **only PS5 homebrew for consoles already in homebrew mode is accepted**.
No exploits or jailbreak tools, nothing related to piracy or to bypassing DRM, licenses
or accounts. Proposals are reviewed by hand.

---

## A. Request an app (the easiest way)

1. Go to the **Issues** tab of this repo and click **New issue**.
2. Choose **Propose an app**.
3. Paste the app's GitHub link, tick the boxes and click **Create**.

That's it: we'll review it and, if it fits, add it ourselves.

---

## B. Add it yourself

### 1. Prepare the entry

Use the [AI prompt](AI-PROMPT.md): copy the text into your AI assistant, paste the app's
link and it will give you back a block like this one:

```json
{
  "id": "github:owner/my-app",
  "name": "My App",
  "author": "owner",
  "repo": "owner/my-app",
  "description": {
    "es": "Qué hace la app.",
    "en": "What the app does."
  },
  "iconUrl": "https://github.com/owner.png?size=256"
}
```

### 2. Edit the catalog on the website

1. Open this repo's [`catalog.json`](catalog.json) file.
2. Click the **pencil** (✏️ *Edit this file*) at the top right. GitHub will automatically
   make a copy of the repo in your account (it tells you with a notice; that's normal).
3. Scroll down to the **last app** in the list. It ends with `}` and right below there
   is a `]`.
4. Type a **comma** right after that `}` and paste your block below it:

```text
    {
      "id": "github:...last app that was already there...",
      ...
    },            <- 1) add this comma
    {             <- 2) paste your block here
      "id": "github:owner/my-app",
      ...
    }             <- your block ends WITHOUT a comma
  ]
}
```

### 3. Send the proposal

1. Click **Commit changes…** and write a short title, e.g. `Add My App`.
2. Click **Propose changes** and on the next screen **Create pull request** (twice).

### 4. Check the automatic validation

Your proposal will show **Validate catalog**:

- ✅ **Green:** the format is correct. Only the manual review is left.
- ❌ **Red:** click **Details** to see the list of things to fix, for example:
  - `App #7 "My App": missing required field "author"`
  - `catalog.json is not valid JSON (line 80…)` → it's almost always a **comma** too
    many or missing.

  To fix it, go back to the **Files changed** tab, click the three dots (`…`) of the
  file → **Edit file**, fix it and save. The validation runs again by itself.

---

## Common errors

| Message | What's wrong |
|---|---|
| `is not valid JSON` | A comma is missing or extra, or some quotes are not closed. |
| `unknown field "descripcion"` | A misspelled field name (it's `description`). |
| `the id must be "github:…"` | The `id` must be `github:` + the `repo`, exactly. |
| `the repo … doesn't exist or is private` | The link was copied wrong or the repo isn't public. |
| `has no published release` | The app doesn't publish downloadable files yet. |
| `the id … is already in …` | That app is already in the catalog. |
