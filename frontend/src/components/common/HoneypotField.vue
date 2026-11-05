<script setup lang="ts">
/**
 * Anti-spam trap. Humans never see nor reach this field (off-screen, out of
 * the tab order, hidden from screen readers); naive bots fill every input.
 * The backend rejects any submission where it is not empty.
 */
const model = defineModel<string>({ default: "" });
</script>

<template>
  <div class="hp" aria-hidden="true">
    <label>
      Ne pas remplir ce champ
      <input v-model="model" type="text" name="website" tabindex="-1" autocomplete="off" />
    </label>
  </div>
</template>

<style scoped>
.hp {
  position: absolute;
  left: -10000px;
  top: auto;
  width: 1px;
  height: 1px;
  overflow: hidden;
}
</style>
