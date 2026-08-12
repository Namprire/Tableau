<script>
  import AnimatedNumber from './AnimatedNumber.svelte';

  const plot = { left: 55, right: 14, top: 28, bottom: 42, width: 560, height: 360 };

  let poorer = 100;
  let richer = 1000;
  let poorWins = 0;
  let richWins = 0;
  let rounds = 0;
  let lastPoorWon = null;
  let poorHistory = [100];
  let richHistory = [1000];
  let announcement = 'Ready to flip.';

  $: wager = Math.max(1, Math.round(Math.min(poorer, richer) * 0.2));
  $: poorDomain = domainFor(poorHistory, 100, 20);
  $: richDomain = domainFor(richHistory, 1000, 120);
  $: poorTicks = ticksFor(poorDomain);
  $: richTicks = ticksFor(richDomain);
  $: turnMaximum = Math.max(10, rounds);
  $: poorPath = pathFor(poorHistory, poorDomain);
  $: richPath = pathFor(richHistory, richDomain);

  function domainFor(values, baseline, padding) {
    const low = Math.min(baseline, ...values);
    const high = Math.max(baseline, ...values);
    return [Math.floor((low - padding) / 10) * 10, Math.ceil((high + padding) / 10) * 10];
  }

  function ticksFor([minimum, maximum]) {
    return [minimum, Math.round((minimum + maximum) / 20) * 10, maximum];
  }

  function xFor(index) {
    const innerWidth = plot.width - plot.left - plot.right;
    return plot.left + (index / turnMaximum) * innerWidth;
  }

  function yFor(value, [minimum, maximum]) {
    const innerHeight = plot.height - plot.top - plot.bottom;
    return plot.top + ((maximum - value) / Math.max(1, maximum - minimum)) * innerHeight;
  }

  function pathFor(values, domain) {
    return values.map((value, index) => `${index ? 'L' : 'M'} ${xFor(index)} ${yFor(value, domain)}`).join(' ');
  }

  function flip() {
    if (poorer <= 0 || richer <= 0) return;
    const amount = wager;
    const poorWon = Math.random() >= 0.5;
    rounds += 1;
    lastPoorWon = poorWon;

    if (poorWon) {
      poorer += amount;
      richer -= amount;
      poorWins += 1;
      announcement = `You won $${amount}.`;
    } else {
      poorer -= amount;
      richer += amount;
      richWins += 1;
      announcement = `The richer player won $${amount}.`;
    }

    poorHistory = [...poorHistory, poorer];
    richHistory = [...richHistory, richer];
  }

  function reset() {
    poorer = 100;
    richer = 1000;
    poorWins = 0;
    richWins = 0;
    rounds = 0;
    lastPoorWon = null;
    poorHistory = [100];
    richHistory = [1000];
    announcement = 'Ready to flip.';
  }
</script>

