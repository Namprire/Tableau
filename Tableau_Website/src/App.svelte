<script>
  import TaskQuiz from './lib/TaskQuiz.svelte';
  import ExposureScrolly from './lib/ExposureScrolly.svelte';
  import WorkdayScrolly from './lib/WorkdayScrolly.svelte';
  import HandoffSimulation from './lib/HandoffSimulation.svelte';
  import OccupationContrast from './lib/OccupationContrast.svelte';
  import ContextProfiles from './lib/ContextProfiles.svelte';
  import OccupationExplorer from './lib/OccupationExplorer.svelte';

  // Set this to false to remove the experimental simulation without deleting it.
  const showHandoffSimulation = true;
</script>

<svelte:head>
  <title>Who Does the Work? — AI, automation, and augmentation</title>
  <meta
    name="description"
    content="An interactive story about how generative AI redistributes workplace tasks between people and machines."
  />
</svelte:head>

<a class="skip-link" href="#story">Skip to the story</a>

<header class="site-header">
  <a class="brand" href="#top" aria-label="Who Does the Work? home">
    <span aria-hidden="true">W/AI</span>
    <strong>Who does the work?</strong>
  </a>
  <nav aria-label="Story navigation">
    <a href="#exposure-story">The evidence</a>
    <a href="#explore">Explore jobs</a>
    <a href="#method">Method</a>
  </nav>
</header>

<main id="top">
  <section class="hero" aria-labelledby="story-title">
    <div class="hero-copy">
      <p class="hero-kicker">A task-by-task view of generative AI at work</p>
      <h1 id="story-title">Who does<br />the <em>work?</em></h1>
      <p class="dek">
        The same AI can act like a worker in one moment and a copilot in the next. To see the
        difference, stop counting jobs—and open them up.
      </p>
      <p class="byline">An interactive analysis of 3,963 workplace tasks</p>
    </div>

    <div class="hero-illustration">
      <img
        src="/assets/story/ai-work-hero-money-palette.png"
        alt="A software worker and a friendly desktop AI robot sort workplace task cards together"
        fetchpriority="high"
        decoding="async"
      />
      <div class="hero-note note-worker" aria-hidden="true"><i></i>Human judgment</div>
      <div class="hero-note note-ai" aria-hidden="true"><i></i>AI execution</div>
    </div>

    <a class="scroll-cue" href="#story">
      <span>Open the job</span><i aria-hidden="true">↓</i>
    </a>
  </section>

  <article id="story" class="prose story-opening">
    <p class="opening-line">
      Ask whether AI will “automate a job,” and the answer is usually unsatisfying. Jobs are bundles:
      writing and checking, deciding and documenting, listening and producing.
    </p>
    <p>
      AI rarely enters every part of that bundle in the same way. Sometimes it receives an instruction
      and produces the output. Sometimes it helps a person learn, iterate, or validate a decision. We
      call those two broad roles <strong class="automation-text">automation</strong> and
      <strong class="augmentation-text">augmentation</strong>.
    </p>
    <p>
      Before looking at the full dataset, try three real workplace tasks. Which side do you think each
      one leans toward?
    </p>
  </article>

  <TaskQuiz />

  <section class="chapter-heading">
    <span>Chapter one</span>
    <h2>Where AI appears is only half the story.</h2>
    <p>Scroll through the evidence to separate exposure from the role AI actually plays.</p>
  </section>

  <ExposureScrolly />

  <article class="prose midpoint">
    <p class="section-kicker">From totals to tasks</p>
    <h2>A 43–57 split sounds simple. Work is not.</h2>
    <p>
      Across the exposure we could classify, augmentation is larger—but that average hides the
      decisions inside every occupation. Two tasks can sit in the same job, carry nearly the same
      exposure, and put AI in opposite roles.
    </p>
    <div class="job-box" aria-label="A job contains many different kinds of tasks">
      <strong>One job title</strong>
      <div>
        <span class="auto-chip">execute</span>
        <span class="aug-chip">advise</span>
        <span class="aug-chip">learn</span>
        <span class="auto-chip">draft</span>
        <span class="aug-chip">validate</span>
      </div>
      <small>Different tasks · different AI roles</small>
    </div>
  </article>

  <section class="chapter-heading left">
    <span>Chapter two</span>
    <h2>Open one workday.</h2>
    <p>A fictional worker helps us trace two real tasks from the same occupation.</p>
  </section>

  <WorkdayScrolly />

  {#if showHandoffSimulation}
    <HandoffSimulation />
  {/if}

  <OccupationContrast />
  <ContextProfiles />
  <OccupationExplorer />

  <section class="ending" aria-labelledby="ending-title">
    <div class="ending-copy">
      <p class="section-kicker">What the task view changes</p>
      <h2 id="ending-title">The future of work is a handoff, not a headline.</h2>
      <p>
        A single label cannot tell us who benefits, who decides, or what skills become more valuable.
        The more useful question is smaller and more concrete: for this task, does AI replace an act
        of work—or extend a person’s ability to do it?
      </p>
      <p class="closing-line">The answer changes task by task.</p>
    </div>
    <div class="ending-art" aria-hidden="true">
      <div class="worker-token"><i></i><b></b></div>
      <div class="handoff-card">?</div>
      <div class="bot-token"><i></i><b></b></div>
    </div>
  </section>

  <section id="method" class="method" aria-labelledby="method-title">
    <div>
      <p class="section-kicker">Method & limits</p>
      <h2 id="method-title">How to read this story</h2>
    </div>
    <div class="method-copy">
      <p>
        The supplied analysis dataset contains one row per occupation–task pair. We aggregate its
        exposure weights and conversation-mode measures into occupation, task, job-family, and Job
        Zone profiles. Directive and feedback-loop interactions are grouped as automation; iteration,
        learning, and validation are grouped as augmentation.
      </p>
      <p>
        Of 3,963 rows, 2,573 contain a usable role profile. Those rows represent 94.39% of total
        measured exposure. The results describe this dataset; they do not prove causal effects,
        predict layoffs, or measure every part of a job.
      </p>
      <p class="source-note">
        Source: the project’s supplied occupation–task analysis workbook. Values are rounded for display.
      </p>
    </div>
  </section>
</main>

<footer class="site-footer">
  <a class="footer-mark" href="#top">W/AI</a>
  <p>An original interactive story about people, tasks, and generative AI.</p>
  <a href="#top">Back to top ↑</a>
</footer>
