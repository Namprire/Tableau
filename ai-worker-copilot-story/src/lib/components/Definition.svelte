<section class="definition section-shell" aria-labelledby="definition-title">
  <div class="intro-copy">
    <p class="section-index">Before we begin</p>
    <h2 id="definition-title">“Worker” and “copilot” describe a pattern of interaction—not whether a job disappears.</h2>
  </div>

  <div class="role-grid">
    <article class="role worker-card">
      <span class="role-number">01</span>
      <div>
        <p class="role-label">AI as worker</p>
        <h3>Delegated execution</h3>
        <p>The user asks for an outcome. AI directly performs the task or completes it through a feedback loop.</p>
        <p class="modes">Directive + feedback loop</p>
      </div>
    </article>

    <div class="continuum" aria-hidden="true">
      <span></span><span></span><span></span><span></span><span></span>
    </div>

    <article class="role copilot-card">
      <span class="role-number">02</span>
      <div>
        <p class="role-label">AI as copilot</p>
        <h3>Human-in-the-loop support</h3>
        <p>The human remains involved while AI helps iterate, validate work, or explain and teach.</p>
        <p class="modes">Iteration + validation + learning</p>
      </div>
    </article>
  </div>
</section>

<style>
  .definition { padding-top: 7rem; padding-bottom: 8rem; }
  .intro-copy { display: grid; grid-template-columns: 11rem minmax(0, 45rem); gap: 2rem; }
  .section-index { color: var(--muted); font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }
  h2 { margin: 0; font-family: var(--display); font-size: clamp(2.1rem, 4vw, 4rem); font-weight: 520; letter-spacing: -0.04em; line-height: 1.05; }
  .role-grid { display: grid; grid-template-columns: 1fr 5rem 1fr; align-items: center; margin-top: 5rem; }
  .role { min-height: 20rem; display: grid; grid-template-columns: 3rem 1fr; gap: 1rem; padding: clamp(1.5rem, 4vw, 3.2rem); border: 1px solid var(--line-strong); }
  .worker-card { background: color-mix(in srgb, var(--worker) 8%, transparent); }
  .copilot-card { background: color-mix(in srgb, var(--copilot) 8%, transparent); }
  .role-number { color: var(--muted); font-size: 0.72rem; font-weight: 780; letter-spacing: 0.08em; }
  .role-label { margin: 0 0 1.5rem; color: var(--muted-dark); font-size: 0.76rem; font-weight: 800; letter-spacing: 0.13em; text-transform: uppercase; }
  h3 { max-width: 10ch; margin: 0 0 1rem; font-family: var(--display); font-size: clamp(2.1rem, 3.6vw, 3.5rem); font-weight: 520; letter-spacing: -0.04em; line-height: 0.98; }
  .role p:not(.role-label, .modes) { max-width: 28rem; color: var(--muted-dark); line-height: 1.6; }
  .modes { margin-top: 2.2rem; font-size: 0.76rem; font-weight: 780; letter-spacing: 0.07em; text-transform: uppercase; }
  .worker-card .modes { color: var(--worker-dark); }
  .copilot-card .modes { color: var(--copilot); }
  .continuum { display: flex; align-items: center; justify-content: space-around; position: relative; z-index: 2; }
  .continuum::before { position: absolute; width: 140%; height: 1px; background: var(--line-strong); content: ''; }
  .continuum span { z-index: 1; width: 0.45rem; height: 0.45rem; border: 2px solid var(--paper); border-radius: 50%; background: var(--gold); }
  @media (max-width: 820px) {
    .intro-copy { grid-template-columns: 1fr; }
    .role-grid { grid-template-columns: 1fr; }
    .continuum { height: 4rem; transform: rotate(90deg); }
  }
</style>
