<script setup lang="ts">
withDefaults(defineProps<{ variant?: "success" | "error" }>(), {
  variant: "success",
});
</script>

<template>
  <div class="alert" :class="variant">
    <slot />
  </div>
</template>

<style scoped>
.alert {
  margin-top: 12px;
  border-radius: 8px;
  padding: 13px;
  font-size: 0.88rem;
  text-align: center;
}
.alert.success {
  background: #fde8ea;
  border: 1px solid #f0b0b8;
  color: var(--green);
}
.alert.error {
  background: rgba(179, 18, 31, 0.08);
  border: 1px solid rgba(179, 18, 31, 0.25);
  color: var(--red-alert);
}
</style>
