<script>
  import { onMount } from 'svelte';

  let profiles = [];
  let selectedId = '15-1199.01';
  let search = '';
  let loading = true;
  let error = '';
  let root;

  onMount(() => {
    const controller = new AbortController();
    let observer;

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

    if ('IntersectionObserver' in window) {
      observer = new IntersectionObserver(
        ([entry]) => {
          if (!entry?.isIntersecting) return;
          observer.disconnect();
          loadProfiles();
        },
        { rootMargin: '1000px 0px' }
      );
      if (root) observer.observe(root);
    } else {
      loadProfiles();
    }

    return () => {
      observer?.disconnect();
      controller.abort();
    };
  });

  $: selected = profiles.find((profile) => profile.id === selectedId) ?? null;
  $: suggestions = (search.trim()
    ? profiles.filter((profile) => profile.name.toLowerCase().includes(search.trim().toLowerCase()))
    : profiles
  ).slice(0, 8);

  function choose(profile) {
    selectedId = profile.id;
    search = '';
  }

  function handleSearch(event) {
    search = event.currentTarget.value;
    const exact = profiles.find(
      (profile) => profile.name.toLowerCase() === search.trim().toLowerCase()
    );
    if (exact) choose(exact);
  }

  const percent = (value, digits = 1) => `${(Number(value) * 100).toFixed(digits)}%`;
</script>

