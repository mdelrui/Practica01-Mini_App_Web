export interface GlossaryConcept {
  concept: string
  definition: string
}

export interface Summary {
  summary: string
  mainIdeas: string[] | null
  glossary: GlossaryConcept[] | null
}

export interface UserInput {
  text: string
  main_ideas: boolean
  glossary: boolean
  summary_length: SummaryLength
}

export enum SummaryLength {
  BRIEF = 'breve',
  STANDARD = 'estándar',
  DETAILED = 'detallado',
}

export const summaryLengthLabels: Record<SummaryLength, string> = {
  [SummaryLength.BRIEF]: 'breve',
  [SummaryLength.STANDARD]: 'estándar',
  [SummaryLength.DETAILED]: 'detallado',
}

export enum FileType {
  TXT,
  MD,
}
