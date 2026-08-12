<script>
  import { onMount } from 'svelte';

  const laneDefinitions = [
    { id: 'human', label: 'Human only', description: 'Does not reach AI' },
    { id: 'execute', label: 'AI executes', description: 'Routed without review' },
    { id: 'together', label: 'Human + AI', description: 'Collaborative or reviewed' }
  ];

  let profiles = [];
  let selectedId = '15-1199.01';
  let aiReach = 65;
  let reviewRate = 40;
  let loading = true;
  let error = '';
  let running = false;
  let complete = false;
  let routedCount = 0;
  let runSeed = 0;
  let frameId = 0;

  onMount(() => {
    const controller = new AbortController();

    async function loadProfiles() {
      try {
        const response = await fetch('/data/occupation-profiles.json', {
          signal: controller.signal
        });
        if (!response.ok) throw new Error(`request failed (${response.status})`);
        const payload = await response.json();
        profiles = payload.occupations;
        if (!profiles.some((profile) => profile.id === selectedId)) selectedId = profiles[0]?.id ?? '';
      } catch (loadError) {
        if (loadError.name !== 'AbortError') error = loadError.message;
      } finally {
        if (!controller.signal.aborted) loading = false;
      }
    }

    loadProfiles();

    return () => {
      controller.abort();
      cancelAnimationFrame(frameId);
    };
  });

  $: sortedProfiles = [...profiles].sort((a, b) => a.name.localeCompare(b.name));
  $: selected = profiles.find((profile) => profile.id === selectedId) ?? null;
  $: assignments = selected
    ? buildAssignments(selected, Number(aiReach), Number(reviewRate), runSeed)
    : [];
  $: lanes = laneDefinitions.map((lane) => ({
    ...lane,
    units: assignments.filter((unit) => unit.lane === lane.id)
  }));
  $: routed = assignments.filter((unit) => unit.order < routedCount);
  $: currentCounts = laneDefinitions.reduce(
    (counts, lane) => ({
      ...counts,
      [lane.id]: routed.filter((unit) => unit.lane === lane.id).length
    }),
    {}
  );
  $: outcome = laneDefinitions.reduce(
    (counts, lane) => ({
      ...counts,
      [lane.id]: assignments.filter((unit) => unit.lane === lane.id).length
    }),
    {}
  );

  function stringSeed(value) {
    let seed = 2166136261;
    for (const character of value) {
      seed ^= character.charCodeAt(0);
      seed = Math.imul(seed, 16777619);
    }
    return seed >>> 0;
  }

  function randomAt(seed, index, salt) {
    let value = (seed + Math.imul(index + 1, 374761393) + Math.imul(salt, 668265263)) >>> 0;
    value = Math.imul(value ^ (value >>> 13), 1274126177);
    value = (value ^ (value >>> 16)) >>> 0;
    return value / 4294967296;
  }

  function buildTaskPool(profile) {
    const tasks = profile.tasks.filter((task) => task.exposure > 0);
    const total = tasks.reduce((sum, task) => sum + task.exposure, 0);
    if (!tasks.length || total <= 0) return [];

    let cumulative = 0;
    const weighted = tasks.map((task) => {
      cumulative += task.exposure / total;
      return { task, cumulative };
    });

    return Array.from({ length: 100 }, (_, index) => {
      const quantile = (index + 0.5) / 100;
      return weighted.find((entry) => quantile <= entry.cumulative)?.task ?? tasks[tasks.length - 1];
    });
  }

  function buildAssignments(profile, reach, review, seedOffset) {
    const taskPool = buildTaskPool(profile);
    const seed = (stringSeed(profile.id) + Math.imul(seedOffset + 1, 2246822519)) >>> 0;
    const units = taskPool.map((task, index) => ({ id: index, task }));
    const reachedTotal = Math.round(Math.max(0, Math.min(100, reach)));
    const reachedIds = new Set(
      [...units]
        .sort((a, b) => randomAt(seed, a.id, 1) - randomAt(seed, b.id, 1))
        .slice(0, reachedTotal)
        .map((unit) => unit.id)
    );
    const revealOrder = new Map(
      [...units]
        .sort((a, b) => randomAt(seed, a.id, 4) - randomAt(seed, b.id, 4))
        .map((unit, index) => [unit.id, index])
    );

    return units.map((unit) => {
      let lane = 'human';
      if (reachedIds.has(unit.id)) {
        const automation = randomAt(seed, unit.id, 2) < unit.task.automation;
        const reviewed = randomAt(seed, unit.id, 3) < review / 100;
        lane = automation && !reviewed ? 'execute' : 'together';
      }

      return { ...unit, lane, order: revealOrder.get(unit.id) };
    });
  }

  function clearRun() {
    cancelAnimationFrame(frameId);
    running = false;
    complete = false;
    routedCount = 0;
  }

  function run() {
    if (running || !selected) return;
    clearRun();
    runSeed += 1;
    running = true;
    const startedAt = performance.now();
    const duration = 1900;

    function animate(now) {
      const progress = Math.min(1, (now - startedAt) / duration);
      const eased = 1 - Math.pow(1 - progress, 3);
      routedCount = Math.min(100, Math.floor(eased * 101));

      if (progress < 1) {
        frameId = requestAnimationFrame(animate);
      } else {
        routedCount = 100;
        running = false;
        complete = true;
      }
    }

    frameId = requestAnimationFrame(animate);
  }

  function resetAll() {
    clearRun();
    selectedId = '15-1199.01';
    aiReach = 65;
    reviewRate = 40;
    runSeed = 0;
  }
