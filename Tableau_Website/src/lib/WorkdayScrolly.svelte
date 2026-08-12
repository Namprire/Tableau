<script>
  import { onMount } from 'svelte';
  import { qaTasks } from './storyData';

  const steps = [
    {
      kicker: 'Open the job',
      title: 'Meet Maya, a fictional software QA engineer.',
      text: 'Her character is illustrative, but every task and value comes from the occupation–task data.'
    },
    {
      kicker: 'Task one',
      title: 'Finding a breakdown leans toward execution.',
      text: 'When AI is used to review logs, configuration files, or code for a failure source, the task is 57% automation-oriented.'
    },
    {
      kicker: 'Task two',
      title: 'Usability feedback leans strongly toward collaboration.',
      text: 'When AI helps recommend improvements to developers, 79% of the classified interaction is augmentation-oriented.'
    },
    {
      kicker: 'The job black box',
      title: 'One occupation contains both roles.',
      text: 'These two tasks have similar exposure, yet AI behaves differently in each. The task—not the job title—is the revealing unit.'
    }
  ];

  const scenes = ['intro', 'debug', 'feedback', 'compare'];
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

<section class="workday-scrolly" aria-label="Two AI roles inside software quality assurance">
  <div class="sticky-wrap">
    <div class:intro={scene === 'intro'} class:debug={scene === 'debug'} class:feedback={scene === 'feedback'} class:compare={scene === 'compare'} class="workday-scene">
      <img
        class="hero-art"
        src="/assets/story/ai-work-hero-money-palette.png"
        alt="Illustrated software quality-assurance worker and a friendly AI robot sorting task cards together"
        loading="lazy"
        decoding="async"
      />
      <div class="wash" aria-hidden="true"></div>

      <div class="job-label">
        <span>Occupation</span>
        <strong>Software quality assurance engineers & testers</strong>
        <small>1.76% of measured exposure · 59% augmentation overall</small>
      </div>

      <div class="debug-spotlight" aria-hidden="true"><i></i></div>
      <div class="feedback-spotlight" aria-hidden="true"><i></i></div>

      {#each qaTasks as task, index}
        <article class:active={(scene === 'debug' && index === 0) || (scene === 'feedback' && index === 1) || scene === 'compare'} class="task-card" class:debug-card={index === 0} class:feedback-card={index === 1}>
          <div class="card-top">
            <span>{index === 0 ? 'Task A' : 'Task B'}</span>
            <strong>{task.exposure.toFixed(3)}%</strong>
          </div>
          <h3>{task.short}</h3>
          <p>{task.name}</p>
          <div class="task-balance" aria-label={`${task.automation}% automation and ${task.augmentation}% augmentation`}>
            <span style:width={`${task.automation}%`}><b>{Math.round(task.automation)}%</b><small>AI executes</small></span>
            <span style:width={`${task.augmentation}%`}><b>{Math.round(task.augmentation)}%</b><small>Human + AI</small></span>
          </div>
          <div class:automation={task.leaning === 'automation'} class="lean-label">
            Leans {task.leaning}
          </div>
        </article>
      {/each}

      <div class="comparison-line" aria-hidden="true">
        <span>Similar exposure</span><i></i><strong>Different role</strong>
      </div>
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
  .workday-scrolly { position: relative; max-width: 84rem; margin: 0 auto 8rem; }
  .sticky-wrap { position: sticky; top: 2.5dvh; height: 95dvh; }
  .workday-scene {
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
  }

  .hero-art {
    position: absolute;
    z-index: 1;
    inset: 0;
    width: 100%;
    height: 100%;
    max-width: none;
    object-fit: cover;
    object-position: center;
    transform: scale(1.02);
    transition: filter 650ms ease, opacity 500ms ease, transform 850ms cubic-bezier(0.2, 0.75, 0.2, 1);
  }

  .debug .hero-art { filter: saturate(0.72) sepia(0.08); transform: scale(1.09) translateX(3%); }
  .feedback .hero-art { filter: saturate(0.78) sepia(0.04); transform: scale(1.08) translateX(-3%); }
  .compare .hero-art { filter: saturate(0.42); opacity: 0.34; transform: scale(1.02); }

  .wash {
    position: absolute;
    z-index: 2;
    inset: 0;
    background: linear-gradient(to bottom, rgba(238,232,240,0.02), rgba(238,232,240,0.38));
    transition: background 500ms ease;
  }

  .debug .wash { background: linear-gradient(90deg, rgba(173,10,134,0.16), rgba(238,232,240,0.68) 64%); }
  .feedback .wash { background: linear-gradient(270deg, rgba(101,201,154,0.17), rgba(238,232,240,0.66) 64%); }
  .compare .wash { background: rgba(238,232,240,0.55); }

  .job-label {
    position: absolute;
    z-index: 8;
    top: 1.3rem;
    left: 1.4rem;
    display: grid;
    max-width: 30rem;
    padding: 0.7rem 0.85rem;
    border: 1.5px solid var(--ink);
    border-radius: 0;
    background: rgba(247,242,248,0.95);
    box-shadow: none;
    transition: opacity 400ms ease, transform 650ms ease;
  }

  .compare .job-label { opacity: 0; transform: translateY(-1rem); }
  .job-label span { color: var(--plum); font-size: 0.58rem; font-weight: 900; letter-spacing: 0.09em; text-transform: uppercase; }
  .job-label strong { font-family: var(--display); font-size: clamp(1rem, 2vw, 1.35rem); line-height: 1; }
  .job-label small { margin-top: 0.25rem; color: var(--ink-soft); font-size: 0.65rem; }

  .task-card {
    position: absolute;
    z-index: 7;
    width: min(38vw, 29rem);
    padding: 1rem;
    border: 2px solid var(--ink);
    border-radius: 0;
    background: rgba(247,242,248,0.97);
    box-shadow: none;
    opacity: 0;
    will-change: transform, opacity;
    transition: opacity 450ms ease, transform 780ms cubic-bezier(0.2, 0.75, 0.2, 1);
  }

  .debug-card { top: 22%; right: 7%; transform: translateX(4rem) rotate(2deg) scale(0.92); }
  .feedback-card { top: 22%; left: 7%; transform: translateX(-4rem) rotate(-2deg) scale(0.92); }
  .debug .debug-card,
  .feedback .feedback-card { opacity: 1; transform: translateX(0) rotate(0) scale(1); }

  .compare .task-card { top: 19%; width: min(41vw, 31rem); opacity: 1; transform: translate(0, 0) rotate(0) scale(1); }
  .compare .debug-card { right: auto; left: 5%; }
  .compare .feedback-card { right: 5%; left: auto; }

  .card-top { display: flex; justify-content: space-between; color: var(--ink-soft); font-size: 0.64rem; font-weight: 900; letter-spacing: 0.07em; text-transform: uppercase; }
  .card-top strong { color: var(--plum); }
  .task-card h3 { margin: 0.7rem 0 0.45rem; font-family: var(--display); font-size: clamp(1.25rem, 2.5vw, 2.15rem); letter-spacing: -0.03em; line-height: 1; }
  .task-card p { display: -webkit-box; margin: 0 0 1rem; overflow: hidden; color: var(--ink-soft); font-size: clamp(0.7rem, 1.3vw, 0.88rem); line-height: 1.4; -webkit-box-orient: vertical; -webkit-line-clamp: 3; line-clamp: 3; }

  .task-balance { display: flex; height: 4rem; overflow: hidden; border: 1.5px solid var(--ink); border-radius: 0; }
  .task-balance span { display: grid; place-content: center; min-width: 0; text-align: center; }
  .task-balance span:first-child { background: var(--automation); }
  .task-balance span:last-child { background: var(--augmentation); color: white; }
  .task-balance b { font-family: var(--display); font-size: clamp(1.15rem, 2.5vw, 1.8rem); line-height: 0.8; }
  .task-balance small { margin-top: 0.3rem; font-size: 0.5rem; font-weight: 900; letter-spacing: 0.05em; text-transform: uppercase; }
  .lean-label { width: fit-content; margin: 0.75rem 0 0 auto; padding: 0.28rem 0.55rem; border-radius: 0; background: var(--augmentation-pale); color: var(--augmentation-dark); font-size: 0.62rem; font-weight: 900; text-transform: uppercase; }
  .lean-label.automation { margin-right: auto; margin-left: 0; background: var(--automation-pale); color: var(--automation-dark); }

  .debug-spotlight,
  .feedback-spotlight { position: absolute; z-index: 4; opacity: 0; transition: opacity 500ms ease, transform 700ms ease; }
  .debug-spotlight { top: 31%; left: 4%; width: 29%; height: 32%; border: 4px solid var(--automation); border-radius: 0; box-shadow: 0 0 0 999px rgba(238,232,240,0.23); transform: rotate(-2deg) scale(0.9); }
  .feedback-spotlight { top: 31%; right: 8%; width: 28%; height: 35%; border: 4px solid var(--augmentation); border-radius: 50%; transform: rotate(2deg) scale(0.9); }
  .debug .debug-spotlight,
  .feedback .feedback-spotlight { opacity: 1; transform: rotate(0) scale(1); }

  .comparison-line {
    position: absolute;
    z-index: 9;
    right: 22%;
    bottom: 32%;
    left: 22%;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 0.8rem;
    color: var(--ink-soft);
    font-size: 0.65rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    opacity: 0;
    text-transform: uppercase;
    transform: translateY(1rem);
    transition: opacity 450ms ease 250ms, transform 600ms ease 250ms;
  }

  .compare .comparison-line { opacity: 1; transform: translateY(0); }
  .comparison-line i { height: 2px; background: var(--ink); }
  .comparison-line strong { color: var(--plum); }

  .paper-grain { position: absolute; z-index: 20; inset: 0; background-image: url('/assets/grain.png'); background-size: 34rem 34rem; opacity: 0.11; pointer-events: none; }
  .steps { position: relative; z-index: 30; margin-top: -95dvh; pointer-events: none; }
  .step { display: flex; align-items: flex-end; justify-content: center; min-height: 92dvh; padding: 0 1rem 5dvh; opacity: 0.16; transition: opacity 320ms ease; }
  .step.active { opacity: 1; }
  .step-card { width: min(100%, 39rem); padding: 0.9rem 1.15rem; border: 0; border-radius: 0; background: rgba(10,9,11,0.91); color: white; box-shadow: none; pointer-events: auto; text-align: center; }
  .step-card > span { color: var(--pink-light); font-size: 0.62rem; font-weight: 900; letter-spacing: 0.09em; text-transform: uppercase; }
  .step-card h2 { margin: 0.25rem 0 0.45rem; color: white; font-family: var(--sans); font-size: clamp(1.25rem, 2.5vw, 1.85rem); font-weight: 700; letter-spacing: -0.02em; line-height: 1.08; }
  .step-card p { margin: 0; color: rgba(255,255,255,0.78); font-size: clamp(0.78rem, 1.4vw, 0.92rem); line-height: 1.38; }

  @media (max-width: 720px) {
    .workday-scrolly { margin-bottom: 5rem; }
    .sticky-wrap { top: 7dvh; height: 86dvh; }
    .workday-scene { width: 95vw; height: 82dvh; min-height: 34rem; border-radius: 0; box-shadow: none; }
    .hero-art { object-position: 52% center; }
    .job-label { top: 0.75rem; left: 0.75rem; max-width: calc(100% - 1.5rem); padding: 0.5rem 0.65rem; }
    .job-label small { display: none; }
    .task-card,
    .compare .task-card { right: 4%; left: 4%; width: auto; }
    .debug-card,
    .feedback-card { top: 17%; }
    .compare .debug-card { top: 13%; }
    .compare .feedback-card { top: 45%; }
    .task-card p { display: none; }
    .task-balance { height: 3.25rem; }
    .comparison-line { right: 8%; bottom: 29%; left: 8%; }
    .debug-spotlight,
    .feedback-spotlight { display: none; }
    .steps { margin-top: -86dvh; }
    .step { min-height: 84dvh; padding-bottom: 2.5dvh; }
    .step-card { padding: 0.75rem 0.85rem; box-shadow: none; }
    .step-card p { display: none; }
  }

  @media (max-height: 720px) {
    .workday-scene { min-height: 0; }
    .task-card { padding: 0.7rem; }
    .task-card p { display: none; }
    .step { padding-bottom: 2dvh; }
  }

  @media (prefers-reduced-motion: reduce) {
    .hero-art,
    .wash,
    .job-label,
    .task-card,
    .debug-spotlight,
    .feedback-spotlight,
    .comparison-line,
    .step { transition-duration: 0.01ms; transition-delay: 0ms; }
  }
</style>
