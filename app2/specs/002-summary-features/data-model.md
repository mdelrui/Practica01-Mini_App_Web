# Data model: Resumen y salida del documento

## Domain entities

### 1) UserInput

Represents the payload sent by the frontend to the backend when the user submits the form.

| Field            | Type            | Required | Validation rules                                           | Notes                                                              |
| ---------------- | --------------- | -------- | ---------------------------------------------------------- | ------------------------------------------------------------------ |
| `text`           | `string`        | Yes      | `min_length=1`, `max_length=5000`, trimmed by model config | Main source text loaded manually or from a local `.txt`/`.md` file |
| `main_ideas`     | `boolean`       | No       | Defaults to `false`                                        | Requests extraction of main ideas                                  |
| `glossary`       | `boolean`       | No       | Defaults to `false`                                        | Requests generation of glossary                                    |
| `summary_length` | `SummaryLength` | No       | Enum values: `breve`, `estándar`, `detallado`              | Used in prompt construction and response labeling                  |

**State notes**:

- The value is validated in `backend/models.py`.
- The frontend serializes it as `summary_length`, `main_ideas`, and `glossary`.
- It is not persisted beyond the request lifecycle.

### 2) SummaryLength

Enum values used by the backend prompt generation and by the frontend UI selectors.

```python
class SummaryLength(str, Enum):
    BRIEF = 'breve'
    STANDARD = 'estándar'
    DETAILED = 'detallado'
```

**Validation rules**:

- Only valid enum values are accepted.
- The frontend’s labels render exactly these values as the chosen summary length.

### 3) GlossaryConcept

Represents each glossary term in the result.

| Field        | Type     | Required | Validation rules           |
| ------------ | -------- | -------- | -------------------------- |
| `concept`    | `string` | Yes      | Must be a non-empty string |
| `definition` | `string` | Yes      | Must be a non-empty string |

### 4) ResumenResponse

The structured result returned by the backend after a valid authenticated call to OpenRouter.

| Field        | Type                    | Required | Validation rules                         |
| ------------ | ----------------------- | -------- | ---------------------------------------- |
| `summary`    | `string`                | Yes      | Must be a non-empty string               |
| `main_ideas` | `list[str]`             | No       | Optional list of concepts, may be `null` |
| `glossary`   | `list[GlossaryConcept]` | No       | Optional list of terms, may be `null`    |

**Behavior**:

- `main_ideas` is set to `None` when the request did not ask for it.
- The backend validates the JSON returned by OpenRouter before returning it.
- The frontend maps `mainIdeas` and `glossary` into the UI sections.

### 5) Frontend view model

The browser-side view model is defined in `frontend/src/types/types.ts`.

```ts
export interface Summary {
	summary: string;
	mainIdeas: string[] | null;
	glossary: GlossaryConcept[] | null;
}
```

**Relationship**:

- Frontend calls `axios.post` with `UserInput`.
- Backend returns `ResumenResponse`.
- Frontend transforms it to a `Summary` view model for rendering, copying, and export.

## Validation and rules

- `text` is required and must be <= 5000 characters.
- File upload is client-side only; the file is read by the browser and its text is inserted into the form, not sent as a file.
- Summary length must match one of the enum values.
- `main_ideas` and `glossary` are booleans; the backend interprets them as request flags.
- Invalid provider responses are rejected with a controlled 502+ error path.

## State transitions

1. Idle form: the user has not submitted the request.
2. Valid request: user enters text and selected options, session is valid, request is sent.
3. Response OK: summary is rendered in the screen and optional blocks appear.
4. Error state: 401/503/502/504 leads to a visible message and no further processing.

## Notes

The current implementation deliberately avoids persistence, database, and multi-screen navigation. The model and rules are intentionally minimal and aligned with the feature scope defined in the constitution.