</script>

<section class="handoff" id="handoff-simulation" aria-labelledby="handoff-title">
  <header class="section-header">
    <p>Interactive model</p>
    <h2 id="handoff-title">Run the handoff.</h2>
    <span>
      Route 100 normalized units of measured task exposure. Change the assumptions, run the
      workday, and watch where the work lands.
    </span>
  </header>

  {#if loading}
    <div class="loading" role="status">Preparing the workday…</div>
  {:else if error}
    <div class="loading error" role="alert">The simulation could not load: {error}</div>
  {:else if selected}
    <div class="controls">
      <label class="occupation-control">
        <span>Occupation</span>
        <select bind:value={selectedId} on:change={clearRun} disabled={running}>
          {#each sortedProfiles as profile}
            <option value={profile.id}>{profile.name}</option>
          {/each}
        </select>
        <small>
          Dataset profile: {(selected.automation * 100).toFixed(0)}% automation ·
          {(selected.augmentation * 100).toFixed(0)}% augmentation
        </small>
      </label>

      <label>
        <span>AI reach <i>your assumption</i></span>
        <b>{aiReach}%</b>
        <input
          type="range"
          min="0"
          max="100"
          step="5"
          bind:value={aiReach}
          on:input={clearRun}
          disabled={running}
        />
        <small>How much measured task exposure reaches AI at all?</small>
      </label>

      <label>
        <span>Human review <i>your assumption</i></span>
        <b>{reviewRate}%</b>
        <input
          type="range"
          min="0"
          max="100"
          step="5"
          bind:value={reviewRate}
          on:input={clearRun}
          disabled={running}
        />
        <small>How often is AI-executed work redirected to a person for review?</small>
      </label>
    </div>

    <figure>
      <div class="simulation-head">
        <span>Work units routed: <strong>{routedCount} / 100</strong></span>
        <button class="run" type="button" on:click={run} disabled={running}>
          {running ? 'Routing…' : complete ? 'Run again' : 'Run workday'}
        </button>
      </div>

      <div class="lane-board">
        {#each lanes as lane}
          <section class={`lane ${lane.id}`} aria-label={`${lane.label}: ${currentCounts[lane.id] ?? 0} units routed`}>
            <header>
              <div><span>{lane.label}</span><small>{lane.description}</small></div>
              <strong>{currentCounts[lane.id] ?? 0}</strong>
            </header>
            <div class="unit-grid" aria-hidden="true">
              {#each lane.units as unit}
                <i
                  class:routed={unit.order < routedCount}
                  style={`--delay:${(unit.order % 10) * 12}ms`}
                  title={unit.task.name}
                ></i>
              {/each}
            </div>
          </section>
        {/each}
      </div>

      <div class="simulation-footer">
        <p aria-live="polite">
          {#if complete}
            In this run, <strong>{outcome.execute}</strong> units went to AI execution,
            <strong>{outcome.together}</strong> became human–AI work, and
            <strong>{outcome.human}</strong> remained human-only.
          {:else}
            Press <strong>Run workday</strong> to sample an illustrative handoff.
          {/if}
        </p>
        <button class="reset" type="button" on:click={resetAll} disabled={running}>Reset</button>
      </div>
    </figure>

    <details>
      <summary>What exactly is this simulating?</summary>
      <p>
        Each mark is one normalized unit of task exposure. Task names are repeated in proportion to
        their measured exposure among the occupation’s displayed tasks. AI reach determines which
        units encounter AI. Task-level role shares then sample execution versus collaboration, and
        the review setting redirects some execution into human–AI work.
      </p>
      <p>
        This is an explanatory model, not a forecast. It does not estimate productivity, time saved,
        job loss, quality, or whether an organization should adopt AI.
      </p>
    </details>
  {/if}
</section>

<style>
  .handoff { width: min(100% - 2rem, 88rem); margin: 5rem auto 10rem; }
  .section-header { max-width: 54rem; margin: 0 auto 2.5rem; text-align: center; }
  .section-header p { margin: 0 0 0.55rem; color: var(--magenta); font-size: 0.7rem; font-weight: 900; letter-spacing: 0.11em; text-transform: uppercase; }
  .section-header h2 { margin: 0; color: var(--purple); font-size: clamp(3rem, 7vw, 6.5rem); font-weight: 950; letter-spacing: -0.065em; line-height: 0.82; text-transform: uppercase; }
  .section-header > span { display: block; max-width: 43rem; margin: 1.2rem auto 0; color: var(--ink-soft); font-size: 1rem; line-height: 1.5; }

  .controls { display: grid; grid-template-columns: 1.25fr 1fr 1fr; gap: 1.25rem; margin-bottom: 1.2rem; }
  label { display: grid; grid-template-columns: 1fr auto; align-content: start; gap: 0.4rem 0.75rem; color: var(--ink-soft); font-size: 0.8rem; }
  label > span { color: var(--ink); font-weight: 850; }
  label > span i { display: inline-block; margin-left: 0.25rem; color: var(--magenta); font-size: 0.58rem; font-style: normal; font-weight: 900; letter-spacing: 0.06em; text-transform: uppercase; }
  label > b { color: var(--purple); font-size: 1rem; }
  label input { grid-column: 1 / -1; width: 100%; accent-color: var(--purple); }
  label small { grid-column: 1 / -1; min-height: 2.4em; line-height: 1.25; }
  .occupation-control { grid-template-columns: 1fr; }
  select { width: 100%; min-width: 0; padding: 0.65rem 2.2rem 0.65rem 0.75rem; border: 2px solid var(--purple-mid); border-radius: 0; background: var(--cream-light); color: var(--ink); font: 700 0.82rem/1.2 var(--sans); }
  select:focus-visible, button:focus-visible, input:focus-visible { outline: 3px solid var(--pink-light); outline-offset: 3px; }

  figure { position: relative; margin: 0; padding: clamp(0.8rem, 2vw, 1.4rem); border: 1.5px solid #9f88aa; background: rgba(255,255,255,0.82); }
  .simulation-head { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.2rem 0.2rem 1.1rem; font-size: clamp(1rem, 2vw, 1.3rem); }
  .simulation-head strong { color: var(--purple); font-weight: 950; }
  button { border: 2px solid var(--purple-mid); border-radius: 0; background: #faedf8; color: var(--purple); font-weight: 900; text-transform: uppercase; cursor: pointer; }
  button:disabled { color: #847b86; cursor: not-allowed; opacity: 0.68; }
  .run { min-width: 13rem; padding: 0.72rem 1.4rem; box-shadow: 4px 4px 0 var(--purple-mid); }

  .lane-board { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.8rem; min-height: 24rem; padding: 1rem; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); background: rgba(238,232,240,0.6); }
  .lane { display: grid; grid-template-rows: auto 1fr; min-width: 0; border: 1.5px solid var(--ink); background: rgba(247,242,248,0.72); }
  .lane header { display: flex; align-items: start; justify-content: space-between; gap: 0.5rem; min-height: 4.5rem; padding: 0.65rem 0.75rem; border-bottom: 1.5px solid var(--ink); }
  .lane header div { display: grid; }
  .lane header span { font-size: clamp(0.68rem, 1.2vw, 0.85rem); font-weight: 950; letter-spacing: 0.05em; text-transform: uppercase; }
  .lane header small { margin-top: 0.2rem; color: var(--ink-soft); font-size: 0.58rem; line-height: 1.15; }
  .lane header strong { color: var(--purple); font-size: clamp(1.4rem, 3vw, 2.2rem); line-height: 0.85; }
  .execute header strong { color: var(--automation-dark); }
  .together header strong { color: var(--augmentation-dark); }

  .unit-grid { display: grid; grid-template-columns: repeat(10, minmax(0, 1fr)); align-content: end; gap: 0.22rem; min-height: 17rem; padding: 0.75rem; }
  .unit-grid i { height: 0.7rem; border: 1px solid var(--ink); background: var(--purple-mid); opacity: 0.05; transform: translateY(-0.75rem) scaleY(0.2); transform-origin: center bottom; transition: opacity 180ms ease var(--delay), transform 360ms cubic-bezier(0.2,0.75,0.2,1) var(--delay); }
  .execute .unit-grid i { background: var(--automation); }
  .together .unit-grid i { background: var(--augmentation); }
  .unit-grid i.routed { opacity: 1; transform: translateY(0) scaleY(1); }

  .simulation-footer { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 1rem 0.2rem 0.2rem; }
  .simulation-footer p { margin: 0; color: var(--ink-soft); font-size: 0.8rem; line-height: 1.4; }
  .simulation-footer p strong { color: var(--purple); }
  .reset { flex: 0 0 auto; padding: 0.45rem 0.7rem; background: transparent; box-shadow: none; }
  details { max-width: 55rem; margin: 1rem auto 0; color: var(--ink-soft); font-size: 0.78rem; line-height: 1.5; }
  summary { color: var(--purple); font-weight: 850; cursor: pointer; }
  details p { margin: 0.8rem 0 0; }
  .loading { display: grid; min-height: 26rem; place-items: center; border: 1.5px solid var(--line); background: rgba(255,255,255,0.55); color: var(--ink-soft); }
  .error { color: var(--automation-dark); }

  @media (max-width: 900px) {
    .controls { grid-template-columns: 1fr 1fr; }
    .occupation-control { grid-column: 1 / -1; }
    .lane-board { min-height: 20rem; padding: 0.65rem; }
    .unit-grid { grid-template-columns: repeat(6, minmax(0, 1fr)); min-height: 14rem; padding: 0.5rem; }
  }

  @media (max-width: 620px) {
    .controls { grid-template-columns: 1fr; }
    .occupation-control { grid-column: auto; }
    .lane-board { grid-template-columns: 1fr; }
    .lane { grid-template-columns: minmax(8rem, 0.65fr) 1.35fr; grid-template-rows: none; }
    .lane header { min-height: 7rem; border-right: 1.5px solid var(--ink); border-bottom: 0; }
    .unit-grid { grid-template-columns: repeat(10, minmax(0, 1fr)); min-height: 7rem; }
    .simulation-head { align-items: flex-start; }
    .run { min-width: 0; padding: 0.6rem 0.7rem; font-size: 0.66rem; }
    .simulation-footer { align-items: flex-start; }
  }

  @media (prefers-reduced-motion: reduce) {
    .unit-grid i { transition-duration: 0.01ms; transition-delay: 0ms; }
  }
</style>
