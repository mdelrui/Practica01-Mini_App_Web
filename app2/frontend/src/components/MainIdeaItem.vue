<script setup lang="ts">
defineProps<{
    num: number
    text: string
}>()
</script>

<template>
    <div class="flex gap-2 items-center py-2">
        <div class="size-6 bg-bg-tertiary rounded-full flex justify-center items-center">
            <span class="text-primary font-semibold text-sm">{{ num }}</span>
        </div>

        <p class="text-sm text-on-primary">{{ text }}</p>
    </div>
</template>