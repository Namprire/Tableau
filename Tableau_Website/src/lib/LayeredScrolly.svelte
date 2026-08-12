<script>
  import { onMount } from 'svelte';
  import AnimatedNumber from './AnimatedNumber.svelte';

  export let steps = [];
  export let layers = [];
  export let scenes = [];
  export let label = 'Illustrated story';
  export let showScrollHint = false;

  let activeStep = 0;
  let stepNodes = [];

  $: scene = scenes[activeStep] ?? scenes[0] ?? { background: '#7c6a85', layers: {} };
  $: stats = scene.stats ?? null;

  function layerStyle(id) {
    const state = scene.layers?.[id] ?? {};
    const x = state.x ?? 0;
    const y = state.y ?? 0;
    const width = state.width ?? 100;
    const scale = state.scale ?? 1;
    const rotate = state.rotate ?? 0;
    const opacity = state.opacity ?? 0;
    const z = state.z ?? 1;

    return `z-index:${z};opacity:${opacity};transform:translate3d(${x}cqw, ${y}cqh, 0) scale(${(width / 100) * scale}) rotate(${rotate}deg)`;
  }

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

<section class="scrolly" aria-label={label}>
  <div class="scene" style:background={scene.background}>
    <div class="scene-art">
      {#each layers as layer}
        <img
          class="scene-layer"
          class:loaded={(scene.layers?.[layer.id]?.opacity ?? 0) > 0}
          src={layer.src}
          alt={layer.alt}
          style={layerStyle(layer.id)}
          draggable="false"
        />
      {/each}

      <div
        class:visible={Boolean(scene.faceCards)}
        class="face-card left-face-card"
        style:background={scene.faceCards?.left ?? '#e8dfe9'}
      ></div>
      <div
        class:visible={Boolean(scene.faceCards)}
        class="face-card right-face-card"
        style:background={scene.faceCards?.right ?? '#e8dfe9'}
      ></div>

      <div class:visible={Boolean(stats)} class="game-stats" aria-hidden={!stats}>
        <div class="player-stat left-stat">
          <strong>{stats?.leftName ?? 'Me'}</strong>
          <small>{stats?.leftRecord ?? '0–0'}</small>
          <span>${stats ? '' : '0'}{#if stats}<AnimatedNumber value={stats.left} />{/if}</span>
          <i><b style:width={`${Math.min(100, (stats?.left ?? 0) / 15)}%`}></b></i>
        </div>
        <div class="wager-stat" class:visible={Boolean(stats?.wager)}>
          <small>Wager</small>
          <strong>${stats ? '' : '0'}{#if stats}<AnimatedNumber value={stats.wager} />{/if}</strong>
        </div>
        <div class="player-stat right-stat">
          <strong>{stats?.rightName ?? 'Opponent'}</strong>
          <small>{stats?.rightRecord ?? '0–0'}</small>
          <span>${stats ? '' : '0'}{#if stats}<AnimatedNumber value={stats.right} />{/if}</span>
          <i><b style:width={`${Math.min(100, (stats?.right ?? 0) / 15)}%`}></b></i>
        </div>
      </div>

      <div class:visible={Boolean(scene.speechLeft)} class="speech left-speech">
        {scene.speechLeft ?? ''}
      </div>
      <div class:visible={Boolean(scene.speechRight)} class="speech right-speech">
        {scene.speechRight ?? ''}
      </div>

      <div class="grain"></div>
    </div>

    {#if showScrollHint}
      <div class:hidden={activeStep > 0} class="scroll-hint" aria-hidden="true">
        <span>Scroll down</span>
        <i></i>
      </div>
    {/if}
  </div>

  <div class="steps">
    {#each steps as text, index}
      <article
        class:active={activeStep === index}
        class="step"
        data-step={index}
        bind:this={stepNodes[index]}
        aria-current={activeStep === index ? 'step' : undefined}
      >
        <p>{text}</p>
      </article>
    {/each}
  </div>
</section>

<style>
  .scrolly { position: relative; max-width: 72rem; min-height: 100dvh; margin-inline: auto; padding-block: 0.5rem; }
  .scene { position: sticky; z-index: 0; top: 2.5dvh; width: min(90vw, 95dvh); height: min(90vw, 95dvh); max-width: 69rem; max-height: 69rem; min-height: 32rem; margin-inline: auto; overflow: visible; border: 3px solid #080709; transition: background-color 600ms ease; }
  .scene-art { position: absolute; inset: 0; overflow: hidden; container-type: size; background: inherit; }
  .scene-layer { position: absolute; top: 0; left: 0; width: 100%; max-width: none; transform-origin: top left; will-change: transform, opacity; transition: transform 800ms cubic-bezier(0.25, 0.1, 0.25, 1), opacity 500ms ease; user-select: none; }
  .face-card { position: absolute; z-index: 2; top: 33%; width: 30%; aspect-ratio: 1; opacity: 0; transition: background-color 500ms ease, opacity 350ms ease; }
  .face-card.visible { opacity: 0.76; }
  .left-face-card { left: 6%; }
  .right-face-card { right: 6%; }
  .grain { position: absolute; z-index: 20; inset: -125%; width: 350%; height: 350%; background-image: url('/assets/grain.png'); opacity: 0.23; pointer-events: none; animation: grain 14s steps(8) infinite; }
  .steps { position: relative; z-index: 3; margin-top: calc(-1 * min(90vw, 95dvh)); pointer-events: none; }
  .step { min-height: 100dvh; display: flex; align-items: flex-start; justify-content: center; padding: 4.5dvh 1rem 0; opacity: 0; transition: opacity 350ms ease; }
  .step.active { opacity: 1; }
  .step p { width: fit-content; max-width: min(31rem, 90vw); margin: 0; padding: 0.65rem 0.9rem; background: rgba(10, 9, 11, 0.87); color: white; font-size: clamp(1rem, 2vw, 1.35rem); line-height: 1.32; text-align: center; text-wrap: balance; }
  .game-stats { position: absolute; z-index: 9; top: 1.25rem; right: 1.5rem; left: 1.5rem; color: white; font-family: var(--sans); opacity: 0; transition: opacity 350ms ease; }
  .game-stats.visible { opacity: 1; }
  .player-stat { position: absolute; top: 0; display: grid; gap: 0.1rem; width: 42%; font-size: clamp(0.75rem, 1.8vw, 1.1rem); }
  .player-stat strong { color: var(--pink-light); font-size: 0.72em; letter-spacing: 0.12em; text-transform: uppercase; }
  .player-stat span { font-size: 1.15em; font-weight: 700; }
  .player-stat small { color: rgba(255,255,255,0.75); }
  .player-stat i { width: 100%; height: 0.72rem; margin-top: 0.3rem; border: 1px solid rgba(255,255,255,0.7); background: rgba(255,255,255,0.12); }
  .player-stat i b { display: block; height: 100%; background: var(--pink-light); transition: width 600ms ease; }
  .right-stat { right: 0; text-align: right; }
  .right-stat i { margin-left: auto; }
  .wager-stat { position: absolute; left: 50%; display: grid; transform: translateX(-50%); text-align: center; opacity: 0; transition: opacity 300ms ease; }
  .wager-stat.visible { opacity: 1; }
  .wager-stat small { color: var(--pink-light); font-size: 0.66rem; letter-spacing: 0.12em; text-transform: uppercase; }
  .speech { position: absolute; z-index: 11; top: 22%; max-width: 13rem; padding: 0.65rem 0.8rem; border: 2px solid #080709; border-radius: 0.45rem; background: #f4eff4; color: #110d14; font-weight: 700; opacity: 0; transform: translateY(0.7rem) scale(0.96); transition: opacity 350ms ease, transform 600ms cubic-bezier(0.25, 0.1, 0.25, 1); }
  .speech.visible { opacity: 1; transform: translateY(0) scale(1); }
  .left-speech { left: 6%; }
  .right-speech { right: 6%; }
  .scroll-hint { position: absolute; top: calc(100% + 2.3rem); left: 50%; display: grid; place-items: center; gap: 0.35rem; color: #262027; opacity: 0.55; transform: translateX(-50%); transition: opacity 300ms ease; }
  .scroll-hint.hidden { opacity: 0; }
  .scroll-hint span { font-size: 0.68rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }
  .scroll-hint i { width: 0; height: 0; border-top: 0.8rem solid #262027; border-right: 0.7rem solid transparent; border-left: 0.7rem solid transparent; animation: bounce 1s ease-in-out infinite; }

  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(0.45rem); }
  }

  @keyframes grain {
    0%, 100% { transform: translate(0, 0); }
    20% { transform: translate(6%, -5%); }
    40% { transform: translate(-5%, 8%); }
    60% { transform: translate(8%, 3%); }
    80% { transform: translate(-7%, -6%); }
  }

  @media (max-width: 640px) {
    .scrolly { padding-top: 0; }
    .scene { top: 8dvh; width: 96vw; height: 96vw; min-height: 0; }
    .steps { margin-top: -96vw; }
    .step { min-height: 92dvh; padding: 4dvh 0.65rem 0; }
    .step p { font-size: 1rem; }
    .game-stats { top: 0.75rem; right: 0.8rem; left: 0.8rem; }
    .player-stat i { height: 0.45rem; }
    .speech { top: 24%; max-width: 8.5rem; padding: 0.45rem 0.55rem; font-size: 0.74rem; }
  }

  @media (prefers-reduced-motion: reduce) {
    .scene, .scene-layer, .face-card, .step, .game-stats, .wager-stat, .speech, .scroll-hint, .player-stat i b { transition-duration: 0.01ms; }
    .grain, .scroll-hint i { animation: none; }
  }
</style>
