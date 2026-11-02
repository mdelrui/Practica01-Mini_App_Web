<script setup lang="ts">
import axios from 'axios'
import { computed, ref } from 'vue'
import { useAuth, useClerk, UserButton } from '@clerk/vue'
import { FileDown, FilePlusCorner, MoveDown, Trash } from 'lucide-vue-next'
import { FileType, SummaryLength, summaryLengthLabels, type Summary, type UserInput } from './types/types'
import ToggleButton from './components/ToggleButton.vue'
import SelectionButton from './components/SelectionButton.vue'
import MainIdeaItem from './components/MainIdeaItem.vue'
import CopyButton from './components/CopyButton.vue'
import ConceptItem from './components/ConceptItem.vue'

const auth = useAuth()
const clerk = useClerk()

const API_URL = import.meta.env.VITE_API_URL ??
  (import.meta.env.DEV ? 'http://127.0.0.1:8000/resumir' : '/api/resumir')
const MAX_WORDS = 5000
const MAX_FILE_SIZE = 1024 * 1024
const ALLOWED_EXTENSIONS = ['.txt', '.md']

const text = ref('')
const loading = ref(false)
const APIResponse = ref<Summary | null>(null)
const copiedSummary = ref(false)
const copiedIdeas = ref(false)
const copiedGlossary = ref(false)
const isDragging = ref(false)
const fileError = ref('')
const reqError = ref<string | null>(null)
const reauthenticationRequired = ref(false)
const mainIdeasEnabled = ref(false)
const glosaryEnabled = ref(false)
const onDragEnter = ref(false)
const summaryLength = ref<SummaryLength>(SummaryLength.STANDARD)

const authReady = computed(() => auth.isLoaded.value === true)
const isSignedIn = computed(() => auth.isSignedIn.value === true)
const canSubmit = computed(() => authReady.value && isSignedIn.value)
const userTextWords = computed(() => {
  const trimmed = text.value.trim()
  return trimmed === '' ? 0 : trimmed.split(/\s+/).length
})
const summaryWords = computed(() => {
  if (!APIResponse.value?.summary)
    return 0

  const trimmed = APIResponse.value.summary.trim()
  return trimmed === '' ? 0 : trimmed.split(/\s+/).length
})

async function copySummary() {
  if (APIResponse.value?.summary) {
    try {
      const copiedText = 'RESUMEN\n' + APIResponse.value.summary

      await navigator.clipboard.writeText(copiedText)
      copiedSummary.value = true

      setTimeout(() => copiedSummary.value = false, 1000)
    } catch (error) {
      console.log('Error al copiar el resumen', error)
    }
  }
}

async function copyMainIdeas() {
  if (APIResponse.value?.mainIdeas) {
    try {
      const copiedText = [
        'IDEAS PRINCIPALES',
        ...APIResponse.value.mainIdeas.map((idea, i) => `${i + 1}. ${idea}`)
      ].join('\n')

      await navigator.clipboard.writeText(copiedText)
      copiedIdeas.value = true

      setTimeout(() => copiedIdeas.value = false, 1000)
    } catch (error) {
      console.log('Error al copiar las ideas', error)
    }
  }
}

async function copyGlossary() {
  if (APIResponse.value?.glossary) {
    try {
      const copiedText = [
        'GLOSARIO',
        ...APIResponse.value.glossary.map((idea) => `- ${idea.concept}: ${idea.definition}`)
      ].join('\n')

      await navigator.clipboard.writeText(copiedText)
      copiedGlossary.value = true

      setTimeout(() => copiedGlossary.value = false, 1000)
    } catch (error) {
      console.log('Error al copiar el glosario', error)
    }
  }
}

async function readFile(file: File) {
  fileError.value = ''

  const extension = file.name.slice(file.name.lastIndexOf('.')).toLowerCase()

  if (!ALLOWED_EXTENSIONS.includes(extension)) {
    fileError.value = 'Solo se admiten archivos .txt o .md'
    return
  }

  if (file.size > MAX_FILE_SIZE) {
    fileError.value = 'El archivo supera 1 MB'
    return
  }

  const content = await file.text()
  text.value = content.slice(0, MAX_WORDS)
}

