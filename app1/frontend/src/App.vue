<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'

const URL = 'http://127.0.0.1/nombre_endpoint' // nombre_endpoint sustituir por el nombre adecuadao

const text = ref('')

async function connectToAPI(): Promise<void> {
  return await axios.post(URL) // Terminar y agregar lo necesario
}
</script>

<template>
  <div class="min-h-screen bg-slate-900">
    <h1 class="text-amber-50">Resumidor Automático</h1>

    <input
      class="border border-[#ffffff86] rounded-sm text-white px-4 py-2 h-min-40"
      type="text"
      placeholder="Escribe o pega tu texto aquí..."
    />
  </div>
</template>

<style scoped></style>