<section bind:this={root} class="explorer-section" id="explore" aria-labelledby="explorer-title">
  <div class="section-intro">
    <p class="eyebrow">Now try your own occupation</p>
    <h2 id="explorer-title">A job title is only the beginning.</h2>
    <p>
      Pick an occupation to see its estimated exposure, its automation–augmentation balance,
      and the individual tasks driving that profile.
    </p>
  </div>

  {#if loading}
    <div class="status" role="status">Loading occupation profiles…</div>
  {:else if error}
    <div class="status error" role="alert">The explorer could not load: {error}</div>
  {:else}
    <div class="explorer-shell">
      <div class="search-panel">
        <label for="occupation-search">Search {profiles.length} occupations</label>
        <input
          id="occupation-search"
          type="search"
          placeholder="Try: teachers, nurses, designers…"
          value={search}
          on:input={handleSearch}
          autocomplete="off"
          aria-controls="occupation-suggestions"
        />

        <div class="suggestions" id="occupation-suggestions" aria-label="Occupation suggestions">
          {#each suggestions as profile}
            <button
              type="button"
              class:active={profile.id === selectedId}
              on:click={() => choose(profile)}
            >{profile.name}</button>
          {/each}
        </div>
      </div>

      {#if selected}
        <article class="profile-card" aria-live="polite">
          <header class="profile-header">
            <div>
              <p class="profile-kicker">Selected occupation</p>
              <h3>{selected.name}</h3>
              <p class="family-name">{selected.family} · Job Zone {selected.jobZone ?? 'not available'}</p>
            </div>
            <div class="exposure-badge" aria-label={`${selected.exposure.toFixed(2)} percent exposure`}>
              <strong>{selected.exposure.toFixed(2)}%</strong>
              <span>exposure</span>
            </div>
          </header>

          <div class="split-summary">
            <div class="split-copy">
              <div><strong>{percent(selected.automation)}</strong><span>automation</span></div>
              <div><strong>{percent(selected.augmentation)}</strong><span>augmentation</span></div>
            </div>
            <div
              class="profile-bar"
              aria-label={`${percent(selected.automation)} automation and ${percent(selected.augmentation)} augmentation`}
            >
              <span class="automation" style={`width:${selected.automation * 100}%`}></span>
              <span class="augmentation" style={`width:${selected.augmentation * 100}%`}></span>
            </div>
            <p class="coverage-note">
              Based on {selected.validTaskCount} classified tasks, representing
              {percent(selected.coverage)} of this occupation’s measured exposure.
            </p>
          </div>

          <div class="tasks-block">
            <h4>Highest-exposure tasks</h4>
            <ol>
              {#each selected.tasks.slice(0, 8) as task}
                <li>
                  <div class="task-copy">
                    <p>{task.name}</p>
                    <span class:automation-label={task.automation >= task.augmentation}>
                      {task.automation >= task.augmentation ? 'automation' : 'augmentation'}
                    </span>
                  </div>
                  <div class="task-meter" aria-hidden="true">
                    <span
                      class:automation-task={task.automation >= task.augmentation}
                      style={`width:${Math.max(4, (task.exposure / selected.tasks[0].exposure) * 100)}%`}
                    ></span>
                  </div>
                  <small>{task.exposure.toFixed(3)} percentage points of total exposure</small>
                </li>
              {/each}
            </ol>
          </div>
        </article>
      {/if}
    </div>
  {/if}
</section>

<style>
  .explorer-section { padding: clamp(5rem, 10vw, 9rem) max(1.25rem, calc((100vw - 1180px) / 2)); background: var(--ink); color: var(--cream-light); }
  .section-intro { max-width: 48rem; margin-bottom: 3rem; }
  .section-intro h2 { margin: 0.2rem 0 1rem; font-family: var(--display); font-size: clamp(2.7rem, 6vw, 5.8rem); font-weight: 950; line-height: 0.88; letter-spacing: -0.06em; text-transform: uppercase; }
  .section-intro > p:last-child { max-width: 40rem; color: #d8cedb; font-size: clamp(1.05rem, 1.5vw, 1.3rem); }
  .eyebrow, .profile-kicker { margin: 0; color: var(--pink-light); font-size: 0.72rem; font-weight: 900; letter-spacing: 0.12em; text-transform: uppercase; }
  .explorer-shell { display: grid; grid-template-columns: minmax(15rem, 0.8fr) minmax(0, 2fr); gap: clamp(1.5rem, 4vw, 4rem); align-items: start; }
  .search-panel { position: sticky; top: 5.5rem; }
  .search-panel label { display: block; margin-bottom: 0.55rem; font-size: 0.82rem; font-weight: 800; }
  input { width: 100%; box-sizing: border-box; padding: 0.9rem 1rem; border: 2px solid var(--purple-mid); border-radius: 0; background: var(--cream-light); color: var(--ink); font: 650 1rem/1.2 var(--sans); }
  input:focus-visible { outline: 3px solid var(--gold); outline-offset: 3px; }
  .suggestions { display: grid; margin-top: 0.65rem; border-top: 1px solid var(--purple-mid); }
  .suggestions button { padding: 0.72rem 0.15rem; border: 0; border-bottom: 1px solid #5d4e63; background: transparent; color: #e8dfea; font: 650 0.83rem/1.25 var(--sans); text-align: left; cursor: pointer; transition: color 160ms ease, padding-left 160ms ease; }
  .suggestions button:hover, .suggestions button:focus-visible, .suggestions button.active { padding-left: 0.55rem; color: var(--pink-light); }
  .profile-card { overflow: hidden; border: 2px solid var(--cream-light); background: var(--paper); color: var(--ink); box-shadow: none; }
  .profile-header { display: flex; justify-content: space-between; gap: 1rem; align-items: flex-start; padding: clamp(1.35rem, 3vw, 2.4rem); border-bottom: 2px solid var(--ink); }
  .profile-header h3 { max-width: 42rem; margin: 0.35rem 0 0.25rem; font-family: var(--display); font-size: clamp(2rem, 4.5vw, 4.2rem); font-weight: 950; line-height: 0.9; letter-spacing: -0.055em; }
  .family-name { margin: 0; color: var(--ink-soft); font-size: 0.86rem; font-weight: 700; }
  .exposure-badge { display: grid; flex: 0 0 auto; width: 7.25rem; aspect-ratio: 1; place-content: center; border: 2px solid var(--ink); border-radius: 50%; background: var(--gold); text-align: center; transform: rotate(4deg); }
  .exposure-badge strong { font-size: 1.45rem; line-height: 1; }
  .exposure-badge span { margin-top: 0.2rem; font-size: 0.6rem; font-weight: 900; letter-spacing: 0.08em; text-transform: uppercase; }
  .split-summary { padding: clamp(1.35rem, 3vw, 2.4rem); background: var(--cream-light); border-bottom: 2px solid var(--ink); }
  .split-copy { display: flex; justify-content: space-between; gap: 1rem; }
  .split-copy div { display: grid; }
  .split-copy div:last-child { text-align: right; }
  .split-copy strong { font-size: clamp(1.5rem, 3vw, 2.4rem); line-height: 1; }
  .split-copy div:first-child strong, .automation-label { color: var(--automation-dark) !important; }
  .split-copy div:last-child strong { color: var(--augmentation-dark); }
  .split-copy span { font-size: 0.67rem; font-weight: 900; letter-spacing: 0.08em; text-transform: uppercase; }
  .profile-bar { display: flex; height: 1.1rem; margin: 0.85rem 0; border: 2px solid var(--ink); background: white; }
  .profile-bar span { transition: width 700ms cubic-bezier(0.22, 1, 0.36, 1); }
  .automation { background: var(--automation); }
  .augmentation { background: var(--augmentation); }
  .coverage-note { margin: 0; color: var(--ink-soft); font-size: 0.75rem; font-weight: 650; }
  .tasks-block { padding: clamp(1.35rem, 3vw, 2.4rem); }
  .tasks-block h4 { margin: 0 0 1.2rem; font-size: 0.8rem; font-weight: 900; letter-spacing: 0.1em; text-transform: uppercase; }
  ol { display: grid; gap: 1.1rem; margin: 0; padding: 0; list-style: none; counter-reset: task; }
  li { counter-increment: task; }
  .task-copy { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 1rem; align-items: start; }
  .task-copy p { position: relative; margin: 0; padding-left: 2rem; font-size: 0.92rem; font-weight: 650; line-height: 1.35; }
  .task-copy p::before { content: counter(task, decimal-leading-zero); position: absolute; left: 0; top: 0.05rem; color: #7d7b74; font-size: 0.64rem; }
  .task-copy span { padding: 0.22rem 0.4rem; border: 1px solid currentColor; color: var(--augmentation-dark); font-size: 0.55rem; font-weight: 900; letter-spacing: 0.07em; text-transform: uppercase; }
  .task-meter { height: 0.34rem; margin: 0.55rem 0 0.3rem 2rem; background: #d7cadb; }
  .task-meter span { display: block; height: 100%; background: var(--augmentation); transition: width 650ms cubic-bezier(0.22, 1, 0.36, 1); }
  .task-meter span.automation-task { background: var(--automation); }
  small { display: block; margin-left: 2rem; color: #6f6b61; font-size: 0.65rem; font-weight: 650; }
  .status { min-height: 20rem; display: grid; place-items: center; border: 1px solid #697481; }
  .error { color: #ffc0ae; }

  @media (max-width: 920px) {
    .explorer-shell { grid-template-columns: 1fr; }
    .search-panel { position: static; }
  }

  @media (max-width: 760px) {
    .suggestions { grid-template-columns: 1fr 1fr; gap: 0 0.8rem; }
    .profile-header { display: grid; }
    .exposure-badge { width: 6rem; }
    .task-copy { grid-template-columns: 1fr; gap: 0.35rem; }
    .task-copy span { width: max-content; margin-left: 2rem; }
  }

  @media (prefers-reduced-motion: reduce) {
    .profile-bar span, .task-meter span, .suggestions button { transition: none; }
  }
</style>
