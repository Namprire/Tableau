<script>
  import { onMount } from 'svelte';
  import { interactionModes, overallBalance, topOccupations } from './storyData';

  const steps = [
    {
      kicker: 'Start with exposure',
      title: 'AI enters work through tasks.',
      text: 'The dataset contains 3,963 occupation–task pairs across hundreds of occupations. Each mark here is one percent of measured workplace AI exposure.'
    },
    {
      kicker: 'An uneven entrance',
      title: 'Five occupations account for about 26% of exposure.',
      text: 'Programming, software, web, and systems work dominate the most exposed occupations in this dataset.'
    },
    {
      kicker: 'The misleading shortcut',
      title: 'But exposure is not automation.',
      text: 'Knowing where AI appears does not tell us whether it performs the task or helps a person perform it.'
    },
    {
      kicker: 'The role split',
      title: 'When AI is used, augmentation is the larger share.',
      text: 'Among classified exposure, 43% is automation-oriented and 57% is augmentation-oriented.'
    },
    {
      kicker: 'Inside the total',
      title: 'Five interaction modes create that split.',
      text: 'Directive work and feedback loops form automation. Iteration, learning, and validation form augmentation.'
    }
  ];

  const scenes = [
    { view: 'tasks', label: '3,963 task pairs' },
    { view: 'concentration', label: 'Top five occupations: 26.05%' },
    { view: 'question', label: 'Exposure is not a role' },
    { view: 'balance', label: 'How AI is used' },
    { view: 'modes', label: 'The five interaction modes' }
  ];

  let activeStep = 0;
  let stepNodes = [];

  $: scene = scenes[activeStep];

  onMount(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const closest = entries
          .filter((entry) => entry.isIntersecting)
          .sort(
            (a, b) =>
              Math.abs(a.boundingClientRect.top + a.boundingClientRect.height / 2 - innerHeight / 2) -
              Math.abs(b.boundingClientRect.top + b.boundingClientRect.height / 2 - innerHeight / 2)
          )[0];

        if (closest) activeStep = Number(closest.target.dataset.step);
      },
      { threshold: 0, rootMargin: '-44% 0px -44% 0px' }
    );

    stepNodes.filter(Boolean).forEach((node) => observer.observe(node));
    return () => observer.disconnect();
  });
</script>

