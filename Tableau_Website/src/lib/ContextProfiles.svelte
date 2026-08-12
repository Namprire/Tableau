<script>
  import { onMount } from 'svelte';
  import { familyProfiles, zoneProfiles } from './storyData';

  let root;
  let visible = false;

  onMount(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry?.isIntersecting) return;
        visible = true;
        observer.disconnect();
      },
      { threshold: 0.18 }
    );

    if (root) observer.observe(root);
    return () => observer.disconnect();
  });
</script>

<section bind:this={root} class:visible class="context" aria-labelledby="context-title">
  <header>
    <p class="eyebrow">Occupational context</p>
    <h2 id="context-title">The balance changes with the structure of work.</h2>
    <p>
      Human-facing and highly specialized work is more augmentation-oriented in this descriptive
      sample. Technical work with the most exposure sits much closer to an even split.
    </p>
  </header>

  <div class="context-grid">
    <figure class="families">
      <figcaption>
        <strong>AI role by job family</strong>
        <span>Exposure-weighted share of classified interactions</span>
      </figcaption>

      <div class="legend" aria-hidden="true"><span>AI executes</span><span>Human + AI</span></div>
      {#each familyProfiles as family, index}
        <div class="family-row" style={`--delay:${index * 70}ms`}>
          <div class="family-name"><strong>{family.name}</strong><small>{family.exposure.toFixed(2)}% classified exposure</small></div>
          <div class="family-bar" aria-label={`${family.automation}% automation and ${family.augmentation}% augmentation`}>
            <span style={`--target-width:${family.automation}%`}></span>
            <span style={`--target-width:${family.augmentation}%`}></span>
          </div>
          <b>{Math.round(family.augmentation)}%</b>
        </div>
      {/each}
    </figure>

    <figure class="zones">
      <figcaption>
        <strong>Augmentation by preparation level</strong>
        <span>Job Zones 2–5; Zone 1 omitted because classified exposure is only 0.11%</span>
      </figcaption>

      <div class="zone-stack">
        {#each zoneProfiles as zone, index}
          <div class="zone-card" style={`--height:${zone.augmentation}%;--delay:${index * 100}ms`}>
            <div class="zone-meta">
              <span>Zone {zone.zone}</span>
              <small>{zone.label}</small>
            </div>
            <div class="zone-fill">
              <strong>{zone.augmentation}%</strong>
            </div>
          </div>
        {/each}
      </div>
      <p>
        Zone 5 work is 68.3% augmentation-oriented, compared with roughly 53–55% for Zones 2–4.
        This is an association, not evidence that preparation level causes AI to take a particular role.
      </p>
    </figure>
  </div>
</section>

<style>
  .context { width: min(100% - 2rem, 76rem); margin: 0 auto 9rem; }
  header { max-width: 48rem; margin-bottom: 2.7rem; }
  .eyebrow { margin: 0 0 0.7rem; color: var(--plum); font-size: 0.7rem; font-weight: 900; letter-spacing: 0.1em; text-transform: uppercase; }
  h2 { margin: 0; font-family: var(--display); font-size: clamp(2.2rem, 6vw, 4.5rem); font-weight: 950; letter-spacing: -0.055em; line-height: 0.9; text-transform: uppercase; }
  header > p:last-child { max-width: 42rem; margin: 1.2rem 0 0; color: var(--ink-soft); line-height: 1.55; }
  .context-grid { display: grid; grid-template-columns: 1.25fr 0.75fr; gap: 1.2rem; }
  figure { margin: 0; padding: clamp(1rem, 3vw, 2rem); border: 2px solid var(--ink); border-radius: 0; background: var(--cream-light); box-shadow: none; }
  figcaption { display: grid; margin-bottom: 1.2rem; }
  figcaption strong { font-family: var(--display); font-size: clamp(1.35rem, 3vw, 2rem); font-weight: 850; letter-spacing: -0.035em; }
  figcaption span { margin-top: 0.25rem; color: var(--ink-soft); font-size: 0.7rem; line-height: 1.3; }
  .legend { display: flex; justify-content: space-between; margin: 0 3rem 0.55rem min(42%, 13rem); color: var(--ink-soft); font-size: 0.57rem; font-weight: 900; text-transform: uppercase; }
  .family-row { display: grid; grid-template-columns: minmax(9rem, 0.85fr) 1.2fr 2.3rem; align-items: center; gap: 0.65rem; margin-bottom: 0.75rem; opacity: 0; transform: translateY(0.8rem); transition: opacity 500ms ease var(--delay), transform 600ms ease var(--delay); }
  .visible .family-row { opacity: 1; transform: translateY(0); }
  .family-name { display: grid; }
  .family-name strong { font-size: clamp(0.65rem, 1.25vw, 0.82rem); line-height: 1.15; }
  .family-name small { margin-top: 0.15rem; color: var(--ink-soft); font-size: 0.53rem; }
  .family-bar { display: flex; height: 1.35rem; overflow: hidden; border: 1px solid var(--ink); border-radius: 0; background: white; }
  .family-bar span { width: 0; transition: width 950ms cubic-bezier(0.2, 0.75, 0.2, 1) var(--delay); }
  .visible .family-bar span { width: var(--target-width); }
  .family-bar span:first-child { background: var(--automation); }
  .family-bar span:last-child { background: var(--augmentation); }
  .family-row > b { color: var(--augmentation-dark); font-size: 0.72rem; text-align: right; }

  .zone-stack { display: grid; grid-template-columns: repeat(4, 1fr); align-items: end; gap: 0.55rem; min-height: 20rem; padding-top: 1rem; border-bottom: 2px solid var(--ink); }
  .zone-card { position: relative; min-height: 18rem; overflow: hidden; border: 1.5px solid var(--ink); border-bottom: 0; border-radius: 0; background: #e4dce7; opacity: 0; transform: translateY(1rem); transition: opacity 500ms ease var(--delay), transform 600ms ease var(--delay); }
  .visible .zone-card { opacity: 1; transform: translateY(0); }
  .zone-fill { position: absolute; right: 0; bottom: 0; left: 0; display: grid; height: 0; place-items: center; overflow: hidden; background: var(--augmentation); transition: height 1000ms cubic-bezier(0.2, 0.75, 0.2, 1) var(--delay); }
  .visible .zone-fill { height: var(--height); }
  .zone-meta { position: absolute; z-index: 2; top: 0.7rem; right: 0.4rem; left: 0.4rem; display: grid; text-align: center; }
  .zone-meta span { font-size: 0.58rem; font-weight: 900; text-transform: uppercase; }
  .zone-meta small { margin-top: 0.2rem; color: var(--ink-soft); font-size: 0.5rem; line-height: 1.1; }
  .zone-fill strong { color: var(--ink); font-family: var(--display); font-size: clamp(1rem, 2.4vw, 1.75rem); font-weight: 900; opacity: 0; white-space: nowrap; transition: opacity 350ms ease calc(var(--delay) + 500ms); }
  .visible .zone-fill strong { opacity: 1; }
  .zones > p { margin: 1rem 0 0; color: var(--ink-soft); font-size: 0.7rem; line-height: 1.4; }

  @media (max-width: 1080px) {
    .context-grid { grid-template-columns: 1fr; }
    .zones { order: -1; }
  }

  @media (max-width: 680px) {
    .family-row { grid-template-columns: minmax(0, 1fr) 2.4rem; gap: 0.35rem 0.55rem; margin-bottom: 1.15rem; }
    .family-name { grid-column: 1 / -1; }
    .family-bar { grid-column: 1; }
    .family-row > b { grid-column: 2; }
    .legend { display: none; }
    .zone-stack { gap: 0.25rem; }
    .zone-card { min-height: 15rem; }
    .zone-meta small { display: none; }
    .zone-fill strong { font-size: clamp(0.82rem, 3.5vw, 1.2rem); }
  }

  @media (prefers-reduced-motion: reduce) {
    .family-row,
    .family-bar span,
    .zone-card,
    .zone-fill,
    .zone-fill strong { transition-duration: 0.01ms; transition-delay: 0ms; }
  }
</style>
