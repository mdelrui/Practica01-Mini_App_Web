<script setup lang="ts">
import { Clipboard, ClipboardCheck } from 'lucide-vue-next';

defineProps<{
    copied: boolean
}>()

const emit = defineEmits<{
    'copy': []
}>()
</script>

<template>
    <button type="button" aria-label="Copiar" title="Copiar"
        class="text-on-primary/50 transition-colors cursor-pointer hover:text-on-primary"
        @click="!copied && emit('copy')">
        <ClipboardCheck v-if="copied" :size="16" />
        <Clipboard v-else :size="16" />
    </button>
</template>