<script setup lang="ts">
import axios from 'axios'
import { computed, ref } from 'vue'
import { FilePlusCorner, MoveDown, Trash } from 'lucide-vue-next'

const URL = 'http://127.0.0.1/nombre_endpoint' // nombre_endpoint sustituir por el nombre adecuadao
const MAX_WORDS = 5000
const MAX_FILE_SIZE = 1024 * 1024
const ALLOWED_EXTENSIONS = ['.txt', '.md']

const text = ref('')
const loading = ref(false)
const summary = ref<string | null>(null)
const isDragging = ref(false)
const fileError = ref('')

const words = computed(() => {
  const trimmed = text.value.trim()
  return trimmed === '' ? 0 : trimmed.split(/\s+/).length
})
const onDragEnter = ref(false)

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

function getSummary() {
  loading.value = true

  setTimeout(() => {
    loading.value = false
    deleteText()
    summary.value = `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vestibulum faucibus magna, at gravida mauris bibendum non. Pellentesque gravida sollicitudin odio vitae fermentum. Pellentesque tempus orci accumsan, efficitur nulla eget, tempus sapien. Pellentesque sed urna metus. Sed rhoncus eu metus ut iaculis. In varius orci non sem gravida bibendum. Vivamus lacinia risus quis augue dignissim, non sodales orci bibendum.

  Cras aliquet mauris urna, eu aliquam ex lacinia eget. Pellentesque consectetur purus at tellus vulputate ornare. Maecenas blandit pharetra dictum. Aenean dapibus, arcu aliquam fringilla placerat, nibh magna euismod leo, quis sagittis sem ipsum ut mauris. Maecenas ullamcorper congue sapien, sed cursus nunc iaculis et. Curabitur tincidunt sodales augue, id facilisis sapien congue quis. Nam vel porttitor libero. Sed sit amet velit orci. Nulla pellentesque mi a nunc auctor scelerisque. Quisque eu dolor pellentesque, rutrum orci malesuada, iaculis eros. Sed tempus eros a mi lobortis, at sagittis purus ultricies. Curabitur nec velit augue.`
  }, 2000)
}

async function connectToAPI(): Promise<void> {
  return await axios.post(URL, text) // Terminar y agregar lo necesario
}
</script>
<!-- Fondo #17212B · Panel #263746 · Acento #67C4D0 · Texto #E8F1F5 -->
<template>
  <div class="min-h-screen bg-[#17212B] flex flex-col items-center py-8 gap-10">
    <header>
      <h1 class="text-[#67C4D0] text-2xl font-semibold mb-2">RESUMIDOR AUTOMÁTICO</h1>
      <h3 class="text-[#e8f1f5c5]">Convierte textos extensos en ideas claras.</h3>
    </header>

    <div class="w-full max-w-3xl flex-col justify-center items-center px-10 md:px-0">
      <div class="flex justify-between pb-4 px-1">
        <div class="flex gap-2 items-center">
          <span
            class="flex justify-center items-center text-[#67C4D0] font-semibold text-sm px-4 py-0.5 tabular-nums"
            >01</span
          >
          <p class="text-[#e8f1f5]">Tu texto</p>
        </div>

        <button
          type="button"
          variant="ghost"
          size="icon"
          aria-label="Borrar texto"
          title="Borrar texto"
          v-on:click="deleteText()"
          class="rounded-full p-1.5 transition-colors text-[#e8f1f5]/50 not-disabled:cursor-pointer hover:not-disabled:bg-red-400/10 hover:not-disabled:text-red-40 disabled:text-[#e8f1f5]/20 disabled:cursor-not-allowed focus-visible:outline-2 focus-visible:outline-red-400"
          :disabled="text.length == 0"
        >
          <Trash :size="16" />
        </button>
      </div>

      <form>
        <div
          @dragover.prevent="isDragging = true"
          @dragleave="onDragLeaveFile"
          @drop.prevent="onDropFile"
          @dragenter="onDragEnter = true"
          :class="isDragging"
          class="relative w-full mb-4 border border-[#e8f1f59f] rounded-lg bg-[#263746] focus-within:border focus-within:border-[#67C4D0] focus-within:ring-1"
        >
          <div
            v-if="onDragEnter"
            class="absolute size-full bg-white/20 flex flex-col justify-center rounded-lg items-center gap-2"
          >
            <span class="text-[#E8F1F5]">Suelta aquí tu archivo</span>

            <FilePlusCorner class="text-[#E8F1F5]" />
          </div>

          <textarea
            class="text-[#e8f1f5] w-full min-h-36 rounded-t-lg px-4 py-3 outline-none bg-transparent"
            placeholder="Escribe o pega tu texto aquí… o arrastra tu archivo (.md o .txt)"
            :maxlength="MAX_WORDS"
            v-model="text"
          ></textarea>

          <div class="flex justify-between px-4 py-3 border-t border-[#e8f1f59f]">
            <span class="text-xs text-[#e8f1f593]"
              >{{ words }} {{ words === 1 ? 'palabra' : 'palabras' }}</span
            >
            <span class="text-xs text-[#e8f1f593]">{{ text.length }} / {{ MAX_WORDS }}</span>
          </div>
        </div>

        <button
          type="submit"
          class="w-full flex justify-center items-center gap-4 py-3 rounded-lg border border-transparent font-semibold text-lg transition-all bg-[#67C4D0] text-[#17212B] not-disabled:cursor-pointer hover:not-disabled:bg-[#55a2ac] hover:not-disabled:scale-[102%] disabled:bg-transparent disabled:text-[#e8f1f5]/40 disabled:border-[#e8f1f5]/25 disabled:cursor-not-allowed"
          :disabled="!text || loading"
          v-on:click="getSummary()"
        >
          <span>{{ loading ? 'Resumiendo...' : 'Resumir Texto' }}</span>
          <div
            v-if="loading"
            class="size-5 animate-spin rounded-full border-2 border-[#e8f1f5]/30 border-t-[#e8f1f5]"
            role="status"
            aria-label="Cargando"
          ></div>
        </button>
      </form>

      <section aria-live="polite">
        <div class="flex justify-evenly items-center my-8">
          <div class="flex flex-1 justify-evenly items-center gap-2">
            <div class="flex-1 border-t border-[#67C4D0]/50"></div>

            <MoveDown class="text-[#67C4D0]" />
          </div>

          <p class="flex-1 text-sm text-[#e8f1f5] text-center">Tu resumen aparecerá aquí debajo</p>

          <div class="flex flex-1 justify-evenly items-center gap-2">
            <MoveDown class="text-[#67C4D0]" />

            <div class="flex-1 border-t border-[#67C4D0]/50"></div>
          </div>
        </div>
        <!-- <h2 class="text-sm font-semibold text-[#e8f1f5] mb-3">Resumen</h2> -->

        <p v-if="loading" class="text-sm font-semibold text-[#e8f1f5]/60">Generando resumen…</p>

        <div v-else-if="summary" class="bg-[#263746] border border-[#e8f1f5]/50 rounded-lg p-4">
          <p class="text-[#e8f1f5] leading-relaxed whitespace-pre-line">
            {{ summary }}
          </p>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped></style>
