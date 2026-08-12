<script>
  import { quizTasks } from './storyData';

  let index = 0;
  let choice = null;
  let score = 0;
  let complete = false;

  $: task = quizTasks[index];
  $: correct = choice === task?.answer;

  function choose(nextChoice) {
    if (choice || complete) return;
    choice = nextChoice;
    if (nextChoice === task.answer) score += 1;
  }

  function advance() {
    if (!choice) return;
    if (index === quizTasks.length - 1) {
      complete = true;
      return;
    }
    index += 1;
    choice = null;
  }

  function reset() {
    index = 0;
    choice = null;
    score = 0;
    complete = false;
  }
</script>

<section class="quiz-shell" aria-labelledby="quiz-title">
  <div class="quiz-label">
    <span>Before we show you the data</span>
    <strong>{complete ? quizTasks.length : index + 1} / {quizTasks.length}</strong>
  </div>

  {#if !complete}
    <div class="quiz-card">
      <div class="task-tag"><i></i> Workplace task</div>
      <h2 id="quiz-title">When AI is used here, which role does it lean toward?</h2>
      <p class="task-copy">{task.prompt}</p>

      <div class="choice-grid" aria-label="Choose the AI role">
        <button
          class:chosen={choice === 'automation'}
          class:dimmed={choice && choice !== 'automation'}
          class="choice automation-choice"
          type="button"
          on:click={() => choose('automation')}
          disabled={Boolean(choice)}
        >
          <span class="choice-icon bot-icon" aria-hidden="true"><i></i><b></b></span>
          <span><strong>AI executes</strong><small>Automation</small></span>
        </button>

        <button
          class:chosen={choice === 'augmentation'}
          class:dimmed={choice && choice !== 'augmentation'}
          class="choice augmentation-choice"
          type="button"
          on:click={() => choose('augmentation')}
          disabled={Boolean(choice)}
        >
          <span class="choice-icon shared-icon" aria-hidden="true"><i></i><b></b></span>
          <span><strong>Human + AI</strong><small>Augmentation</small></span>
        </button>
      </div>

      {#if choice}
        <div class:correct class="answer" aria-live="polite">
          <strong>{correct ? 'You found the stronger signal.' : 'The data leans the other way.'}</strong>
          <p>{task.note}</p>
          <div class="mini-balance" aria-label={`${task.automation}% automation and ${task.augmentation}% augmentation`}>
            <span style:width={`${task.automation}%`}>AI {Math.round(task.automation)}%</span>
            <span style:width={`${task.augmentation}%`}>Together {Math.round(task.augmentation)}%</span>
          </div>
          <button class="next" type="button" on:click={advance}>
            {index === quizTasks.length - 1 ? 'See the story' : 'Next task'} <span aria-hidden="true">→</span>
          </button>
        </div>
      {/if}
    </div>
  {:else}
    <div class="quiz-card complete-card" aria-live="polite">
      <div class="score-ring"><strong>{score}</strong><span>of {quizTasks.length}</span></div>
      <div>
        <p class="eyebrow">Your result</p>
        <h2 id="quiz-title">The labels are harder than they look.</h2>
        <p>
          The same technology can execute one task and support human judgment on another. The rest
          of the story explains why occupation-level labels miss that distinction.
        </p>
        <div class="complete-actions">
          <a href="#exposure-story">Continue to the evidence <span aria-hidden="true">↓</span></a>
          <button type="button" on:click={reset}>Try again</button>
        </div>
      </div>
    </div>
  {/if}
</section>

<style>
  .quiz-shell {
    width: min(100% - 2rem, 62rem);
    margin: 0 auto 8rem;
  }

  .quiz-label {
    display: flex;
    justify-content: space-between;
    margin: 0 0 0.6rem;
    color: var(--ink-soft);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.09em;
    text-transform: uppercase;
  }

  .quiz-card {
    min-height: 31rem;
    padding: clamp(1.35rem, 4vw, 3.25rem);
    border: 2px solid var(--ink);
    border-radius: 0;
    background: var(--cream-light);
    box-shadow: none;
  }

  .task-tag,
  .eyebrow {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 0 1rem;
    color: var(--plum);
    font-size: 0.72rem;
    font-weight: 900;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  .task-tag i {
    width: 0.75rem;
    height: 0.75rem;
    border: 2px solid currentColor;
    border-radius: 50%;
    background: var(--gold);
  }

  h2 {
    max-width: 45rem;
    margin: 0;
    font-family: var(--display);
    font-size: clamp(1.7rem, 4vw, 3rem);
    font-weight: 950;
    letter-spacing: -0.05em;
    line-height: 0.94;
  }

  .task-copy {
    max-width: 43rem;
    min-height: 4.3rem;
    margin: 1.25rem 0 2rem;
    font-size: clamp(1.05rem, 2.2vw, 1.4rem);
    line-height: 1.45;
  }

  .choice-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
  }

  .choice {
    display: flex;
    align-items: center;
    gap: 1rem;
    min-height: 7rem;
    padding: 1rem 1.15rem;
    border: 2px solid var(--ink);
    border-radius: 0;
    color: var(--ink);
    text-align: left;
    cursor: pointer;
    transition: transform 180ms ease, box-shadow 180ms ease, opacity 180ms ease;
  }

  .choice:not(:disabled):hover,
  .choice.chosen {
    transform: translate(-3px, -3px);
    box-shadow: none;
  }

  .choice:disabled { cursor: default; }
  .choice.dimmed { opacity: 0.38; }
  .automation-choice { background: var(--automation-pale); }
  .augmentation-choice { background: var(--augmentation-pale); }

  .choice > span:last-child { display: grid; gap: 0.15rem; }
  .choice strong { font-size: 1.05rem; }
  .choice small { color: var(--ink-soft); }

  .choice-icon {
    position: relative;
    width: 3.4rem;
    height: 3.4rem;
    flex: 0 0 auto;
  }

  .bot-icon i {
    position: absolute;
    inset: 0.55rem 0.2rem 0.25rem;
    border: 2px solid var(--ink);
    border-radius: 0.2rem;
    background: var(--automation);
  }

  .bot-icon i::before,
  .bot-icon i::after {
    position: absolute;
    top: 0.75rem;
    width: 0.35rem;
    height: 0.45rem;
    border-radius: 50%;
    background: var(--ink);
    content: '';
  }

  .bot-icon i::before { left: 0.7rem; }
  .bot-icon i::after { right: 0.7rem; }
  .bot-icon b { position: absolute; top: 0; left: 50%; width: 2px; height: 0.75rem; background: var(--ink); }
  .bot-icon b::after { position: absolute; top: -0.2rem; left: -0.18rem; width: 0.4rem; height: 0.4rem; border: 2px solid var(--ink); border-radius: 50%; background: var(--gold); content: ''; }

  .shared-icon i,
  .shared-icon b {
    position: absolute;
    top: 0.4rem;
    width: 2.05rem;
    height: 2.65rem;
    border: 2px solid var(--ink);
    border-radius: 1.2rem 1.2rem 0.6rem 0.6rem;
  }

  .shared-icon i { left: 0; background: var(--gold); }
  .shared-icon b { right: 0; background: var(--augmentation); }

  .answer {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 0.35rem 1rem;
    margin-top: 1.2rem;
    padding-top: 1.1rem;
    border-top: 1px solid var(--line);
  }

  .answer > strong { color: var(--automation-dark); }
  .answer.correct > strong { color: var(--augmentation-dark); }
  .answer p { margin: 0; color: var(--ink-soft); font-size: 0.9rem; }

  .mini-balance {
    grid-column: 1 / -1;
    display: flex;
    height: 1.8rem;
    margin-top: 0.6rem;
    overflow: hidden;
    border: 1px solid var(--ink);
    border-radius: 0;
    font-size: 0.66rem;
    font-weight: 900;
  }

  .mini-balance span { display: grid; place-items: center; white-space: nowrap; }
  .mini-balance span:first-child { background: var(--automation); }
  .mini-balance span:last-child { background: var(--augmentation); color: white; }

  .next {
    grid-column: 2;
    grid-row: 1 / 3;
    align-self: center;
    padding: 0.75rem 1rem;
    border: 2px solid var(--ink);
    border-radius: 0;
    background: var(--ink);
    color: white;
    font-weight: 850;
    cursor: pointer;
  }

  .complete-card {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    gap: clamp(1.5rem, 5vw, 4rem);
  }

  .score-ring {
    display: grid;
    place-content: center;
    width: clamp(8rem, 18vw, 12rem);
    aspect-ratio: 1;
    border: 3px solid var(--ink);
    border-radius: 50%;
    background: var(--gold);
    box-shadow: none;
    text-align: center;
  }

  .score-ring strong { font-family: var(--display); font-size: clamp(3rem, 8vw, 5rem); line-height: 0.8; }
  .score-ring span { margin-top: 0.55rem; font-size: 0.72rem; font-weight: 900; text-transform: uppercase; }
  .complete-card p:not(.eyebrow) { max-width: 38rem; line-height: 1.55; }
  .complete-actions { display: flex; align-items: center; gap: 1.1rem; margin-top: 1.5rem; }
  .complete-actions a { padding: 0.8rem 1rem; border-radius: 0; background: var(--ink); color: white; font-weight: 850; text-decoration: none; }
  .complete-actions button { border: 0; background: transparent; color: var(--ink-soft); text-decoration: underline; cursor: pointer; }

  @media (max-width: 650px) {
    .quiz-shell { margin-bottom: 6rem; }
    .quiz-card { min-height: 0; box-shadow: none; }
    .choice-grid { grid-template-columns: 1fr; }
    .choice { min-height: 5.6rem; }
    .answer { grid-template-columns: 1fr; }
    .next { grid-column: 1; grid-row: auto; justify-self: start; margin-top: 0.5rem; }
    .complete-card { grid-template-columns: 1fr; }
    .score-ring { width: 8rem; }
    .complete-actions { align-items: flex-start; flex-direction: column; }
  }

  @media (prefers-reduced-motion: reduce) {
    .choice { transition: none; }
  }
</style>
