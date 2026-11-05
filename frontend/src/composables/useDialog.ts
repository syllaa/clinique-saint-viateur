import { reactive } from "vue";

type DialogKind = "alert" | "confirm" | "prompt";

interface DialogState {
  open: boolean;
  kind: DialogKind;
  message: string;
  title?: string;
  danger: boolean;
  confirmLabel: string;
  cancelLabel: string;
  inputValue: string;
  inputPlaceholder: string;
}

interface DialogOptions {
  title?: string;
  danger?: boolean;
  confirmLabel?: string;
  cancelLabel?: string;
}

interface PromptOptions extends DialogOptions {
  defaultValue?: string;
  placeholder?: string;
}

const state = reactive<DialogState>({
  open: false,
  kind: "alert",
  message: "",
  title: undefined,
  danger: false,
  confirmLabel: "OK",
  cancelLabel: "Annuler",
  inputValue: "",
  inputPlaceholder: "",
});

let resolver: ((value: boolean | string | null) => void) | null = null;

function openDialog(kind: "alert" | "confirm", message: string, opts: DialogOptions) {
  return new Promise<boolean>((resolve) => {
    resolver = resolve as (value: boolean | string | null) => void;
    Object.assign(state, {
      open: true,
      kind,
      message,
      title: opts.title,
      danger: opts.danger ?? false,
      confirmLabel: opts.confirmLabel ?? (kind === "confirm" ? "Confirmer" : "OK"),
      cancelLabel: opts.cancelLabel ?? "Annuler",
      inputValue: "",
      inputPlaceholder: "",
    });
  });
}

export function alertDialog(message: string, opts: DialogOptions = {}) {
  return openDialog("alert", message, opts);
}

export function confirmDialog(message: string, opts: DialogOptions = {}) {
  return openDialog("confirm", message, opts);
}

export function promptDialog(message: string, opts: PromptOptions = {}) {
  return new Promise<string | null>((resolve) => {
    resolver = resolve as (value: boolean | string | null) => void;
    Object.assign(state, {
      open: true,
      kind: "prompt",
      message,
      title: opts.title,
      danger: false,
      confirmLabel: opts.confirmLabel ?? "OK",
      cancelLabel: opts.cancelLabel ?? "Annuler",
      inputValue: opts.defaultValue ?? "",
      inputPlaceholder: opts.placeholder ?? "",
    });
  });
}

export function resolveDialog(result: boolean) {
  state.open = false;
  resolver?.(result);
  resolver = null;
}

export function resolvePrompt(submit: boolean) {
  state.open = false;
  resolver?.(submit ? state.inputValue : null);
  resolver = null;
}

export function useDialogState() {
  return state;
}
