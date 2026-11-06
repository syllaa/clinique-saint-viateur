/**
 * Coordination between the page <Transition> (App.vue) and the router's
 * scrollBehavior: the scroll reset must happen once the old page has
 * finished leaving, otherwise the leaving page visibly jumps to the top.
 */
let waiters: (() => void)[] = [];

/** Called by App.vue's <Transition @after-leave>. */
export function notifyPageLeft(): void {
  const pending = waiters;
  waiters = [];
  pending.forEach((resolve) => resolve());
}

/** Resolves when the current page has left (or after a safety timeout). */
export function waitForPageLeave(timeoutMs = 700): Promise<void> {
  return new Promise((resolve) => {
    let done = false;
    const finish = () => {
      if (done) return;
      done = true;
      resolve();
    };
    waiters.push(finish);
    setTimeout(finish, timeoutMs);
  });
}
