import { computed, onBeforeUnmount, onMounted, ref } from "vue";

/**
 * Consultation opening hours (the same ones shown everywhere on the site).
 * Emergencies are open 24/7 regardless. Times are evaluated in Abidjan time
 * (GMT, no daylight saving), whatever the visitor's own timezone.
 */
export const OPENING_HOURS: { day: string; open: string | null; close: string | null }[] = [
  { day: "Dimanche", open: null, close: null },
  { day: "Lundi", open: "08:00", close: "20:00" },
  { day: "Mardi", open: "08:00", close: "20:00" },
  { day: "Mercredi", open: "08:00", close: "20:00" },
  { day: "Jeudi", open: "08:00", close: "20:00" },
  { day: "Vendredi", open: "08:00", close: "20:00" },
  { day: "Samedi", open: "08:00", close: "12:00" },
];

/** Monday-first order, for display tables. */
export const OPENING_HOURS_WEEK = [...OPENING_HOURS.slice(1), OPENING_HOURS[0]];

const toMinutes = (hhmm: string) => {
  const [h, m] = hhmm.split(":").map(Number);
  return h * 60 + m;
};

function abidjanNow(): { dayIndex: number; minutes: number } {
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Africa/Abidjan",
    weekday: "short",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(new Date());
  const get = (type: string) => parts.find((p) => p.type === type)?.value ?? "0";
  const dayIndex = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(get("weekday"));
  return { dayIndex, minutes: Number(get("hour")) * 60 + Number(get("minute")) };
}

export function useClinicHours() {
  const now = ref(abidjanNow());
  let timer: ReturnType<typeof setInterval> | undefined;
  onMounted(() => {
    timer = setInterval(() => (now.value = abidjanNow()), 60_000);
  });
  onBeforeUnmount(() => clearInterval(timer));

  const today = computed(() => OPENING_HOURS[now.value.dayIndex]);

  const consultationsOpen = computed(() => {
    const { open, close } = today.value;
    if (!open || !close) return false;
    return now.value.minutes >= toMinutes(open) && now.value.minutes < toMinutes(close);
  });

  /** Human summary, e.g. "Consultations ouvertes jusqu'à 20h". */
  const statusLabel = computed(() => {
    const { open, close } = today.value;
    if (consultationsOpen.value && close) return `Consultations ouvertes jusqu'à ${close.replace(":00", "h")}`;
    if (open && now.value.minutes < toMinutes(open)) return `Consultations dès ${open.replace(":00", "h")}`;
    return "Consultations fermées · urgences ouvertes";
  });

  return { today, todayName: computed(() => today.value.day), consultationsOpen, statusLabel };
}