async function openSignIn(): Promise<void> {
  if (!clerk?.value) {
    reqError.value = 'No se pudo abrir la autenticación. Inténtalo de nuevo.'
    return
  }

  try {
    reqError.value = null
    await clerk.value.openSignIn()
  } catch {
    reqError.value = 'No se pudo abrir la autenticación. Inténtalo de nuevo.'
  }
}

async function openSignUp(): Promise<void> {
  if (!clerk?.value) {
    reqError.value = 'No se pudo abrir la autenticación. Inténtalo de nuevo.'
    return
  }

  try {
    reqError.value = null
    await clerk.value.openSignUp()
  } catch {
    reqError.value = 'No se pudo abrir la autenticación. Inténtalo de nuevo.'
  }
}

async function signOut(): Promise<void> {
  if (!clerk?.value) return

  try {
    await clerk.value.signOut()
  } catch {
    reqError.value = 'No se pudo cerrar la sesión. Inténtalo de nuevo.'
  }
}

async function getSummary(): Promise<void> {
  if (!canSubmit.value) {
    reqError.value = 'Inicia sesión para poder resumir el texto.'
    return
  }

  loading.value = true
  reqError.value = null
  reauthenticationRequired.value = false
  APIResponse.value = null

  try {
    let token: string | null
    try {
      token = await auth.getToken.value()
    } catch {
      reqError.value = 'No se pudo obtener la sesión. Vuelve a iniciar sesión e inténtalo de nuevo.'
      reauthenticationRequired.value = true
      return
    }

    if (!token) {
      reqError.value = 'No se pudo obtener la sesión. Vuelve a iniciar sesión e inténtalo de nuevo.'
      reauthenticationRequired.value = true
      return
    }

    const userInput: UserInput = {
      text: text.value.trim().replace(/\n/g, ''),
      main_ideas: mainIdeasEnabled.value,
      glossary: glosaryEnabled.value,
      summary_length: summaryLength.value
    }
    const response = await axios.post(API_URL, userInput, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const payload = response.data ?? {}
    const data: Summary = {
      summary:
        typeof payload.summary === 'string'
          ? payload.summary
          : typeof payload.resumen === 'string'
            ? payload.resumen
            : '',
      mainIdeas: Array.isArray(payload.mainIdeas)
        ? payload.mainIdeas
        : Array.isArray(payload.main_ideas)
          ? payload.main_ideas
          : null,
      glossary: Array.isArray(payload.glossary) // TODO: Revisar que esté correcto
        ? payload.glossary
        : null
    }

    APIResponse.value = data
    deleteText()
  } catch (e) {
    if (axios.isAxiosError(e) && e.response?.status === 401) {
      reqError.value = 'Tu sesión no es válida o ha caducado. Vuelve a iniciar sesión.'
      reauthenticationRequired.value = true
    } else if (axios.isAxiosError(e) && e.response?.status === 503) {
      reqError.value = 'No se pudo verificar la sesión temporalmente. Inténtalo más tarde.'
    } else {
      reqError.value =
        'Ha ocurrido un error al contactar con el servicio. Por favor, inténtelo de nuevo.'
    }
    console.log(e)
  } finally {
    loading.value = false
  }
}

function selectSummaryLength(length: SummaryLength) {
  if (length !== summaryLength.value) {
    summaryLength.value = length
  }
}

function onDropFile(e: DragEvent) {
  isDragging.value = true
  onDragEnter.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) readFile(file)
}

function onDragLeaveFile(e: DragEvent) {
  const container = e.currentTarget as HTMLElement

  if (!container.contains(e.relatedTarget as Node)) {
    isDragging.value = false
    onDragEnter.value = false
  }
}

function deleteText() {
  text.value = ''
}

