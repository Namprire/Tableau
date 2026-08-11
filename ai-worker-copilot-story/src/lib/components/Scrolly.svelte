<script lang="ts">
  import { onMount } from 'svelte';
  import StoryGraphic from './StoryGraphic.svelte';

  export let zones: any[] = [];
  export let families: any[] = [];
  export let salary: any = { quartiles: [], q4Zones: [] };

  let activeScene = 0;
  let steps: HTMLElement[] = [];

  const scenes = [
    {
      eyebrow: 'The concentration',
      title: 'AI exposure is a high-preparation story.',
      copy: 'Job Zones 4 and 5 account for 77% of observed occupation exposure. A typical Zone 5 occupation is exposed about eleven times as much as one in Zone 1.',
      takeaway: 'Exposure is not the same as replacement—it tells us where people are using AI.'
    },
    {
      eyebrow: 'The divide',
      title: 'The worker side is narrow. The copilot side is broader.',
      copy: 'Computing alone accounts for about 40% of exposure and sits almost exactly between worker and copilot. Education, science, business, and healthcare lean more clearly toward copilot use.',
      takeaway: 'Production leans worker, but contributes only about 2% of total exposure.'
    },
    {
      eyebrow: 'The wrong shortcut',
      title: 'Higher salary does not automatically mean copilot.',
      copy: 'The highest salary quartile contains nearly half of classified exposure. Yet it is only 54% copilot overall—not the strongest copilot-oriented salary group.',
      takeaway: 'Salary tells us where much of the exposure sits, but not why AI takes a particular role.'
    },
    {
      eyebrow: 'The explanation',
      title: 'Look inside the salary group and the answer changes.',
      copy: 'Within the highest salary quartile, Zone 4 supplies 80% of exposure and is nearly balanced. Zone 5 contributes 19%, but is 69% copilot.',
      takeaway: 'The composition of work—and ultimately the task—matters more than a salary label alone.'
    }
  ];

  onMount(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) activeScene = Number((visible.target as HTMLElement).dataset.scene);
      },
      { threshold: [0.35, 0.55, 0.75], rootMargin: '-15% 0px -25% 0px' }
    );
    steps.forEach((step) => observer.observe(step));
    return () => observer.disconnect();
  });
</script>

<section id="story" class="story section-shell" aria-label="The evidence">
  <div class="story-heading">
    <p class="section-index">Follow the evidence</p>
    <h2>One question leads to the next.</h2>
  </div>

  <div class="scrolly">
    <div class="steps">
      {#each scenes as item, index}
        <article
          class:active={activeScene === index}
          class="step"
          data-scene={index}
          bind:this={steps[index]}
        >
          <p class="eyebrow">{item.eyebrow}</p>
          <h3>{item.title}</h3>
          <p>{item.copy}</p>
          <p class="takeaway">{item.takeaway}</p>
        </article>
      {/each}
    </div>

    <div class="graphic" aria-live="polite">
      <StoryGraphic scene={activeScene} {zones} {families} {salary} />
    </div>
  </div>
</section>

<style>
  .story { padding-top: 7rem; padding-bottom: 7rem; }
  .story-heading { max-width: 55rem; margin-bottom: 4rem; }
  .section-index { color: var(--worker); font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }
  .story-heading h2 { margin: 0.7rem 0 0; font-family: var(--display); font-size: clamp(2.8rem, 6vw, 6rem); font-weight: 520; letter-spacing: -0.055em; line-height: 0.95; }
  .scrolly { display: grid; grid-template-columns: minmax(18rem, 0.72fr) minmax(32rem, 1.28fr); gap: clamp(2rem, 6vw, 7rem); align-items: start; }
  .steps { padding-bottom: 30vh; }
  .step { min-height: 82vh; display: flex; flex-direction: column; justify-content: center; opacity: 0.28; transition: opacity 260ms ease; }
  .step.active { opacity: 1; }
  .eyebrow { margin: 0 0 1rem; color: var(--gold-dark); font-size: 0.72rem; font-weight: 800; letter-spacing: 0.13em; text-transform: uppercase; }
  h3 { margin: 0 0 1.3rem; font-family: var(--display); font-size: clamp(2.2rem, 4vw, 4.2rem); font-weight: 520; letter-spacing: -0.045em; line-height: 1; }
  .step > p:not(.eyebrow, .takeaway) { max-width: 36rem; margin: 0; color: var(--muted-dark); font-size: 1.08rem; line-height: 1.65; }
  .takeaway { max-width: 34rem; margin: 1.8rem 0 0; padding: 1.1rem 0 0 1.1rem; border-left: 2px solid var(--gold); color: var(--ink); font-size: 0.92rem; font-weight: 650; line-height: 1.5; }
  .graphic { position: sticky; top: 6vh; min-height: 75vh; display: flex; align-items: center; border-top: 1px solid var(--line-strong); border-bottom: 1px solid var(--line-strong); background: var(--paper); }
  @media (max-width: 900px) {
    .scrolly { grid-template-columns: 1fr; }
    .graphic { grid-row: 1; top: 0; z-index: 4; min-height: 48vh; box-shadow: 0 12px 24px rgba(23, 35, 54, 0.08); }
    .steps { grid-row: 2; padding-bottom: 0; }
    .step { min-height: 70vh; max-width: 38rem; margin-inline: auto; padding: 2rem 1rem; opacity: 0.2; }
  }
</style>
