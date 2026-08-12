<script>
  import { onDestroy } from 'svelte';

  export let value = 0;
  export let duration = 550;

  let displayed = value;
  let target = value;
  let frame = 0;

  const easeOut = (t) => 1 - Math.pow(1 - t, 3);

  function animateTo(next) {
    if (typeof window === 'undefined' || next === target) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      cancelAnimationFrame(frame);
      target = next;
      displayed = next;
      return;
    }

    cancelAnimationFrame(frame);
    const from = displayed;
    const start = performance.now();
    target = next;

    const tick = (now) => {
      const progress = Math.min(1, (now - start) / duration);
      displayed = from + (target - from) * easeOut(progress);
      if (progress < 1) frame = requestAnimationFrame(tick);
    };

    frame = requestAnimationFrame(tick);
  }

  $: animateTo(value);

  onDestroy(() => {
    if (typeof window !== 'undefined') cancelAnimationFrame(frame);
  });
</script>

{Math.round(displayed).toLocaleString('en-US')}
