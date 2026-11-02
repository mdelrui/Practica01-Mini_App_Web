from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

MAX_CHARS = 5000

class GlossaryConcept(BaseModel):
    concept: str
    definition: str

# ---------- Esquema de la salida de la IA ----------
class ResumenResponse(BaseModel):
    summary: str
    main_ideas: list[str] | None = None
    glossary: list[GlossaryConcept] | None = None

class SummaryLength(str, Enum):
    BRIEF = 'breve'
    STANDARD = 'estándar'
    DETAILED = 'detallado'

class UserInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(min_length=1, max_length=MAX_CHARS)
    main_ideas: bool = False
    glossary: bool = False
    summary_length: SummaryLength = SummaryLength.STANDARD