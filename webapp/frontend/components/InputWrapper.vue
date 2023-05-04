<template>
  <div>
    <label>
      <div class="mb-1">{{ label }}</div>
      <input
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        v-bind="$attrs"
        class="w-full bg-neutral-700 rounded p-1"
      />
    </label>
  </div>
</template>

<script setup lang="ts">
defineProps(['modelValue', 'label'])
defineEmits(['update:modelValue'])
</script>