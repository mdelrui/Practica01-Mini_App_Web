<script setup lang="ts">
import { summaryLengthLabels, type SummaryLength } from '@/types/types';
import { capitalize } from 'vue';

defineProps<{
    length: SummaryLength
    isActive: boolean
}>()

const emit = defineEmits<{
    'select': [value: SummaryLength]
}>()
</script>

<template>
    <button type="button" @click="emit('select', length)"
        :class="isActive ? 'bg-primary font-normal text-bg-primary' : 'bg-transparent text-on-primary hover:bg-primary/20'"
        class="h-10 w-23 rounded-lg font-semibold text-sm cursor-pointer">
        {{ capitalize(summaryLengthLabels[length]) }}
    </button>
</template>