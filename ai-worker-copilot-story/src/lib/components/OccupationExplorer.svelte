<script lang="ts">
  type Task = { name: string; balance: number; classifiedExposure: number } | null;
  type Occupation = {
    name: string;
    family: string;
    zone: number;
    salary: number | null;
    salaryQuartile: string;
    exposure: number;
    roleBalance: number | null;
    workerShare: number | null;
    copilotShare: number | null;
    coverage: number | null;
    workerTask: Task;
    copilotTask: Task;
  };

  export let occupations: Occupation[] = [];
  let selectedName = 'Software Developers, Systems Software';

  $: selected = occupations.find((occupation) => occupation.name === selectedName) ?? occupations[0];
  $: marker = selected?.roleBalance == null ? 50 : (selected.roleBalance + 1) * 50;

  const quickPicks = [
    'Software Developers, Systems Software',
    'Tutors',
    'Pharmacists',
    'Interpreters and Translators'
  ];

  function salaryLabel(value: number | null) {
    if (value == null) return 'Not available';
    if (value < 1000) return `$${value.toFixed(2)} / hour`;
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value);
  }

  function roleLabel(balance: number | null) {
    if (balance == null) return 'Not classified';
    if (balance < -0.1) return 'Worker-oriented';
    if (balance > 0.1) return 'Copilot-oriented';
    return 'Nearly balanced';
  }
</script>

