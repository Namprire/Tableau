<script lang="ts">
  export let zonesShare = 0.77;
  export let taskRows = 3963;
  export let occupations = 731;
</script>

<header class="hero section-shell">
  <nav class="eyebrow" aria-label="Story context">
    <span>Human × AI</span>
    <span class="rule"></span>
    <span>Workplace interactions</span>
  </nav>

  <div class="hero-grid">
    <div>
      <p class="kicker">Who is doing the work?</p>
      <h1>AI can be the worker and the copilot—<em>even within the same job.</em></h1>
      <p class="dek">
        We analyzed {taskRows.toLocaleString('en-US')} workplace-task observations across
        {occupations} occupations to see where AI executes work, where it supports people,
        and why salary alone does not explain the difference.
      </p>
      <a class="start" href="#story">Follow the evidence <span aria-hidden="true">↓</span></a>
    </div>

    <aside class="hero-stat" aria-label="Headline finding">
      <span class="stat-number">{Math.round(zonesShare * 100)}%</span>
      <span class="stat-copy">of observed occupation AI exposure comes from jobs requiring high or extensive preparation.</span>
    </aside>
  </div>
</header>

<style>
  .hero {
    min-height: 94vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-top: 2rem;
    padding-bottom: 4rem;
  }

  .eyebrow {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.13em;
    text-transform: uppercase;
  }

  .rule {
    width: 3.5rem;
    height: 1px;
    background: var(--line-strong);
  }

  .hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(16rem, 0.65fr);
    align-items: end;
    gap: clamp(3rem, 8vw, 8rem);
    margin-top: 10vh;
  }

  .kicker {
    margin: 0 0 1.1rem;
    color: var(--worker);
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  h1 {
    max-width: 15ch;
    margin: 0;
    font-family: var(--display);
    font-size: clamp(3.1rem, 7.2vw, 7.4rem);
    font-weight: 540;
    letter-spacing: -0.058em;
    line-height: 0.92;
  }

  h1 em {
    color: var(--copilot);
    font-style: italic;
    font-weight: 480;
  }

  .dek {
    max-width: 47rem;
    margin: 2rem 0 2rem;
    color: var(--muted-dark);
    font-size: clamp(1.05rem, 1.6vw, 1.32rem);
    line-height: 1.58;
  }

  .start {
    display: inline-flex;
    align-items: center;
    gap: 0.8rem;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid var(--ink);
    color: var(--ink);
    font-size: 0.86rem;
    font-weight: 780;
    letter-spacing: 0.08em;
    text-decoration: none;
    text-transform: uppercase;
  }

  .hero-stat {
    position: relative;
    padding: 2rem 0 0 2rem;
    border-left: 1px solid var(--line-strong);
  }

  .hero-stat::before {
    position: absolute;
    top: 0;
    left: -0.3rem;
    width: 0.55rem;
    height: 0.55rem;
    border-radius: 50%;
    background: var(--gold);
    content: '';
  }

  .stat-number {
    display: block;
    color: var(--ink);
    font-family: var(--display);
    font-size: clamp(4.5rem, 9vw, 8rem);
    letter-spacing: -0.07em;
    line-height: 0.8;
  }

  .stat-copy {
    display: block;
    max-width: 20rem;
    margin-top: 1.6rem;
    color: var(--muted-dark);
    font-size: 1rem;
    line-height: 1.5;
  }

  @media (max-width: 780px) {
    .hero { min-height: auto; padding-bottom: 5rem; }
    .hero-grid { grid-template-columns: 1fr; margin-top: 5rem; }
    .hero-stat { max-width: 27rem; }
    h1 { font-size: clamp(3.2rem, 15vw, 5.5rem); }
  }
</style>
