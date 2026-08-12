<script>
  import { onMount } from 'svelte';

  const steps = [
    'After two rounds, this is how much money the 100 people in the room have.',
    'Now let the game run for 10,000 rounds so everyone can win roughly half their coin flips.',
    'Whoa, you lost all your money. Meanwhile, one person ended up with nearly all of the wealth!'
  ];

  const afterTwo = [
    ...Array(20).fill(640),
    ...Array(40).fill(992),
    ...Array(20).fill(1020),
    ...Array(14).fill(1320),
    ...Array(6).fill(1440)
  ];
  const condensed = [...Array(95).fill(0), 1186, 5300, 11700, 21000, 60814];

  let activeStep = 0;
  let stepNodes = [];

  $: values = activeStep < 2 ? afterTwo : condensed;
  $: maximum = activeStep < 2 ? 1500 : 96000;
  $: ticks = activeStep < 2 ? [0, 500, 1000, 1500] : [0, 24000, 48000, 72000, 96000];
  $: richest = Math.max(...values);
  $: poorest = Math.min(...values);
  $: richestLabelY = Math.max(68, 550 - (richest / maximum) * 450 - 12);

  onMount(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries
          .filter((item) => item.isIntersecting)
          .sort(
            (a, b) =>
              Math.abs(a.boundingClientRect.top + a.boundingClientRect.height / 2 - innerHeight / 2) -
              Math.abs(b.boundingClientRect.top + b.boundingClientRect.height / 2 - innerHeight / 2)
          )[0];
        if (entry) activeStep = Number(entry.target.dataset.step);
      },
      { threshold: 0, rootMargin: '-46% 0px -46% 0px' }
    );

    stepNodes.filter(Boolean).forEach((node) => observer.observe(node));
    return () => observer.disconnect();
  });
</script>

<section class="wealth-scrolly" aria-label="Wealth distribution simulation">
  <div class="chart-scene">
    <div class="chart-meta">
      <span>Round: <strong>{activeStep < 2 ? '2' : '10,000'}</strong></span>
    </div>

    <svg viewBox="0 0 1000 620" role="img" aria-label={`The poorest player has $${poorest} and the richest has $${richest}.`}>
      <g class="grid">
        {#each ticks as tick}
          <line x1="40" x2="970" y1={550 - (tick / maximum) * 450} y2={550 - (tick / maximum) * 450}></line>
          <text x="42" y={542 - (tick / maximum) * 450}>${tick.toLocaleString()}</text>
        {/each}
      </g>
      <g class="bars">
        {#each values as value, index}
          <rect
            class:poorest={value === poorest}
            class:richest={value === richest}
            x={48 + index * 9.15}
            y="100"
            width="6.6"
            height="450"
            style:transform={`scaleY(${Math.max(0.003, value / maximum)})`}
          ></rect>
        {/each}
      </g>
      <text class="poor-label" x="90" y="540">Poorest: ${poorest.toLocaleString()}</text>
      <text class="rich-label" x="965" y={richestLabelY} text-anchor="end">Richest: ${richest.toLocaleString()}</text>
    </svg>

    <div class="grain"></div>
  </div>

  <div class="steps">
    {#each steps as text, index}
      <article
        class:active={activeStep === index}
        class="step"
        data-step={index}
        bind:this={stepNodes[index]}
      >
        <p>{text}</p>
      </article>
    {/each}
  </div>
</section>

<style>
  .wealth-scrolly { position: relative; max-width: 72rem; margin: 3rem auto 0; }
  .chart-scene { position: sticky; top: 2.5dvh; width: min(90vw, 95dvh); height: min(90vw, 95dvh); min-height: 32rem; margin-inline: auto; overflow: hidden; border: 3px solid #0b080d; background: #e5dfe8; }
  .chart-meta { position: absolute; z-index: 4; top: 0.45rem; right: 1.1rem; color: #171319; font-size: clamp(0.72rem, 1.7vw, 1rem); }
  .chart-meta strong { font-weight: 900; }
  svg { position: absolute; z-index: 2; inset: 7% 2% 4%; width: 96%; height: 89%; overflow: visible; }
  .grid line { stroke: rgba(57,42,65,0.24); stroke-dasharray: 4 5; }
  .grid text { fill: #66596b; font-size: 14px; }
  .bars rect { fill: #a58aad; transform-box: fill-box; transform-origin: center bottom; transition: transform 1800ms cubic-bezier(0.25, 0.1, 0.25, 1), fill 500ms ease; }
  .bars rect.poorest { fill: #421050; }
  .bars rect.richest { fill: #620070; }
  .poor-label, .rich-label { fill: #4b1158; font-size: 17px; font-weight: 800; }
  .grain { position: absolute; z-index: 7; inset: -100%; background: url('/assets/grain.png'); opacity: 0.12; pointer-events: none; }
  .steps { position: relative; z-index: 8; margin-top: calc(-1 * min(90vw, 95dvh)); pointer-events: none; }
  .step { min-height: 100dvh; display: flex; align-items: flex-start; justify-content: center; padding: 13dvh 1rem 0; opacity: 0; transition: opacity 350ms ease; }
  .step.active { opacity: 1; }
  .step p { max-width: 31rem; margin: 0; padding: 0.65rem 0.9rem; background: rgba(8,7,9,0.87); color: white; font-size: clamp(1rem, 2vw, 1.28rem); line-height: 1.35; text-align: center; }

  @media (max-width: 640px) {
    .chart-scene { top: 8dvh; width: 96vw; height: 96vw; min-height: 0; }
    .steps { margin-top: -96vw; }
    .step { min-height: 92dvh; padding: 9dvh 0.65rem 0; }
    .chart-meta { top: 0.65rem; right: 0.75rem; left: 0.75rem; font-size: 0.57rem; }
  }

  @media (prefers-reduced-motion: reduce) {
    .bars rect, .step { transition-duration: 0.01ms; transition-delay: 0ms; }
  }
</style>
