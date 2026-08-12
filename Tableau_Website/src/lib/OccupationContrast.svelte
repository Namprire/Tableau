<script>
  import { occupationContrast } from './storyData';
</script>

<section class="contrast" aria-labelledby="contrast-title">
  <header>
    <p class="eyebrow">Same amount, different use</p>
    <h2 id="contrast-title">Similar exposure does not produce the same AI role.</h2>
    <p>
      These occupations have almost the same measured exposure, but their observed interactions sit
      on opposite sides of the worker–copilot spectrum.
    </p>
  </header>

  <div class="contrast-grid">
    {#each occupationContrast as occupation, index}
      <article class:automation-card={index === 0} class="occupation-card">
        <div class="illustration" aria-hidden="true">
          {#if occupation.setting === 'stage'}
            <svg viewBox="0 0 220 170">
              <path class="curtain" d="M8 10h55v148H8c24-32 27-64 0-96zM212 10h-55v148h55c-24-32-27-64 0-96z" />
              <path class="stage" d="M53 143h114v15H53z" />
              <circle class="head" cx="110" cy="67" r="24" />
              <path class="body" d="M68 142c4-41 20-59 42-59s38 18 42 59z" />
              <path class="mask" d="M88 62c7-5 15-6 22-2-1 17-9 26-23 28-6-9-6-18 1-26zm44 0c-7-5-15-6-22-2 1 17 9 26 23 28 6-9 6-18-1-26z" />
            </svg>
          {:else}
            <svg viewBox="0 0 220 170">
              <path class="shelf" d="M15 139h190v14H15z" />
              <circle class="head" cx="74" cy="61" r="24" />
              <path class="body" d="M36 141c4-43 17-62 38-62s35 19 39 62z" />
              <path class="flask" d="M139 30h24v9h-4v33l31 53c5 9-2 16-12 16h-58c-10 0-17-7-12-16l31-53V39h-4v-9z" />
              <path class="liquid" d="M121 112h56l12 21H109z" />
              <circle class="bubble" cx="166" cy="96" r="5" />
              <circle class="bubble" cx="145" cy="87" r="4" />
            </svg>
          {/if}
        </div>

        <div class="card-copy">
          <span class="exposure-pill">{occupation.exposure.toFixed(2)}% exposure</span>
          <h3>{occupation.name}</h3>
          <div class="spectrum-labels"><span>AI executes</span><span>Human + AI</span></div>
          <div class="spectrum" aria-label={`${occupation.automation}% automation and ${occupation.augmentation}% augmentation`}>
            <span style:width={`${occupation.automation}%`}></span>
            <span style:width={`${occupation.augmentation}%`}></span>
          </div>
          <p>
            <strong>{Math.round(Math.max(occupation.automation, occupation.augmentation))}%</strong>
            {occupation.automation > occupation.augmentation ? 'automation-oriented' : 'augmentation-oriented'}
          </p>
        </div>
      </article>
    {/each}
  </div>

  <p class="caveat">
    Role balance describes the observed type of AI interaction. It is not a forecast of job loss or
    a causal effect of AI.
  </p>
</section>

<style>
  .contrast { width: min(100% - 2rem, 72rem); margin: 0 auto 9rem; }
  header { max-width: 47rem; margin: 0 auto 3rem; text-align: center; }
  .eyebrow { margin: 0 0 0.7rem; color: var(--plum); font-size: 0.7rem; font-weight: 900; letter-spacing: 0.1em; text-transform: uppercase; }
  h2 { margin: 0; font-family: var(--display); font-size: clamp(2.2rem, 6vw, 4.6rem); font-weight: 950; letter-spacing: -0.055em; line-height: 0.9; text-transform: uppercase; }
  header > p:last-child { max-width: 40rem; margin: 1.2rem auto 0; color: var(--ink-soft); line-height: 1.55; }
  .contrast-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.3rem; }
  .occupation-card { display: grid; grid-template-columns: 0.82fr 1.18fr; min-height: 25rem; overflow: hidden; border: 2px solid var(--ink); border-radius: 0; background: var(--augmentation-pale); box-shadow: none; }
  .occupation-card.automation-card { background: var(--automation-pale); }
  .illustration { display: grid; place-items: center; padding: 1rem; border-right: 2px solid var(--ink); background: rgba(255,255,255,0.36); }
  .illustration svg { width: 100%; overflow: visible; }
  .curtain { fill: var(--automation-dark); stroke: var(--ink); stroke-width: 3; }
  .stage, .shelf { fill: var(--gold); stroke: var(--ink); stroke-width: 3; }
  .head { fill: #a85f35; stroke: var(--ink); stroke-width: 3; }
  .body { fill: var(--plum); stroke: var(--ink); stroke-width: 3; }
  .mask { fill: var(--cream-light); stroke: var(--ink); stroke-width: 2.5; }
  .flask { fill: var(--cream-light); stroke: var(--ink); stroke-width: 3; }
  .liquid, .bubble { fill: var(--augmentation); stroke: var(--ink); stroke-width: 2.5; }
  .card-copy { display: flex; flex-direction: column; justify-content: center; padding: clamp(1.2rem, 3vw, 2.2rem); }
  .exposure-pill { width: fit-content; padding: 0.35rem 0.58rem; border: 1.5px solid var(--ink); border-radius: 0; background: var(--cream-light); font-size: 0.66rem; font-weight: 900; text-transform: uppercase; }
  h3 { margin: 1rem 0 auto; font-family: var(--display); font-size: clamp(1.6rem, 3vw, 2.6rem); font-weight: 900; letter-spacing: -0.045em; line-height: 0.92; }
  .spectrum-labels { display: flex; justify-content: space-between; margin-top: 2rem; color: var(--ink-soft); font-size: 0.58rem; font-weight: 900; text-transform: uppercase; }
  .spectrum { display: flex; height: 1.5rem; margin-top: 0.35rem; overflow: hidden; border: 1.5px solid var(--ink); border-radius: 0; background: white; }
  .spectrum span:first-child { background: var(--automation); }
  .spectrum span:last-child { background: var(--augmentation); }
  .card-copy > p { margin: 0.7rem 0 0; color: var(--ink-soft); font-size: 0.78rem; }
  .card-copy > p strong { color: var(--ink); }
  .caveat { max-width: 48rem; margin: 1.8rem auto 0; color: var(--ink-soft); font-size: 0.76rem; line-height: 1.45; text-align: center; }

  @media (max-width: 980px) {
    .contrast-grid { grid-template-columns: 1fr; }
    .occupation-card { min-height: 21rem; }
  }

  @media (max-width: 500px) {
    .occupation-card { grid-template-columns: 1fr; }
    .illustration { max-height: 13rem; border-right: 0; border-bottom: 2px solid var(--ink); }
    .illustration svg { max-height: 11rem; }
    h3 { margin-bottom: 1rem; }
  }
</style>