function prepareToTXT(): string {
  const sections: string[] = []

  if (APIResponse.value?.summary.trim()) {
    sections.push(`RESUMEN\n\n${APIResponse.value?.summary.trim()}`)
  }

  if (APIResponse.value?.mainIdeas) {
    const ideas = APIResponse.value?.mainIdeas
      .map((idea, index) => `${index + 1}. ${idea}`)
      .join('\n')

    sections.push(`IDEAS PRINCIPALES\n\n${ideas}`)
  }

  if (APIResponse.value?.glossary) {
    const terms = APIResponse.value?.glossary
      .map(({ concept, definition }) => `${concept}: ${definition}`)
      .join('\n\n')

    sections.push(`GLOSARIO DE TÉRMINOS\n\n${terms}`)
  }

  const content = sections.join('\n\n------------------------------\n\n')

  return content
}

function prepareToMD(): string {
  const sections: string[] = []

  if (APIResponse.value?.summary.trim()) {
    sections.push(`## RESUMEN\n\n${APIResponse.value?.summary.trim()}`)
  }

  if (APIResponse.value?.mainIdeas) {
    const ideas = APIResponse.value?.mainIdeas
      .map((idea, index) => `${index + 1}. ${idea}`)
      .join('\n')

    sections.push(`## IDEAS PRINCIPALES\n\n${ideas}`)
  }

  if (APIResponse.value?.glossary) {
    const terms = APIResponse.value?.glossary
      .map(({ concept, definition }) => `**${concept}:** ${definition}`)
      .join('\n\n')

    sections.push(`## GLOSARIO DE TÉRMINOS\n\n${terms}`)
  }

  const content = sections.join('\n\n')

  return content
}

function exportToFile(type: FileType) {
  switch (type) {
    case FileType.TXT: {
      const blob = new Blob([prepareToTXT()], {
        type: 'text/plain;charset=utf-8',
      })

      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')

      link.href = url
      link.download = `resumen_${getTimestamp()}.txt`
      link.click()

      URL.revokeObjectURL(url)
      return
    }
    case FileType.MD: {
      const blob = new Blob([prepareToMD()], {
        type: 'text/markdown;charset=utf-8',
      })

      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')

      link.href = url
      link.download = `resumen_${getTimestamp()}.md`
      link.click()

      URL.revokeObjectURL(url)
      return
    }
    default:
      return
  }
}

function getTimestamp(): string {
  const now = new Date()
  const timestamp = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, '0'),
    String(now.getDate()).padStart(2, '0')
  ].join('-') + '_' + [
    String(now.getHours()).padStart(2, '0'),
    String(now.getMinutes()).padStart(2, '0'),
  ].join('-')

  return timestamp
}
</script>