<section class="coin-game" aria-labelledby="coin-game-title">
  <header>
    <h3 id="coin-game-title">Flip a coin to see who wins <strong>${wager}</strong></h3>
    <button on:click={flip} disabled={poorer <= 0 || richer <= 0}>Flip coin</button>
    <p class="announcement" aria-live="polite">{announcement}</p>
  </header>

  <div class="charts">
    <figure>
      <figcaption>
        <span class="portrait poor-portrait">
          <img src={lastPoorWon === false ? '/assets/player1-sad.png' : '/assets/player1-happy.png'} alt="" />
        </span>
        <span class="identity">
          <strong>You (poorer player)</strong>
          <b>$<AnimatedNumber value={poorer} /></b>
          <small>{poorWins}-{richWins} ({rounds ? Math.round((poorWins / rounds) * 100) : 0}%)</small>
        </span>
        {#if lastPoorWon !== null}
          <em class:win={lastPoorWon} class:lose={!lastPoorWon}>{lastPoorWon ? 'Win' : 'Lose'}</em>
        {/if}
      </figcaption>

      <svg viewBox="0 0 560 360" role="img" aria-label={`Your balance is $${poorer} after ${rounds} rounds.`}>
        {#each poorTicks as tick}
          <line class="grid horizontal" x1={plot.left} x2={plot.width - plot.right} y1={yFor(tick, poorDomain)} y2={yFor(tick, poorDomain)}></line>
          <text class="axis-label" x="8" y={yFor(tick, poorDomain) - 5}>${tick}</text>
        {/each}
        {#each Array(11) as _, index}
          <line class="grid vertical" x1={plot.left + (index / 10) * (plot.width - plot.left - plot.right)} x2={plot.left + (index / 10) * (plot.width - plot.left - plot.right)} y1={plot.top} y2={plot.height - plot.bottom}></line>
          <text class="turn-label" x={plot.left + (index / 10) * (plot.width - plot.left - plot.right)} y={plot.height - 12} text-anchor="middle">{Math.round((index / 10) * turnMaximum)}</text>
        {/each}
        <line class="baseline" x1={plot.left} x2={plot.width - plot.right} y1={yFor(100, poorDomain)} y2={yFor(100, poorDomain)}></line>
        <text class="baseline-label" x="8" y={yFor(100, poorDomain) - 5}>$100</text>
        <path d={poorPath}></path>
      </svg>
    </figure>

    <figure>
      <figcaption>
        <span class="portrait rich-portrait">
          <img src={lastPoorWon === true ? '/assets/player4-sad.png' : '/assets/player4-happy.png'} alt="" />
        </span>
        <span class="identity">
          <strong>Richer player</strong>
          <b>$<AnimatedNumber value={richer} /></b>
          <small>{richWins}-{poorWins} ({rounds ? Math.round((richWins / rounds) * 100) : 0}%)</small>
        </span>
        {#if lastPoorWon !== null}
          <em class:win={!lastPoorWon} class:lose={lastPoorWon}>{lastPoorWon ? 'Lose' : 'Win'}</em>
        {/if}
      </figcaption>

      <svg viewBox="0 0 560 360" role="img" aria-label={`The richer player's balance is $${richer} after ${rounds} rounds.`}>
        {#each richTicks as tick}
          <line class="grid horizontal" x1={plot.left} x2={plot.width - plot.right} y1={yFor(tick, richDomain)} y2={yFor(tick, richDomain)}></line>
          <text class="axis-label" x="8" y={yFor(tick, richDomain) - 5}>${tick}</text>
        {/each}
        {#each Array(11) as _, index}
          <line class="grid vertical" x1={plot.left + (index / 10) * (plot.width - plot.left - plot.right)} x2={plot.left + (index / 10) * (plot.width - plot.left - plot.right)} y1={plot.top} y2={plot.height - plot.bottom}></line>
          <text class="turn-label" x={plot.left + (index / 10) * (plot.width - plot.left - plot.right)} y={plot.height - 12} text-anchor="middle">{Math.round((index / 10) * turnMaximum)}</text>
        {/each}
        <line class="baseline" x1={plot.left} x2={plot.width - plot.right} y1={yFor(1000, richDomain)} y2={yFor(1000, richDomain)}></line>
        <text class="baseline-label" x="8" y={yFor(1000, richDomain) - 5}>$1000</text>
        <path d={richPath}></path>
      </svg>
    </figure>
  </div>

  <button class="reset" on:click={reset} disabled={rounds === 0}>Reset</button>
</section>

<style>
  .coin-game { width: min(100% - 2rem, 96rem); margin: 4rem auto 7rem; color: #42104c; }
  header { display: grid; justify-items: center; min-height: 8.5rem; text-align: center; }
  h3 { margin: 0 0 1rem; font-size: clamp(1.25rem, 3vw, 2rem); font-weight: 500; }
  h3 strong { font-weight: 900; }
  button { min-width: 13rem; padding: 0.6rem 1.05rem; border: 2px solid #51105c; background: #f7eafb; color: #42104c; font-weight: 850; cursor: pointer; box-shadow: 3px 3px 0 #51105c; text-transform: none; }
  button:hover:not(:disabled) { transform: translate(-1px, -1px); box-shadow: 5px 5px 0 #51105c; }
  button:disabled { opacity: 0.42; cursor: not-allowed; }
  .announcement { min-height: 1.2rem; margin: 0.55rem 0 0; color: #78677e; font-size: 0.72rem; }
  .charts { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  figure { margin: 0; border: 1px solid #a996ae; background: rgba(255,255,255,0.78); }
  figcaption { position: relative; display: flex; align-items: center; gap: 0.8rem; min-height: 7rem; padding: 1rem; }
  .portrait { width: 5rem; height: 5rem; flex: 0 0 auto; overflow: hidden; border: 1px solid #7f6b85; background: #f4d24f; }
  .rich-portrait { background: #ded6e0; }
  .portrait img { width: 100%; height: 100%; object-fit: contain; object-position: center bottom; }
  .identity { display: grid; color: #4b0758; font-size: clamp(0.8rem, 1.5vw, 1.08rem); line-height: 1.2; text-align: left; }
  .identity strong { font-weight: 900; }
  .identity b { font-weight: 500; }
  .identity small { font-size: 0.9em; }
  figcaption em { position: absolute; top: 1rem; right: 1rem; padding: 0.28rem 0.7rem; background: #dedede; color: #111; font-style: normal; font-weight: 900; text-transform: uppercase; }
  figcaption em.win { background: #f3cf48; }
  svg { display: block; width: 100%; height: auto; }
  .grid { stroke: #d7cbda; stroke-dasharray: 4 5; stroke-width: 1; }
  .vertical { opacity: 0.85; }
  .axis-label, .turn-label { fill: #a38dac; font-size: 13px; }
  .baseline { stroke: #541060; stroke-dasharray: 5 5; stroke-width: 1.6; }
  .baseline-label { fill: #541060; font-size: 13px; font-weight: 900; }
  path { fill: none; stroke: #50105e; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; transition: d 500ms cubic-bezier(0.25, 0.1, 0.25, 1); }
  .reset { display: block; min-width: 0; margin: 1.2rem 0 0 auto; border-color: #a38dac; background: transparent; color: #8e7c94; box-shadow: none; text-transform: uppercase; }

  @media (max-width: 720px) {
    .charts { grid-template-columns: 1fr; }
    figcaption { min-height: 5.5rem; padding: 0.7rem; }
    .portrait { width: 4rem; height: 4rem; }
    figcaption em { top: 0.7rem; right: 0.7rem; }
  }

  @media (prefers-reduced-motion: reduce) {
    path, button { transition: none; }
  }
</style>
