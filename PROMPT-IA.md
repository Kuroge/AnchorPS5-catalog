# Prompt para añadir una app con ayuda de una IA

**Español** · [English](AI-PROMPT.md)

¿No sabes nada de JSON? No pasa nada. Copia **todo** el bloque de abajo en tu asistente
de IA (cualquiera que pueda leer páginas web), cambia la última línea por el enlace de
GitHub de la app y envíalo. Te devolverá la entrada lista para pegar en `catalog.json`
siguiendo la [guía para contribuir](CONTRIBUIR.md).

> La IA puede equivocarse. Revisa siempre lo que te da y, al abrir la propuesta, la
> comprobación automática del repo te dirá si falta o sobra algo.

---

```text
Eres un asistente que prepara entradas para el catálogo de AnchorPS5, un gestor de
homebrew para consolas PS5. Te paso el enlace de GitHub de una app y tienes que
devolver UNA entrada JSON para la lista "apps" de catalog.json.

PASO 1 · Comprueba que la app es para PS5. Si solo es para PS4 u otra plataforma,
dímelo y no generes ninguna entrada.

PASO 2 · Lee el README del repo y la página de su última release (lista de ficheros).
Si no puedes abrir enlaces, pídeme que te pegue el README y los nombres de los ficheros
de la última release, y espera.

PASO 3 · Devuelve SOLO un bloque de código JSON con esta forma exacta (sin comentarios):

{
  "id": "github:AUTOR/REPO",
  "name": "Nombre de la app",
  "author": "AUTOR",
  "repo": "AUTOR/REPO",
  "description": {
    "es": "Qué hace la app y cómo se usa, en 1 o 2 frases.",
    "en": "The same in English, 1 or 2 sentences."
  },
  "iconUrl": "https://github.com/AUTOR.png?size=256",
  "assets": [
    { "match": "nombre-del-fichero.elf", "label": "Payload" }
  ]
}

Reglas:
- AUTOR y REPO salen del enlace: https://github.com/AUTOR/REPO. Respeta mayúsculas.
- "id" es siempre "github:" + "AUTOR/REPO".
- "name": el nombre con el que se conoce la app (el del README), no el del repo si son
  distintos. Máximo 60 caracteres.
- "description": neutra y práctica, sin emojis ni marketing, SIEMPRE en español ("es")
  e inglés ("en"). Di qué hace y, si hace
  falta, cómo se usa (p. ej. "se envía al ELF loader", "se abre en el navegador del PC en
  http://<ip-de-la-ps5>:PUERTO"). Si la app cambia algo importante de la consola (red,
  bloqueos, ficheros del sistema), dilo.
- "assets" es OPCIONAL. Inclúyelo solo si la release tiene varios ficheros o nombres
  poco claros. Una regla por tipo de fichero:
    - "match": el nombre del fichero; usa * si el nombre lleva la versión
      (p. ej. "app-*.elf"). ? vale por un carácter.
    - "label": nombre corto: "Payload", { "es": "Instalador", "en": "Installer" }…
    - "description" (opcional): para qué sirve ese fichero, en es y en.
      Para el fichero de PS4: { "es": "Versión para PS4.", "en": "PS4 version." }
    - "hidden": true para ocultar ficheros que no sirven al usuario (símbolos de
      depuración, etc.). El código fuente ya se oculta solo; no hace falta.
- No añadas campos que no estén en la plantilla.

PASO 4 · Debajo del JSON, en 3 viñetas como máximo, dime qué conviene que revise a mano
(p. ej. si la descripción la has deducido sin README claro).

Enlace de la app: PEGA AQUÍ EL ENLACE DE GITHUB
```