<template>
  <div class="min-h-screen bg-bg-primary flex flex-col items-center py-8 gap-10">
    <header class="flex justify-center w-full relative max-w-3xl px-10 md:px-0">
      <div>
        <h1 class="text-primary text-2xl font-semibold mb-2">RESUMIDOR AUTOMÁTICO</h1>
        <h3 class="text-on-primary/70">Convierte textos extensos en ideas claras.</h3>
      </div>

      <div class="absolute right-0 top-0">
        <UserButton v-if="isSignedIn" />
      </div>
    </header>

    <section v-if="!isSignedIn" class="flex justify-center gap-5 w-full max-w-3xl px-10 mt-10 md:px-0"
      aria-live="polite">
      <button type="button" @click="openSignIn"
        class="bg-primary text-bg-primary font-semibold text-lg py-3 px-10 rounded-sm cursor-pointer hover:bg-primary/70">
        Iniciar sesión
      </button>
      <button type="button" @click="openSignUp"
        class="bg-transparent text-primary border font-semibold border-primary text-lg py-3 px-10 rounded-sm cursor-pointer hover:bg-primary hover:text-bg-primary">
        Crear cuenta
      </button>
    </section>

    <div v-else class="w-full max-w-3xl px-10 m-auto md:px-0">
      <div class="flex justify-between pb-4 px-1">
        <div class="flex gap-2 items-center">
          <span
            class="flex justify-center items-center text-primary font-semibold text-sm px-4 py-0.5 tabular-nums">01</span>
          <p class="text-on-primary">Tu texto</p>
        </div>

        <button type="button" variant="ghost" size="icon" aria-label="Borrar texto" title="Borrar texto"
          v-on:click="deleteText()"
          class="rounded-full p-1.5 transition-colors text-on-primary/50 not-disabled:cursor-pointer hover:not-disabled:bg-red-400/10 hover:not-disabled:text-red-40 disabled:text-on-primary/20 disabled:cursor-not-allowed focus-visible:outline-2 focus-visible:outline-red-400"
          :disabled="text.length == 0">
          <Trash :size="16" />
        </button>
      </div>

      <form @submit.prevent="getSummary">
        <div @dragover.prevent="isDragging = true" @dragleave="onDragLeaveFile" @drop.prevent="onDropFile"
          @dragenter="onDragEnter = true" :class="isDragging"
          class="relative w-full mb-8 border border-[#e8f1f59f] rounded-lg bg-bg-secondary focus-within:border focus-within:border-primary focus-within:ring-1">
          <div v-if="onDragEnter"
            class="absolute size-full bg-white/20 flex flex-col justify-center rounded-lg items-center gap-2">
            <span class="text-on-primary">Suelta aquí tu archivo</span>

            <FilePlusCorner class="text-on-primary" />
          </div>

          <textarea class="text-on-primary w-full min-h-36 rounded-t-lg px-4 py-3 outline-none bg-transparent"
            placeholder="Escribe o pega tu texto aquí… o arrastra tu archivo (.md o .txt)" :maxlength="MAX_WORDS"
            v-model="text"></textarea>

          <div class="flex justify-between px-4 py-3 border-t border-[#e8f1f59f] gap-4">
            <span class="text-xs text-[#e8f1f593]">{{ userTextWords }} {{ userTextWords === 1 ? 'palabra' : 'palabras'
            }}</span>
            <span class="text-xs text-[#e8f1f593]">{{ text.length }} / {{ MAX_WORDS }}</span>
          </div>
        </div>

        <div class="flex justify-between mb-6 items-center">
          <div>
            <p class="text-sm text-on-primary/50">LONGITUD DEL RESUMEN</p>

            <div
              class="mt-2 p-1 border border-outline-primary rounded-lg bg-bg-secondary flex gap-2 justify-center items-center">
              <SelectionButton :length="SummaryLength.BRIEF" :is-active="summaryLength === SummaryLength.BRIEF"
                @select="selectSummaryLength($event)" />

              <SelectionButton :length="SummaryLength.STANDARD" :is-active="summaryLength === SummaryLength.STANDARD"
                @select="selectSummaryLength($event)" />

              <SelectionButton :length="SummaryLength.DETAILED" :is-active="summaryLength === SummaryLength.DETAILED"
                @select="selectSummaryLength($event)" />
            </div>
          </div>

          <div class="flex flex-col gap-4">
            <ToggleButton text="Extraer ideas principales" v-model:is-active="mainIdeasEnabled" />

            <ToggleButton text="Generar glosario de términos" v-model:is-active="glosaryEnabled" />
          </div>
        </div>

        <button type="submit"
          class="w-full flex justify-center items-center gap-4 py-3 rounded-lg border border-transparent font-semibold text-lg transition-all bg-primary text-bg-primary not-disabled:cursor-pointer hover:not-disabled:bg-[#55a2ac] hover:not-disabled:scale-[102%] disabled:bg-transparent disabled:text-on-primary/40 disabled:border-on-primary/25 disabled:cursor-not-allowed"
          :disabled="!text || loading || !canSubmit">
          <span>{{ loading ? 'Resumiendo...' : 'Resumir Texto' }}</span>
          <div v-if="loading" class="size-5 animate-spin rounded-full border-2 border-on-primary/30 border-t-on-primary"
            role="status" aria-label="Cargando"></div>
        </button>
      </form>

      <section aria-live="polite">
        <div class="flex justify-evenly items-center my-8">
          <div class="flex flex-1 justify-evenly items-center gap-2">
            <div class="flex-1 border-t border-primary/50"></div>

            <MoveDown class="text-primary" />
          </div>

          <p class="flex-1 text-sm text-on-primary text-center">Tu resumen aparecerá aquí debajo</p>

          <div class="flex flex-1 justify-evenly items-center gap-2">
            <MoveDown class="text-primary" />

            <div class="flex-1 border-t border-primary/50"></div>
          </div>
        </div>

        <!-- RESUMEN -->

        <div v-if="APIResponse && APIResponse.summary">
          <div class="flex justify-between items-center mb-4">
            <div class="flex gap-2">
              <span class="py-1 px-3 bg-bg-secondary border border-on-primary/20 text-xs text-on-primary rounded-full">
                Resumen {{ summaryLengthLabels[summaryLength].toLowerCase() }}
              </span>

              <span class="py-1 px-3 bg-bg-secondary border border-on-primary/20 text-xs text-on-primary rounded-full">
                {{ summaryWords }} palabras
              </span>
            </div>

            <div class="flex gap-3 items-center">
              <span class="text-on-primary/60 text-sm">Exportar todo</span>

              <button type="button" @click="exportToFile(FileType.TXT)"
                class="flex justify-evenly items-center h-11 w-20 text-on-primary bg-bg-secondary border border-on-primary/20 rounded-lg cursor-pointer hover:bg-primary hover:text-bg-primary">
                <FileDown :size="20" />

                <span class="text-sm font-semibold">.txt</span>
              </button>

              <button type="button" @click="exportToFile(FileType.MD)"
                class="flex justify-evenly items-center h-11 w-20 text-on-primary bg-bg-secondary border border-on-primary/20 rounded-lg cursor-pointer hover:bg-primary hover:text-bg-primary">
                <FileDown :size="20" />

                <span class="text-sm font-semibold">.md</span>
              </button>
            </div>
          </div>

          <div class="bg-bg-secondary border border-on-primary/50 rounded-lg p-4 mb-6">
            <div class="flex justify-between items-center mb-3">
              <h2 class="text-lg font-semibold text-primary">RESUMEN</h2>

              <CopyButton :copied="copiedSummary" @copy="copySummary" />
            </div>

            <p class="text-on-primary leading-relaxed whitespace-pre-line">
              {{ APIResponse.summary }}
            </p>
          </div>
        </div>

        <!-- IDEAS PRINCIPALES -->

        <div v-if="APIResponse && APIResponse.mainIdeas"
          class="bg-bg-secondary border border-on-primary/50 rounded-lg p-4 ps-8 mb-6">
          <div class="flex justify-between items-center mb-3">
            <h2 class="text-lg font-semibold text-primary">IDEAS PRINCIPALES</h2>

            <CopyButton :copied="copiedIdeas" @copy="copyMainIdeas" />
          </div>

          <MainIdeaItem v-for="idea, i in APIResponse.mainIdeas" :num="i + 1" :text="idea" />
        </div>

        <!-- GLOSARIO DE CONCEPTOS -->

        <div v-if="APIResponse && APIResponse.glossary"
          class="bg-bg-secondary border border-on-primary/50 rounded-lg p-4 ps-8">
          <div class="flex justify-between items-center mb-3">
            <h2 class="text-lg font-semibold text-primary">GLOSARIO</h2>

            <CopyButton :copied="copiedGlossary" @copy="copyGlossary" />
          </div>

          <ConceptItem v-for="concept in APIResponse.glossary" :concept="concept" />
        </div>

        <!-- MENSAJES DE ERROR -->

        <div v-if="reqError" class="bg-[#ff7979]/20 border border-[#ff9292] rounded-lg p-4">
          <p class="text-[#cc4f4f] font-semibold leading-relaxed whitespace-pre-line">
            {{ reqError }}
          </p>
          <button v-if="reauthenticationRequired" type="button" @click="openSignIn" class="mt-3 text-primary underline">
            Volver a iniciar sesión
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped></style>