<script setup lang="ts" generic="T extends string | null">
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";

/**
 * Category filter: a row of pills with an indicator that slides to the
 * active one (it follows across wrapped lines too). Buttons expose
 * aria-pressed; the group is labelled for screen readers.
 */
const props = defineProps<{
  options: { value: T; label: string }[];
  modelValue: T;
  label: string;
}>();
const emit = defineEmits<{ "update:modelValue": [value: T] }>();

const wrap = ref<HTMLElement | null>(null);
const indicator = ref({ x: 0, y: 0, w: 0, h: 0, visible: false });

function measure() {
  const active = wrap.value?.querySelector<HTMLElement>(".fp-pill.on");
  if (!active) {
    indicator.value.visible = false;
    return;
  }
  indicator.value = {
    x: active.offsetLeft,
    y: active.offsetTop,
    w: active.offsetWidth,
    h: active.offsetHeight,
    visible: true,
  };
}

let ro: ResizeObserver | null = null;
onMounted(() => {
  measure();
  ro = new ResizeObserver(measure);
  if (wrap.value) ro.observe(wrap.value);
});
onBeforeUnmount(() => ro?.disconnect());
watch(
  () => [props.modelValue, props.options.length],
  () => nextTick(measure),
);
</script>

<template>
  <div ref="wrap" class="fp" role="group" :aria-label="label">
    <span
      class="fp-indicator"
      aria-hidden="true"
      :style="{
        opacity: indicator.visible ? 1 : 0,
        width: `${indicator.w}px`,
        height: `${indicator.h}px`,
        transform: `translate(${indicator.x}px, ${indicator.y}px)`,
      }"
    ></span>
    <button
      v-for="o in options"
      :key="String(o.value)"
      type="button"
      class="fp-pill"
      :class="{ on: o.value === modelValue }"
      :aria-pressed="o.value === modelValue"
      @click="emit('update:modelValue', o.value)"
    >
      {{ o.label }}
    </button>
  </div>
</template>

<style scoped>
.fp {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.fp-indicator {
  position: absolute;
  left: 0;
  top: 0;
  border-radius: var(--radius-pill);
  background: var(--blue);
  box-shadow: 0 6px 18px rgba(200, 16, 46, 0.3);
  transition:
    transform 0.45s var(--ease-out),
    width 0.45s var(--ease-out),
    height 0.45s var(--ease-out),
    opacity 0.2s;
  pointer-events: none;
}
.fp-pill {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border-soft);
  color: var(--muted);
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition:
    color 0.3s,
    border-color 0.2s,
    background 0.3s;
}
.fp-pill:hover:not(.on) {
  border-color: var(--blue);
  color: var(--blue);
}
/* The active pill becomes transparent so the sliding indicator shows through. */
.fp-pill.on {
  background: transparent;
  border-color: transparent;
  color: #fff;
}
</style>
