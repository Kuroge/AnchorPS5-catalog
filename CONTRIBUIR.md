# Cómo proponer una app

**Español** · [English](CONTRIBUTING.md)

Hay dos formas. **Las dos se hacen desde la web de GitHub**; no hace falta instalar nada
ni saber programar. Solo necesitas una cuenta de GitHub (gratis).

| | Para quién | Qué haces tú |
|---|---|---|
| **A. Pedirla** | Si solo quieres sugerirla | Rellenas un formulario con el enlace |
| **B. Añadirla tú** | Si te animas a editar el catálogo | Pegas la entrada en `catalog.json` |

Las propuestas se revisan a mano antes de añadirlas.

---

## A. Pedir una app (lo más fácil)

1. Entra en la pestaña **Issues** de este repo y pulsa **New issue**.
2. Elige **Proponer una app**.
3. Pega el enlace de GitHub de la app, marca las casillas y pulsa **Create**.

Ya está: la revisaremos y, si encaja, la añadiremos nosotros.

---

## B. Añadirla tú

### 1. Prepara la entrada

Usa el [prompt para IA](PROMPT-IA.md): copias el texto en tu asistente de IA, pegas el
enlace de la app y te devuelve un bloque como este:

```json
{
  "id": "github:autor/mi-app",
  "name": "Mi App",
  "author": "autor",
  "repo": "autor/mi-app",
  "description": {
    "es": "Qué hace la app.",
    "en": "What the app does."
  },
  "iconUrl": "https://github.com/autor.png?size=256"
}
```

### 2. Edita el catálogo en la web

1. Abre el fichero [`catalog.json`](catalog.json) de este repo.
2. Pulsa el **lápiz** (✏️ *Edit this file*), arriba a la derecha. GitHub hará una copia
   del repo en tu cuenta automáticamente (te lo dirá con un aviso; es normal).
3. Baja hasta la **última app** de la lista. Termina en `}` y justo debajo hay un `]`.
4. Escribe una **coma** justo después de esa `}` y pega tu bloque debajo:

```text
    {
      "id": "github:...última app que ya estaba...",
      ...
    },            <- 1) añade esta coma
    {             <- 2) pega aquí tu bloque
      "id": "github:autor/mi-app",
      ...
    }             <- tu bloque termina SIN coma
  ]
}
```

> Edita solo `catalog.json`. El fichero `releases.json` se genera solo, varias veces al día: no lo
> toques; en cuanto tu app entre en el catálogo, aparecerá en él.

### 3. Envía la propuesta

1. Pulsa **Commit changes…** y escribe un título corto, p. ej. `Añadir Mi App`.
2. Pulsa **Propose changes** y en la siguiente pantalla **Create pull request** (dos veces).

### 4. Mira la comprobación automática

En tu propuesta aparecerá **Validar catálogo**:

- ✅ **Verde:** el formato es correcto. Solo queda la revisión a mano.
- ❌ **Rojo:** pulsa **Details** y verás la lista de cosas que corregir, por ejemplo:
  - `App nº 7 «Mi App»: falta el campo obligatorio "author"`
  - `catalog.json no es un JSON válido (línea 80…)` → casi siempre es una **coma**
    que sobra o falta.

  Para corregir, vuelve a la pestaña **Files changed**, pulsa los tres puntos (`…`) del
  fichero → **Edit file**, arregla y guarda. La comprobación se repite sola.

---

## Errores típicos

| Mensaje | Qué pasa |
|---|---|
| `no es un JSON válido` | Falta o sobra una coma, o unas comillas sin cerrar. |
| `campo desconocido "descripcion"` | Un nombre de campo mal escrito (es `description`). |
| `el id debe ser "github:…"` | El `id` tiene que ser `github:` + el `repo`, igual. |
| `el repo … no existe o es privado` | El enlace está mal copiado o el repo no es público. |
| `no tiene ninguna release publicada` | La app aún no publica ficheros descargables. |
| `el id … ya está en …` | Esa app ya está en el catálogo. |
