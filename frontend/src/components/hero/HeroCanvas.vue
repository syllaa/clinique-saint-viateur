<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from "vue";

import { reducedMotion } from "@/motion/motionPreferences";

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  r: number;
  op: number;
  cross: boolean;
  crossRot: number;
  crossVr: number;
}

const canvasRef = ref<HTMLCanvasElement | null>(null);
const N = 65;
let particles: Particle[] = [];
let width = 0;
let height = 0;
let ecgX = 0;
let rafId = 0;

function resize(canvas: HTMLCanvasElement) {
  // Draw in CSS pixels, back the canvas with device pixels (sharp on retina),
  // capped at 2x to keep the fill cost reasonable on phones.
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  width = canvas.offsetWidth;
  height = canvas.offsetHeight;
  canvas.width = Math.round(width * dpr);
  canvas.height = Math.round(height * dpr);
  canvas.getContext("2d")?.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function randomParticle(): Particle {
  return {
    x: Math.random() * width,
    y: Math.random() * height,
    vx: (Math.random() - 0.5) * 0.32,
    vy: (Math.random() - 0.5) * 0.32,
    r: Math.random() * 1.6 + 0.4,
    op: Math.random() * 0.5 + 0.1,
    cross: Math.random() < 0.1,
    crossRot: Math.random() * Math.PI,
    crossVr: (Math.random() - 0.5) * 0.005,
  };
}

function drawCross(ctx: CanvasRenderingContext2D, x: number, y: number, s: number, op: number, rot: number) {
  ctx.save();
  ctx.globalAlpha = op * 0.55;
  ctx.strokeStyle = "rgba(200,16,46,.9)";
  ctx.lineWidth = 1.2;
  ctx.translate(x, y);
  ctx.rotate(rot);
  ctx.beginPath();
  ctx.moveTo(-s, 0);
  ctx.lineTo(s, 0);
  ctx.moveTo(0, -s);
  ctx.lineTo(0, s);
  ctx.stroke();
  ctx.restore();
}

function drawEcg(ctx: CanvasRenderingContext2D) {
  const y0 = height * 0.86;
  const amp = 20;
  const seg = width * 0.35;
  for (let ox = (ecgX % seg) - seg; ox < width; ox += seg) {
    const pts: [number, number][] = [
      [0, 0],
      [0.08, 0],
      [0.14, -0.6],
      [0.22, 0.9],
      [0.3, -0.9],
      [0.38, 0.5],
      [0.45, 0],
      [1, 0],
    ];
    ctx.save();
    ctx.globalAlpha = 0.18;
    ctx.strokeStyle = "rgba(200,16,46,1)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    pts.forEach(([px, py], i) => {
      const x = ox + px * seg;
      const y = y0 + py * amp;
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.restore();
  }
  ecgX += 0.4;
}

function frame(ctx: CanvasRenderingContext2D) {
  ctx.clearRect(0, 0, width, height);
  drawEcg(ctx);

  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const d = Math.sqrt(dx * dx + dy * dy);
      if (d < 115) {
        ctx.save();
        ctx.globalAlpha = (1 - d / 115) * 0.11;
        ctx.strokeStyle = "rgba(224,71,90,1)";
        ctx.lineWidth = 0.6;
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.stroke();
        ctx.restore();
      }
    }
  }

  particles.forEach((p) => {
    p.x += p.vx;
    p.y += p.vy;
    if (p.x < 0) p.x = width;
    if (p.x > width) p.x = 0;
    if (p.y < 0) p.y = height;
    if (p.y > height) p.y = 0;

    if (p.cross) {
      p.crossRot += p.crossVr;
      drawCross(ctx, p.x, p.y, 5.5, p.op, p.crossRot);
    } else {
      ctx.save();
      ctx.globalAlpha = p.op;
      ctx.fillStyle = "rgba(224,71,90,1)";
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  });

}

// ─── Lifecycle: only animate while visible, on-screen and allowed ───
let ctx2d: CanvasRenderingContext2D | null = null;
let running = false;
let onScreen = true;
let onWindowResize: (() => void) | null = null;
let io: IntersectionObserver | null = null;

function loop() {
  if (!ctx2d) return;
  frame(ctx2d);
  rafId = requestAnimationFrame(loop);
}

function shouldRun() {
  return onScreen && !document.hidden && !reducedMotion.value;
}

function sync() {
  if (shouldRun() && !running) {
    running = true;
    rafId = requestAnimationFrame(loop);
  } else if (!shouldRun() && running) {
    running = false;
    cancelAnimationFrame(rafId);
  }
  // Reduced motion: keep one still frame as a decorative background.
  if (reducedMotion.value && ctx2d) frame(ctx2d);
}

const stopMotionWatch = watch(reducedMotion, sync);

onMounted(() => {
  const canvas = canvasRef.value;
  if (!canvas) return;
  ctx2d = canvas.getContext("2d");
  if (!ctx2d) return;

  resize(canvas);
  // Fewer particles on small screens: same look, a quarter of the line checks.
  const count = width < 640 ? Math.round(N * 0.55) : N;
  particles = Array.from({ length: count }, randomParticle);

  onWindowResize = () => resize(canvas);
  window.addEventListener("resize", onWindowResize, { passive: true });
  document.addEventListener("visibilitychange", sync);

  io = new IntersectionObserver(([entry]) => {
    onScreen = entry.isIntersecting;
    sync();
  });
  io.observe(canvas);

  sync();
});

onBeforeUnmount(() => {
  running = false;
  cancelAnimationFrame(rafId);
  stopMotionWatch();
  io?.disconnect();
  document.removeEventListener("visibilitychange", sync);
  if (onWindowResize) window.removeEventListener("resize", onWindowResize);
});
</script>

<template>
  <canvas ref="canvasRef" class="hero-canvas"></canvas>
</template>

<style scoped>
.hero-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
</style>
