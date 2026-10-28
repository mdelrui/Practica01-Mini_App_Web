<script setup lang="ts">
import { resumirTexto } from './services/resumen'
import { computed, ref } from 'vue'
import { FilePlusCorner, MoveDown, Trash } from '@lucide/vue'

const MAX_CHARS = 5000
const MAX_FILE_SIZE = 1024 * 1024
const ALLOWED_EXTENSIONS = ['.txt', '.md']

const text = ref('')
const loading = ref(false)
const summary = ref<string | null>(null)
const isDragging = ref(false)
const fileError = ref('')
const reqError = ref<string | null>(null)

const words = computed(() => {
  const trimmed = text.value.trim()
  return trimmed === '' ? 0 : trimmed.split(/\s+/).length
})

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

  try {
    const content = await file.text()
    text.value = content.slice(0, MAX_CHARS)
  } catch {
    fileError.value = 'No se pudo leer el archivo'
  }
}

function onDropFile(e: DragEvent) {
  isDragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) readFile(file)
}

function onDragLeaveFile(e: DragEvent) {
  const container = e.currentTarget as HTMLElement

  if (!container.contains(e.relatedTarget as Node)) {
    isDragging.value = false
  }
}

function deleteText() {
  text.value = ''
}

async function getSummary() {
  // No enviamos el formulario si el texto está vacío o ya se está procesando.
  if (!text.value.trim() || loading.value) return

  loading.value = true
  summary.value = null
  try {
    // Enviamos el texto a Python y guardamos el resumen
    summary.value = await resumirTexto(text.value)
  } catch {
    // Mostramos un mensaje sencillo si ocurre un error.
    summary.value = 'No se pudo generar el resumen. Comprueba la conexión e inténtalo de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-bg-primary flex flex-col items-center py-8 gap-10">
    <header>
      <h1 class="text-primary text-2xl font-semibold mb-2">RESUMIDOR AUTOMÁTICO</h1>
      <h3 class="text-on-primary/80">Convierte textos extensos en ideas claras.</h3>
    </header>

    <div class="w-full max-w-3xl flex-col justify-center items-center px-10 md:px-0">
      <div class="flex justify-between pb-4 px-1">
        <div class="flex gap-2 items-center">
          <span
            class="flex justify-center items-center text-primary font-semibold text-sm px-4 py-0.5 tabular-nums">01</span>
          <p class="text-on-primary">Tu texto</p>
        </div>

        <button type="button" aria-label="Borrar texto" title="Borrar texto" @click="deleteText"
          class="rounded-full p-1.5 transition-colors text-[#e8f1f5]/50 not-disabled:cursor-pointer hover:not-disabled:bg-red-400/10 hover:not-disabled:text-red-40 disabled:text-[#e8f1f5]/20 disabled:cursor-not-allowed focus-visible:outline-2 focus-visible:outline-red-400"
          :disabled="text.length === 0">
          <Trash :size="16" />
        </button>
      </div>

      <form @submit.prevent="getSummary">
        <div @dragover.prevent="isDragging = true" @dragleave="onDragLeaveFile" @drop.prevent="onDropFile"
          @dragenter="isDragging = true" :class="{ 'border-[#67C4D0]': isDragging }"
          class="relative w-full mb-4 border border-[#e8f1f59f] rounded-lg bg-[#263746] focus-within:border focus-within:border-[#67C4D0] focus-within:ring-1">
          <div v-if="isDragging"
            class="absolute size-full bg-white/20 flex flex-col justify-center rounded-lg items-center gap-2">
            <span class="text-on-primary">Suelta aquí tu archivo</span>
            <FilePlusCorner class="text-on-primary" />
          </div>

          <textarea class="text-on-primary w-full min-h-36 rounded-t-lg px-4 py-3 outline-none bg-transparent"
            placeholder="Escribe o pega tu texto aquí… o arrastra tu archivo (.md o .txt)" :maxlength="MAX_CHARS"
            v-model="text"></textarea>

          <div class="flex justify-between px-4 py-3 border-t border-on-primary/60">
            <span class="text-xs text-on-primary/60">{{ words }} {{ words === 1 ? 'palabra' : 'palabras' }}</span>
            <span class="text-xs text-[#e8f1f593]">{{ text.length }} / {{ MAX_CHARS }} caracteres</span>
          </div>
        </div>

        <p v-if="fileError" class="mb-3 text-sm text-red-300" role="alert">{{ fileError }}</p>

        <button type="submit"
          class="w-full flex justify-center items-center gap-4 py-3 rounded-lg border border-transparent font-semibold text-lg transition-all bg-primary text-bg-primary not-disabled:cursor-pointer hover:not-disabled:bg-[#55a2ac] hover:not-disabled:scale-[102%] disabled:bg-transparent disabled:text-on-primary/40 disabled:border-on-primary/25 disabled:cursor-not-allowed"
          :disabled="!text || loading">
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
        <!-- <h2 class="text-sm font-semibold text-[#e8f1f5] mb-3">Resumen</h2> -->

        <p v-if="loading" class="text-sm font-semibold text-on-primary/60">Generando resumen…</p>

        <div v-else-if="summary" class="bg-bg-secondary border border-on-primary/50 rounded-lg p-4">
          <p class="text-on-primary leading-relaxed whitespace-pre-line">
            {{ summary }}
          </p>
        </div>

        <div v-if="reqError" class="bg-[#ff7979]/20 border border-[#ff9292] rounded-lg p-4">
          <p class="text-[#cc4f4f] font-semibold leading-relaxed whitespace-pre-line">
            {{ reqError }}
          </p>
        </div>
      </section>
    </div>
  </div>
</template>
