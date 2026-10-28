<script setup lang="ts">
import type { Concept } from '@/types/types';

defineProps<{
    concept: Concept
}>()
</script>

<template>
    <div class="py-2">
        <div class="ps-2 py-0.5 border-l-2 border-l-on-primary/30">
            <p class="text-on-primary font-semibold text-base">{{ concept.concept }}</p>

            <p class="text-on-primary/60 text-sm">{{ concept.definition }}</p>
        </div>
    </div>
</template>