<section id="exposure-story" class="scrolly" aria-label="Where AI enters work and the role it plays">
  <div class="sticky-scene">
    <div class:tasks={scene.view === 'tasks'} class:concentration={scene.view === 'concentration'} class:question={scene.view === 'question'} class:balance={scene.view === 'balance'} class:modes={scene.view === 'modes'} class="scene">
      <header class="scene-heading">
        <span>AI at work</span>
        <strong>{scene.label}</strong>
      </header>

      <div class="task-field" aria-hidden="true">
        {#each Array(100) as _, index}
          <i class:top-five={index < 26} style={`--delay:${(index % 10) * 18 + Math.floor(index / 10) * 8}ms`}></i>
        {/each}
      </div>

      <div class="occupation-ranking" aria-hidden={scene.view !== 'concentration'}>
        <p>Share of measured exposure</p>
        {#each topOccupations as occupation, index}
          <div class="occupation-row" style={`--delay:${index * 90}ms`}>
            <span>{occupation.name}</span>
            <div><i style:width={`${(occupation.exposure / topOccupations[0].exposure) * 100}%`}></i></div>
            <strong>{occupation.exposure.toFixed(2)}%</strong>
          </div>
        {/each}
        <small>Top five combined: 26.05%</small>
      </div>

      <div class="question-layer" aria-hidden={scene.view !== 'question'}>
        <div class="exposure-card">
          <span>How much?</span>
          <strong>Exposure</strong>
        </div>
        <div class="not-equal" aria-hidden="true">≠</div>
        <div class="role-card">
          <span>What role?</span>
          <strong>Automation or augmentation</strong>
        </div>
      </div>

      <div class="balance-layer" aria-hidden={scene.view !== 'balance' && scene.view !== 'modes'}>
        <div class="role-characters" aria-hidden="true">
          <div class="robot-character"><i></i><b></b><span></span></div>
          <div class="worker-character"><i></i><b></b><span></span></div>
        </div>
        <div class="balance-title">
          <span>Share of classified exposure</span>
          <strong>{overallBalance.automation}% <i>vs.</i> {overallBalance.augmentation}%</strong>
        </div>
        <div class="role-bar" aria-label={`${overallBalance.automation}% automation and ${overallBalance.augmentation}% augmentation`}>
          <span style:width={`${overallBalance.automation}%`}><strong>{overallBalance.automation}%</strong><small>AI executes</small></span>
          <span style:width={`${overallBalance.augmentation}%`}><strong>{overallBalance.augmentation}%</strong><small>Human + AI</small></span>
        </div>
      </div>

      <div class="mode-layer" aria-hidden={scene.view !== 'modes'}>
        <div class="mode-column automation-modes">
          <strong>Automation</strong>
          {#each interactionModes.filter((mode) => mode.side === 'automation') as mode, index}
            <div class="mode-card" style={`--delay:${index * 100}ms`}>
              <span>{mode.name}</span><b>{mode.value}%</b>
              <small>{mode.description}</small>
            </div>
          {/each}
        </div>
        <div class="mode-column augmentation-modes">
          <strong>Augmentation</strong>
          {#each interactionModes.filter((mode) => mode.side === 'augmentation') as mode, index}
            <div class="mode-card" style={`--delay:${index * 100}ms`}>
              <span>{mode.name}</span><b>{mode.value}%</b>
              <small>{mode.description}</small>
            </div>
          {/each}
        </div>
      </div>

      <p class="sr-only">
        Among 94.39 percent of exposure that could be classified, 43 percent is automation-oriented
        and 57 percent is augmentation-oriented.
      </p>
      <div class="paper-grain" aria-hidden="true"></div>
    </div>
  </div>

  <div class="steps">
    {#each steps as step, index}
      <article
        class:active={activeStep === index}
        class="step"
        data-step={index}
        bind:this={stepNodes[index]}
        aria-current={activeStep === index ? 'step' : undefined}
      >
        <div class="step-card">
          <span>{step.kicker}</span>
          <h2>{step.title}</h2>
          <p>{step.text}</p>
        </div>
      </article>
    {/each}
  </div>
</section>

<style>
  .scrolly { position: relative; max-width: 84rem; min-height: 100dvh; margin: 0 auto 8rem; }
  .sticky-scene { position: sticky; top: 2.5dvh; height: 95dvh; }
  .scene {
    position: relative;
    width: min(96vw, 82rem);
    height: 92dvh;
    min-height: 40rem;
    margin: 0 auto;
    overflow: hidden;
    border: 2px solid var(--ink);
    border-radius: 0;
    background: var(--paper);
    box-shadow: none;
    transition: background-color 700ms ease;
  }

  .scene.question { background: #d8ccdc; }
  .scene.balance,
  .scene.modes { background: #e4dce7; }

  .scene-heading {
    position: absolute;
    z-index: 12;
    top: 1.2rem;
    right: 1.4rem;
    left: 1.4rem;
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    color: var(--ink-soft);
    font-size: 0.68rem;
    font-weight: 850;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .scene-heading strong { color: var(--ink); text-align: right; }

  .task-field {
    position: absolute;
    z-index: 2;
    top: 12%;
    left: 5%;
    display: grid;
    grid-template-columns: repeat(10, minmax(0, 1fr));
    gap: clamp(0.35rem, 1vw, 0.75rem);
    width: min(38%, 31rem);
    opacity: 0;
    transform: translateX(-4rem) scale(0.92);
    transition: opacity 500ms ease, transform 800ms cubic-bezier(0.2, 0.75, 0.2, 1);
  }

  .tasks .task-field,
  .concentration .task-field { opacity: 1; transform: translateX(0) scale(1); }

  .task-field i {
    aspect-ratio: 1;
    border: 1.5px solid var(--ink);
    border-radius: 0.2rem;
    background: var(--pink-light);
    opacity: 0.92;
    transform: rotate(-2deg);
    transition: background-color 500ms ease var(--delay), opacity 500ms ease var(--delay), transform 650ms ease var(--delay);
  }

  .task-field i:nth-child(3n) { transform: rotate(2.5deg); }
  .task-field i:nth-child(4n) { border-radius: 50%; }
  .concentration .task-field i { opacity: 0.16; transform: scale(0.82); }
  .concentration .task-field i.top-five { background: var(--automation); opacity: 1; transform: scale(1.06); }

  .occupation-ranking {
    position: absolute;
    z-index: 4;
    top: 15%;
    right: 5%;
    width: min(44%, 34rem);
    opacity: 0;
    transform: translateX(3rem);
    transition: opacity 450ms ease, transform 700ms cubic-bezier(0.2, 0.75, 0.2, 1);
  }

  .concentration .occupation-ranking { opacity: 1; transform: translateX(0); }
  .occupation-ranking > p { margin: 0 0 1.3rem; color: var(--ink-soft); font-size: 0.72rem; font-weight: 850; letter-spacing: 0.08em; text-transform: uppercase; }
  .occupation-ranking > small { display: block; margin-top: 1.1rem; color: var(--plum); font-weight: 900; text-align: right; }

  .occupation-row {
    display: grid;
    grid-template-columns: minmax(8rem, 1.5fr) 1fr auto;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 0.85rem;
    opacity: 0;
    transform: translateY(0.7rem);
    transition: opacity 450ms ease var(--delay), transform 550ms ease var(--delay);
  }

  .concentration .occupation-row { opacity: 1; transform: translateY(0); }
  .occupation-row span { font-size: clamp(0.72rem, 1.4vw, 0.98rem); font-weight: 750; }
  .occupation-row > div { height: 0.7rem; overflow: hidden; border: 1px solid var(--ink); border-radius: 0; background: rgba(255,255,255,0.55); }
  .occupation-row > div i { display: block; height: 100%; background: var(--automation); }
  .occupation-row strong { font-size: 0.82rem; }

  .question-layer {
    position: absolute;
    z-index: 5;
    inset: 10% 8% 22%;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: clamp(1rem, 4vw, 3rem);
    opacity: 0;
    transform: scale(0.88);
    transition: opacity 400ms ease, transform 750ms cubic-bezier(0.2, 0.75, 0.2, 1);
  }

  .question .question-layer { opacity: 1; transform: scale(1); }
  .exposure-card,
  .role-card { display: grid; place-content: center; min-height: 14rem; padding: 1.4rem; border: 2px solid var(--ink); border-radius: 0; background: var(--cream-light); text-align: center; box-shadow: none; }
  .exposure-card span,
  .role-card span { color: var(--ink-soft); font-size: 0.72rem; font-weight: 850; letter-spacing: 0.08em; text-transform: uppercase; }
  .exposure-card strong,
  .role-card strong { max-width: 16rem; font-family: var(--display); font-size: clamp(1.7rem, 4vw, 3.4rem); line-height: 0.95; }
  .not-equal { font-family: var(--display); font-size: clamp(4rem, 10vw, 8rem); font-weight: 900; transform: rotate(-8deg); }

  .balance-layer {
    position: absolute;
    z-index: 5;
    inset: 13% 8% 25%;
    display: grid;
    align-content: center;
    opacity: 0;
    transform: translateY(2rem);
    transition: opacity 450ms ease, transform 800ms cubic-bezier(0.2, 0.75, 0.2, 1);
  }

  .balance .balance-layer,
  .modes .balance-layer { opacity: 1; transform: translateY(0); }
  .modes .balance-layer { inset: 10% 7% auto; transform: none; }
  .modes .role-characters,
  .modes .balance-title { display: none; }

  .balance-title { display: grid; justify-items: center; margin-bottom: 1.4rem; text-align: center; }
  .balance-title span { color: var(--ink-soft); font-size: 0.72rem; font-weight: 850; letter-spacing: 0.08em; text-transform: uppercase; }
  .balance-title strong { font-family: var(--display); font-size: clamp(2.7rem, 8vw, 6rem); letter-spacing: -0.04em; line-height: 0.9; }
  .balance-title i { color: var(--ink-soft); font-family: var(--sans); font-size: 0.2em; font-style: normal; text-transform: uppercase; }

  .role-bar { display: flex; height: clamp(5rem, 10vw, 7.5rem); overflow: hidden; border: 2px solid var(--ink); border-radius: 0; box-shadow: none; }
  .role-bar > span { display: grid; place-content: center; min-width: 0; text-align: center; transition: width 900ms cubic-bezier(0.2, 0.75, 0.2, 1); }
  .role-bar > span:first-child { background: var(--automation); }
  .role-bar > span:last-child { background: var(--augmentation); color: white; }
  .role-bar strong { font-family: var(--display); font-size: clamp(1.7rem, 5vw, 3.5rem); line-height: 0.8; }
  .role-bar small { margin-top: 0.4rem; font-size: clamp(0.58rem, 1.3vw, 0.78rem); font-weight: 850; letter-spacing: 0.06em; text-transform: uppercase; }
  .modes .role-bar { height: 2.9rem; }
  .modes .role-bar strong { font-family: var(--sans); font-size: 1rem; line-height: 1; }
  .modes .role-bar small { margin-top: 0.08rem; font-size: 0.52rem; }

  .role-characters { display: flex; justify-content: space-between; width: 72%; margin: 0 auto -1rem; }
  .robot-character,
  .worker-character { position: relative; width: 5rem; height: 5rem; }
  .robot-character i { position: absolute; inset: 1rem 0.4rem 0; border: 2px solid var(--ink); border-radius: 0.8rem; background: var(--automation); }
  .robot-character i::before,
  .robot-character i::after { position: absolute; top: 1rem; width: 0.45rem; height: 0.55rem; border-radius: 50%; background: var(--ink); content: ''; }
  .robot-character i::before { left: 1rem; }
  .robot-character i::after { right: 1rem; }
  .robot-character b { position: absolute; top: 0.25rem; left: 50%; width: 2px; height: 0.9rem; background: var(--ink); }
  .robot-character b::after { position: absolute; top: -0.2rem; left: -0.2rem; width: 0.45rem; height: 0.45rem; border: 2px solid var(--ink); border-radius: 50%; background: var(--gold); content: ''; }
  .worker-character i { position: absolute; top: 0.25rem; left: 1.25rem; width: 2.7rem; height: 2.7rem; border: 2px solid var(--ink); border-radius: 50%; background: #a85f35; }
  .worker-character i::before { position: absolute; inset: -0.35rem -0.3rem 1.35rem; border-radius: 1.2rem 1.2rem 0 0; background: var(--ink); content: ''; }
  .worker-character b { position: absolute; right: 0.5rem; bottom: 0; left: 0.5rem; height: 2.4rem; border: 2px solid var(--ink); border-radius: 1.2rem 1.2rem 0.4rem 0.4rem; background: var(--augmentation); }

  .mode-layer {
    position: absolute;
    z-index: 7;
    top: 24%;
    right: 7%;
    bottom: 23%;
    left: 7%;
    display: grid;
    grid-template-columns: 1fr 1.35fr;
    gap: 1rem;
    opacity: 0;
    transform: translateY(3rem);
    transition: opacity 500ms ease 180ms, transform 750ms cubic-bezier(0.2, 0.75, 0.2, 1) 180ms;
  }

  .modes .mode-layer { opacity: 1; transform: translateY(0); }
  .mode-column { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.55rem; align-content: start; }
  .augmentation-modes { grid-template-columns: repeat(3, 1fr); }
  .mode-column > strong { grid-column: 1 / -1; color: var(--ink-soft); font-size: 0.68rem; letter-spacing: 0.09em; text-transform: uppercase; }
  .mode-card { display: grid; align-content: start; min-height: 7.3rem; padding: 0.75rem; border: 1.5px solid var(--ink); border-radius: 0; background: var(--automation-pale); opacity: 0; transform: translateY(1rem) rotate(-1deg); transition: opacity 450ms ease var(--delay), transform 550ms ease var(--delay); }
  .augmentation-modes .mode-card { background: var(--augmentation-pale); }
  .modes .mode-card { opacity: 1; transform: translateY(0) rotate(0); }
  .mode-card span { font-size: 0.78rem; font-weight: 900; }
  .mode-card b { margin: 0.25rem 0; font-family: var(--display); font-size: clamp(1.4rem, 3vw, 2.2rem); }
  .mode-card small { color: var(--ink-soft); font-size: clamp(0.55rem, 1vw, 0.68rem); line-height: 1.25; }

  .paper-grain { position: absolute; z-index: 20; inset: 0; background-image: url('/assets/grain.png'); background-size: 34rem 34rem; opacity: 0.14; mix-blend-mode: multiply; pointer-events: none; }
  .steps { position: relative; z-index: 30; margin-top: -95dvh; pointer-events: none; }
  .step { display: flex; align-items: flex-end; justify-content: center; min-height: 92dvh; padding: 0 1rem 5dvh; opacity: 0.18; transition: opacity 320ms ease; }
  .step.active { opacity: 1; }
  .step-card { width: min(100%, 39rem); padding: 0.9rem 1.15rem; border: 0; border-radius: 0; background: rgba(10,9,11,0.91); color: white; box-shadow: none; pointer-events: auto; text-align: center; }
  .step-card > span { color: var(--pink-light); font-size: 0.62rem; font-weight: 900; letter-spacing: 0.09em; text-transform: uppercase; }
  .step-card h2 { margin: 0.25rem 0 0.45rem; color: white; font-family: var(--sans); font-size: clamp(1.25rem, 2.5vw, 1.85rem); font-weight: 700; letter-spacing: -0.02em; line-height: 1.08; }
  .step-card p { margin: 0; color: rgba(255,255,255,0.78); font-size: clamp(0.78rem, 1.4vw, 0.92rem); line-height: 1.38; }

  @media (max-width: 720px) {
    .scrolly { margin-bottom: 5rem; }
    .sticky-scene { top: 7dvh; height: 86dvh; }
    .scene { width: 95vw; height: 82dvh; min-height: 34rem; border-radius: 0; box-shadow: none; }
    .steps { margin-top: -86dvh; }
    .step { min-height: 84dvh; padding-bottom: 2.5dvh; }
    .step-card { padding: 0.75rem 0.85rem; box-shadow: none; }
    .step-card p { display: none; }
    .task-field { top: 14%; left: 7%; width: 86%; gap: 0.32rem; }
    .occupation-ranking { top: 14%; right: 7%; left: 7%; width: auto; }
    .concentration .task-field { opacity: 0; transform: translateX(-2rem) scale(0.9); }
    .occupation-row { grid-template-columns: minmax(7rem, 1.5fr) 0.8fr auto; margin-bottom: 0.58rem; }
    .question-layer { inset: 11% 6% 22%; grid-template-columns: 1fr; gap: 0.6rem; }
    .exposure-card,
    .role-card { min-height: 7rem; }
    .not-equal { position: absolute; z-index: 2; top: 50%; left: 50%; padding: 0 0.5rem; background: #d8ccdc; font-size: 3.5rem; transform: translate(-50%, -50%) rotate(-8deg); }
    .balance-layer { inset: 15% 6% 24%; }
    .modes .balance-layer { inset: 10% 4% auto; transform: none; }
    .role-characters { width: 84%; }
    .mode-layer { top: 23%; right: 4%; bottom: 22%; left: 4%; grid-template-columns: 1fr 1.35fr; gap: 0.45rem; }
    .mode-column,
    .augmentation-modes { gap: 0.28rem; }
    .mode-card { min-height: 6.1rem; padding: 0.42rem; }
    .mode-card small { display: none; }
    .scene-heading { top: 0.75rem; right: 0.8rem; left: 0.8rem; font-size: 0.55rem; }
  }

  @media (max-height: 720px) {
    .scene { min-height: 0; }
    .mode-card { min-height: 5.6rem; padding: 0.45rem; }
    .mode-card small { display: none; }
    .step { padding-bottom: 2dvh; }
  }

  @media (prefers-reduced-motion: reduce) {
    .scene,
    .task-field,
    .task-field i,
    .occupation-ranking,
    .occupation-row,
    .question-layer,
    .balance-layer,
    .mode-layer,
    .mode-card,
    .step { transition-duration: 0.01ms; transition-delay: 0ms; }
  }
</style>