<section class="explorer section-shell" id="explore" aria-labelledby="explorer-title">
  <div class="explorer-head">
    <div>
      <p class="section-index">Now make it personal</p>
      <h2 id="explorer-title">What role does AI play in your occupation?</h2>
    </div>
    <p>Search the occupation list, then compare its overall orientation with the individual tasks that sit underneath it.</p>
  </div>

  <div class="search-panel">
    <label for="occupation-search">Search an occupation</label>
    <div class="input-wrap">
      <input id="occupation-search" list="occupation-list" bind:value={selectedName} autocomplete="off" />
      <span aria-hidden="true">⌕</span>
    </div>
    <datalist id="occupation-list">
      {#each occupations as occupation}<option value={occupation.name}></option>{/each}
    </datalist>
    <div class="quick-picks" aria-label="Example occupations">
      <span>Try:</span>
      {#each quickPicks as pick}
        <button class:current={selectedName === pick} on:click={() => selectedName = pick}>{pick}</button>
      {/each}
    </div>
  </div>

  {#if selected}
    <div class="occupation-card">
      <div class="occupation-title">
        <p>{selected.family}</p>
        <h3>{selected.name}</h3>
        <span class="role-badge" class:worker={selected.roleBalance != null && selected.roleBalance < -0.1}>
          {roleLabel(selected.roleBalance)}
        </span>
      </div>

      <dl class="stats">
        <div><dt>Job Zone</dt><dd>{selected.zone} / 5</dd></div>
        <div><dt>Median pay</dt><dd>{salaryLabel(selected.salary)}</dd></div>
        <div><dt>Observed exposure</dt><dd>{selected.exposure.toFixed(2)}%</dd></div>
        <div><dt>Classified coverage</dt><dd>{selected.coverage == null ? '—' : `${Math.round(selected.coverage * 100)}%`}</dd></div>
      </dl>

      <div class="spectrum-block">
        <div class="spectrum-labels"><span>AI as worker</span><span>AI as copilot</span></div>
        <div class="spectrum" aria-label={`Role balance: ${roleLabel(selected.roleBalance)}`}>
          <span class="midpoint"></span>
          {#if selected.roleBalance != null}
            <span class="marker" style={`left: ${marker}%`}></span>
          {/if}
        </div>
        <div class="spectrum-values">
          <span>{selected.workerShare == null ? '—' : `${Math.round(selected.workerShare * 100)}% worker`}</span>
          <span>{selected.copilotShare == null ? '—' : `${Math.round(selected.copilotShare * 100)}% copilot`}</span>
        </div>
      </div>

      <div class="task-grid">
        <article class="task worker-task">
          <p class="task-label">A more worker-like task</p>
          {#if selected.workerTask}<h4>{selected.workerTask.name}</h4>{:else}<h4>No strongly worker-oriented task passed the classification rules.</h4>{/if}
        </article>
        <article class="task copilot-task">
          <p class="task-label">A more copilot-like task</p>
          {#if selected.copilotTask}<h4>{selected.copilotTask.name}</h4>{:else}<h4>No strongly copilot-oriented task passed the classification rules.</h4>{/if}
        </article>
      </div>
    </div>
  {/if}
</section>

<style>
  .explorer { padding-top: 8rem; padding-bottom: 8rem; }
  .explorer-head { display: grid; grid-template-columns: 1.15fr 0.6fr; gap: 4rem; align-items: end; }
  .section-index { color: var(--worker); font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }
  h2 { max-width: 13ch; margin: 0.7rem 0 0; font-family: var(--display); font-size: clamp(3rem, 6.2vw, 6.3rem); font-weight: 520; letter-spacing: -0.058em; line-height: 0.94; }
  .explorer-head > p { max-width: 27rem; margin: 0; color: var(--muted-dark); line-height: 1.65; }
  .search-panel { margin-top: 4rem; padding: 1.5rem; border: 1px solid var(--line-strong); background: rgba(255,255,255,0.28); }
  label { display: block; margin-bottom: 0.6rem; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; }
  .input-wrap { display: flex; align-items: center; border-bottom: 2px solid var(--ink); }
  input { width: 100%; padding: 0.55rem 0 0.8rem; border: 0; outline: 0; background: transparent; color: var(--ink); font-family: var(--display); font-size: clamp(1.4rem, 3vw, 2.4rem); }
  .input-wrap span { color: var(--muted); font-size: 2rem; }
  .quick-picks { display: flex; flex-wrap: wrap; align-items: center; gap: 0.55rem; margin-top: 1rem; color: var(--muted); font-size: 0.75rem; }
  button { padding: 0.4rem 0.7rem; border: 1px solid var(--line-strong); border-radius: 999px; background: transparent; color: var(--muted-dark); cursor: pointer; font: inherit; }
  button:hover, button:focus-visible, button.current { border-color: var(--ink); background: var(--ink); color: var(--paper); }
  .occupation-card { margin-top: 1.5rem; border: 1px solid var(--line-strong); background: var(--paper-light); }
  .occupation-title { padding: clamp(1.5rem, 4vw, 3rem); border-bottom: 1px solid var(--line-strong); }
  .occupation-title p { margin: 0 0 0.6rem; color: var(--muted); font-size: 0.72rem; font-weight: 800; letter-spacing: 0.09em; text-transform: uppercase; }
  h3 { max-width: 24ch; margin: 0; font-family: var(--display); font-size: clamp(2.3rem, 5vw, 5rem); font-weight: 520; letter-spacing: -0.05em; line-height: 0.98; }
  .role-badge { display: inline-block; margin-top: 1.5rem; padding: 0.45rem 0.75rem; border-radius: 999px; background: color-mix(in srgb, var(--copilot) 14%, transparent); color: var(--copilot); font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }
  .role-badge.worker { background: color-mix(in srgb, var(--worker) 14%, transparent); color: var(--worker-dark); }
  .stats { display: grid; grid-template-columns: repeat(4, 1fr); margin: 0; border-bottom: 1px solid var(--line-strong); }
  .stats div { padding: 1.5rem; border-right: 1px solid var(--line-strong); }
  .stats div:last-child { border: 0; }
  dt { color: var(--muted); font-size: 0.68rem; font-weight: 800; letter-spacing: 0.09em; text-transform: uppercase; }
  dd { margin: 0.55rem 0 0; font-family: var(--display); font-size: clamp(1.2rem, 2vw, 1.8rem); }
  .spectrum-block { padding: clamp(1.5rem, 4vw, 3rem); border-bottom: 1px solid var(--line-strong); }
  .spectrum-labels, .spectrum-values { display: flex; justify-content: space-between; gap: 1rem; font-size: 0.73rem; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase; }
  .spectrum-labels span:first-child { color: var(--worker-dark); }
  .spectrum-labels span:last-child { color: var(--copilot); }
  .spectrum { position: relative; height: 1rem; margin: 1.1rem 0; border-radius: 999px; background: linear-gradient(90deg, var(--worker), #d8d1c6 50%, var(--copilot)); }
  .midpoint { position: absolute; left: 50%; top: -0.35rem; width: 1px; height: 1.7rem; background: var(--ink); opacity: 0.45; }
  .marker { position: absolute; top: 50%; width: 1.45rem; height: 1.45rem; border: 4px solid var(--paper-light); border-radius: 50%; background: var(--ink); box-shadow: 0 1px 6px rgba(0,0,0,0.24); transform: translate(-50%, -50%); transition: left 450ms cubic-bezier(.2,.8,.2,1); }
  .spectrum-values { color: var(--muted); font-weight: 650; letter-spacing: 0; text-transform: none; }
  .task-grid { display: grid; grid-template-columns: 1fr 1fr; }
  .task { min-height: 16rem; padding: clamp(1.5rem, 4vw, 3rem); }
  .task + .task { border-left: 1px solid var(--line-strong); }
  .worker-task { background: color-mix(in srgb, var(--worker) 8%, transparent); }
  .copilot-task { background: color-mix(in srgb, var(--copilot) 8%, transparent); }
  .task-label { margin: 0 0 1.2rem; font-size: 0.7rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; }
  .worker-task .task-label { color: var(--worker-dark); }
  .copilot-task .task-label { color: var(--copilot); }
  h4 { margin: 0; font-family: var(--display); font-size: clamp(1.5rem, 2.8vw, 2.5rem); font-weight: 520; letter-spacing: -0.035em; line-height: 1.12; }
  @media (max-width: 760px) {
    .explorer-head { grid-template-columns: 1fr; gap: 1.5rem; }
    .stats { grid-template-columns: 1fr 1fr; }
    .stats div:nth-child(2) { border-right: 0; }
    .stats div:nth-child(-n+2) { border-bottom: 1px solid var(--line-strong); }
    .task-grid { grid-template-columns: 1fr; }
    .task + .task { border-left: 0; border-top: 1px solid var(--line-strong); }
  }
</style>
