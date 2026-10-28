<script setup lang="ts">
defineProps<{
    text: string
    isActive: boolean
}>()

const emit = defineEmits<{
    'update:isActive': [value: boolean]
}>()
</script>

<template>
    <div class="flex items-center gap-3">
        <button type="button" role="switch" :aria-checked="isActive"
            :aria-label="isActive ? 'Desactivar opción' : 'Activar opción'" @click="emit('update:isActive', !isActive)"
            :class="isActive ? 'bg-primary' : 'bg-bg-tertiary border border-outline-primary'"
            class="relative flex h-6 w-12 items-center rounded-xl transition-colors cursor-pointer">
            <span :class="isActive ? 'translate-x-6' : 'translate-x-0'
                "
                class="bg-on-primary absolute left-0.5 size-5 rounded-full transition-transform duration-200 ease-in-out"></span>
        </button>

        <p class="text-xs md:text-sm text-on-primary">{{ text }}</p>
    </div>
</template>