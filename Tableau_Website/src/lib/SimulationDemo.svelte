<script>
  import { onMount } from 'svelte';

  const playerCount = 100;
  const targetRounds = 1000;
  const chartMaximum = 40000;
  const ticks = [0, 10000, 20000, 30000, 40000];

  let wagerPercent = 20;
  let redistributionPercent = 0;
  let rounds = 0;
  let wealth = Array(playerCount).fill(1000);
  let running = false;
  let frameId = 0;
  let randomState = 202301;

  function random() {
    randomState = (randomState * 1664525 + 1013904223) >>> 0;
    return randomState / 4294967296;
  }

  function simulateRound() {
    const order = Array.from({ length: playerCount }, (_, index) => index);
    for (let index = order.length - 1; index > 0; index -= 1) {
      const swapIndex = Math.floor(random() * (index + 1));
      [order[index], order[swapIndex]] = [order[swapIndex], order[index]];
    }

    for (let index = 0; index < order.length; index += 2) {
      const first = order[index];
      const second = order[index + 1];
      const wager = Math.min(wealth[first], wealth[second]) * (wagerPercent / 100);
      const winner = random() > 0.5 ? first : second;
      const loser = winner === first ? second : first;
      wealth[winner] += wager;
      wealth[loser] = Math.max(0, wealth[loser] - wager);
    }

    if (redistributionPercent > 0) {
      const rate = redistributionPercent / 100;
      let pool = 0;
      for (let index = 0; index < wealth.length; index += 1) {
        const contribution = wealth[index] * rate;
        wealth[index] -= contribution;
        pool += contribution;
      }
      const share = pool / playerCount;
      for (let index = 0; index < wealth.length; index += 1) wealth[index] += share;
    }
  }

  function animate() {
    const roundsThisFrame = Math.min(8, targetRounds - rounds);
    for (let index = 0; index < roundsThisFrame; index += 1) simulateRound();
    rounds += roundsThisFrame;
    wealth = [...wealth].sort((a, b) => a - b);

    if (rounds < targetRounds) frameId = requestAnimationFrame(animate);
    else running = false;
  }

  function play() {
    if (running || rounds >= targetRounds) return;
    running = true;
    frameId = requestAnimationFrame(animate);
  }

  function reset() {
    cancelAnimationFrame(frameId);
    running = false;
    rounds = 0;
    randomState = 202301;
    wealth = Array(playerCount).fill(1000);
  }

  onMount(() => () => cancelAnimationFrame(frameId));
</script>

<section class="simulation" aria-labelledby="simulation-title">
  <header>
    <p>Adjust the model</p>
    <h3 id="simulation-title">Run the game for 1,000 rounds.</h3>
  </header>

  <div class="controls">
    <label>
      <span>Maximum wager</span>
      <input type="range" min="5" max="40" step="1" bind:value={wagerPercent} disabled={running} />
      <b>{wagerPercent}%</b>
    </label>
    <label>
      <span>Redistribution</span>
      <input type="range" min="0" max="2" step="0.1" bind:value={redistributionPercent} disabled={running} />
      <b>{Number(redistributionPercent).toFixed(1)}%</b>
    </label>
  </div>

  <figure>
    <div class="chart-head">
      <span>Round: <strong>{rounds.toLocaleString()}</strong></span>
      <button on:click={play} disabled={running || rounds >= targetRounds}>
        {running ? 'Simulating…' : rounds ? 'Continue simulation' : 'Play simulation'}
      </button>
    </div>

    <svg viewBox="0 0 1000 620" role="img" aria-label={`Wealth distribution after ${rounds} rounds.`}>
      <g class="grid">
        {#each ticks as tick}
          <line x1="55" x2="960" y1={540 - (tick / chartMaximum) * 440} y2={540 - (tick / chartMaximum) * 440}></line>
          <text x="15" y={532 - (tick / chartMaximum) * 440}>${tick.toLocaleString()}</text>
        {/each}
      </g>
      <g class="bars">
        {#each wealth as value, index}
          <rect
            class:richest={index === wealth.length - 1}
            x={70 + index * 8.85}
            y="100"
            width="6.5"
            height="440"
            style:transform={`scaleY(${Math.max(0.002, Math.min(1, value / chartMaximum))})`}
          ></rect>
        {/each}
      </g>
    </svg>

    <button class="reset" on:click={reset} disabled={rounds === 0}>Reset</button>
  </figure>
</section>

<style>
  .simulation { width: min(100% - 2rem, 88rem); margin: 4rem auto 8rem; }
  header { max-width: 42rem; margin: 0 auto 2rem; text-align: center; }
  header p { margin: 0 0 0.55rem; color: var(--magenta); font-size: 0.72rem; font-weight: 850; letter-spacing: 0.1em; text-transform: uppercase; }
  h3 { margin: 0; font-size: clamp(1.7rem, 4vw, 2.8rem); line-height: 1.05; }
  .controls { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; max-width: 56rem; margin: 0 auto 1.4rem; }
  label { display: grid; grid-template-columns: 1fr auto; gap: 0.45rem 0.8rem; color: #5d5260; font-size: 0.82rem; }
  label input { grid-column: 1 / -1; width: 100%; accent-color: var(--purple); }
  label b { color: var(--purple); }
  figure { position: relative; margin: 0; padding: 1.2rem; border: 1px solid #a996ae; background: rgba(255,255,255,0.82); }
  .chart-head { display: flex; align-items: center; justify-content: space-between; padding: 0.5rem 0.2rem 0; color: #171319; font-size: clamp(1rem, 2vw, 1.3rem); }
  .chart-head strong { color: #4f0e5d; font-weight: 900; }
  button { padding: 0.7rem 2rem; border: 2px solid #9f84ae; background: #faedf8; color: #4f0e5d; font-weight: 900; cursor: pointer; box-shadow: 4px 4px 0 #9f84ae; }
  button:disabled { color: #888; cursor: not-allowed; opacity: 0.76; }
  svg { display: block; width: 100%; margin-top: 0.5rem; }
  .grid line { stroke: rgba(71,55,77,0.3); stroke-dasharray: 5 6; }
  .grid text { fill: #58515a; font-size: 14px; }
  .bars rect { fill: #9a91cc; transform-box: fill-box; transform-origin: center bottom; transition: transform 140ms linear; }
  .bars rect.richest { fill: #4f006d; }
  .reset { display: block; margin: -0.3rem 0 0 auto; padding: 0.45rem 0.8rem; background: transparent; box-shadow: none; text-transform: uppercase; }

  @media (max-width: 680px) {
    .controls { grid-template-columns: 1fr; }
    figure { padding: 0.7rem; }
    .chart-head { align-items: flex-start; gap: 0.8rem; }
    .chart-head button { padding: 0.5rem 0.7rem; font-size: 0.7rem; }
  }

  @media (prefers-reduced-motion: reduce) {
    .bars rect { transition: none; }
  }
</style>
