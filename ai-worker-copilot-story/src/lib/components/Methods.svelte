<script lang="ts">
  export let taskRows = 3963;
  export let occupations = 731;
  export let classifiedOccupations = 597;
</script>

<section class="methods section-shell" aria-labelledby="methods-title">
  <div class="conclusion">
    <p class="section-index">The takeaway</p>
    <h2>AI’s role is determined task by task—not by a job title or paycheck alone.</h2>
    <p>Higher-preparation occupations account for most observed use. But the worker–copilot balance changes across occupational families, Job Zones, and the individual activities people ask AI to support.</p>
  </div>

  <details>
    <summary id="methods-title">Methods & limitations <span>+</span></summary>
    <div class="methods-grid">
      <div><h3>Data</h3><p>{taskRows.toLocaleString('en-US')} cleaned occupation-task rows covering {occupations} occupations. Exposure measures the share of observed workplace AI conversations associated with each occupation-task pair.</p></div>
      <div><h3>Classification</h3><p>Worker combines directive and feedback-loop interactions. Copilot combines task iteration, validation, and learning. {classifiedOccupations} occupations have a valid role classification.</p></div>
      <div><h3>Interpret carefully</h3><p>This is a description of observed AI interaction patterns—not a forecast of job loss, a measure of productivity, or proof that an occupation will be automated.</p></div>
      <div><h3>Sources</h3><p>Anthropic Economic Index interaction data, O*NET occupation and Job Zone classifications, and BLS salary information as prepared in the course dataset.</p></div>
    </div>
  </details>
</section>

<footer class="footer section-shell">
  <p>Who is working—AI or me?</p>
  <p>Interactive data story · Prototype</p>
</footer>

<style>
  .methods { padding-top: 8rem; padding-bottom: 5rem; }
  .conclusion { display: grid; grid-template-columns: 10rem minmax(0, 1fr) minmax(15rem, 0.48fr); gap: clamp(2rem, 5vw, 5rem); align-items: start; padding-bottom: 7rem; }
  .section-index { color: var(--worker); font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }
  h2 { max-width: 14ch; margin: 0; font-family: var(--display); font-size: clamp(2.8rem, 5.7vw, 6rem); font-weight: 520; letter-spacing: -0.055em; line-height: 0.95; }
  .conclusion > p:last-child { margin: 0; color: var(--muted-dark); font-size: 1.04rem; line-height: 1.65; }
  details { border-top: 1px solid var(--line-strong); border-bottom: 1px solid var(--line-strong); }
  summary { display: flex; justify-content: space-between; padding: 1.5rem 0; cursor: pointer; font-size: 0.78rem; font-weight: 800; letter-spacing: 0.1em; list-style: none; text-transform: uppercase; }
  summary::-webkit-details-marker { display: none; }
  summary span { font-size: 1.2rem; }
  details[open] summary span { transform: rotate(45deg); }
  .methods-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; padding: 1rem 0 2.5rem; }
  h3 { margin: 0 0 0.7rem; font-family: var(--display); font-size: 1.35rem; }
  .methods-grid p { margin: 0; color: var(--muted-dark); font-size: 0.84rem; line-height: 1.62; }
  .footer { display: flex; justify-content: space-between; gap: 2rem; padding-top: 2rem; padding-bottom: 2rem; border-top: 1px solid var(--line-strong); color: var(--muted); font-size: 0.72rem; font-weight: 750; letter-spacing: 0.08em; text-transform: uppercase; }
  @media (max-width: 900px) {
    .conclusion { grid-template-columns: 1fr; }
    .methods-grid { grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 560px) {
    .methods-grid { grid-template-columns: 1fr; }
    .footer { flex-direction: column; }
  }
</style>
