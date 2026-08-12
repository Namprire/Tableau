import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = "/Users/nampham/Documents/Blended/Tableau";
const BUILD = path.join(ROOT, "tmp/final_slides/build");
const RENDER_DIR = path.join(BUILD, "rendered");
const LAYOUT_DIR = path.join(BUILD, "layouts");
const FINAL_PPTX = path.join(ROOT, "output/Who_Does_the_Work_Tableau_Final_Project.pptx");

const W = 1280;
const H = 720;
const FONT = "Aptos";

const C = {
  paper: "#F7F5F0",
  white: "#FFFFFF",
  ink: "#18232D",
  ink2: "#273744",
  muted: "#65717A",
  faint: "#D8D6D0",
  soft: "#ECE9E2",
  coral: "#E4575B",
  coralDark: "#B9383F",
  teal: "#77B7B2",
  tealDark: "#397F7A",
  blue: "#5B86AE",
  orange: "#F39A43",
  green: "#2F713D",
  gold: "#F1C75B",
};

async function imageBytes(relPath) {
  const bytes = await fs.readFile(path.join(ROOT, relPath));
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

function addText(slide, text, position, style = {}, name = "text") {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name,
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    typeface: FONT,
    fontSize: 23,
    color: C.ink,
    alignment: "left",
    verticalAlignment: "top",
    autoFit: "none",
    wrap: "square",
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
    ...style,
  };
  return shape;
}

function addRect(slide, position, fill, opts = {}) {
  return slide.shapes.add({
    geometry: opts.geometry ?? "rect",
    name: opts.name ?? "rect",
    position,
    fill,
    line: opts.line ?? { style: "solid", fill: "none", width: 0 },
    ...(opts.borderRadius !== undefined ? { borderRadius: opts.borderRadius } : {}),
    ...(opts.shadow ? { shadow: opts.shadow } : {}),
  });
}

function addLine(slide, x, y, width, color = C.faint, weight = 1, name = "line") {
  return slide.shapes.add({
    geometry: "line",
    name,
    position: { left: x, top: y, width, height: 0 },
    fill: "none",
    line: { style: "solid", fill: color, width: weight },
  });
}

function addCircle(slide, x, y, diameter, fill, name = "circle") {
  return slide.shapes.add({
    geometry: "ellipse",
    name,
    position: { left: x, top: y, width: diameter, height: diameter },
    fill,
    line: { style: "solid", fill: "none", width: 0 },
  });
}

function addHeader(slide, section, title, page, options = {}) {
  slide.background.fill = options.dark ? C.ink : C.paper;
  const fg = options.dark ? C.white : C.ink;
  const muted = options.dark ? "#C8D0D6" : C.muted;
  addText(
    slide,
    section.toUpperCase(),
    { left: 68, top: 34, width: 560, height: 24 },
    { fontSize: 16, bold: true, color: options.accent ?? C.coral },
    `section-${page}`,
  );
  addText(
    slide,
    String(page).padStart(2, "0"),
    { left: 1160, top: 34, width: 52, height: 24 },
    { fontSize: 16, bold: true, color: muted, alignment: "right" },
    `page-${page}`,
  );
  addText(
    slide,
    title,
    { left: 68, top: 70, width: 1144, height: options.titleHeight ?? 106 },
    { fontSize: options.titleSize ?? 48, bold: true, color: fg },
    `title-${page}`,
  );
}

function addFooter(slide, page, dark = false) {
  const line = dark ? "#52606B" : C.faint;
  const text = dark ? "#AEB9C1" : C.muted;
  addLine(slide, 68, 684, 1144, line, 1, `footer-line-${page}`);
  addText(
    slide,
    "AI AT WORK  /  TABLEAU FINAL PROJECT",
    { left: 68, top: 692, width: 480, height: 18 },
    { fontSize: 13, bold: true, color: text },
    `footer-label-${page}`,
  );
}

async function addImageFrame(slide, relPath, position, alt, name) {
  addRect(
    slide,
    { left: position.left - 6, top: position.top - 6, width: position.width + 12, height: position.height + 12 },
    C.white,
    {
      geometry: "roundRect",
      name: `${name}-backing`,
      borderRadius: 10,
      line: { style: "solid", fill: "#CBCBC6", width: 1 },
      shadow: "shadow-sm",
    },
  );
  return slide.images.add({
    blob: await imageBytes(relPath),
    contentType: "image/jpeg",
    alt,
    fit: "contain",
    position,
    geometry: "roundRect",
    borderRadius: 8,
    name,
  });
}

function setNotes(slide, body, sources) {
  const notes = `${body}\n\n[Sources]\n${sources.map((s) => `- ${s}`).join("\n")}`;
  slide.speakerNotes.textFrame.setText(notes);
}

function addBullet(slide, x, y, width, heading, body, color, index, bodyHeight = 64) {
  addRect(slide, { left: x, top: y + 4, width: 5, height: bodyHeight - 4 }, color, {
    name: `bullet-accent-${index}`,
  });
  addText(
    slide,
    heading,
    { left: x + 22, top: y, width: width - 22, height: 40 },
    { fontSize: 32, bold: true, color: C.ink },
    `bullet-heading-${index}`,
  );
  addText(
    slide,
    body,
    { left: x + 22, top: y + 44, width: width - 22, height: bodyHeight - 40 },
    { fontSize: 22, color: C.muted },
    `bullet-body-${index}`,
  );
}

async function build() {
  await fs.mkdir(RENDER_DIR, { recursive: true });
  await fs.mkdir(LAYOUT_DIR, { recursive: true });
  await fs.mkdir(path.dirname(FINAL_PPTX), { recursive: true });

  const presentation = Presentation.create({
    slideSize: { width: W, height: H },
  });

  // Slide 1: Minimal title.
  {
    const slide = presentation.slides.add();
    slide.background.fill = C.paper;
    addRect(slide, { left: 0, top: 0, width: 14, height: H }, C.ink, { name: "title-left-rule" });
    addText(
      slide,
      "TABLEAU FINAL PROJECT",
      { left: 76, top: 70, width: 420, height: 26 },
      { fontSize: 18, bold: true, color: C.coral },
      "title-eyebrow",
    );
    addRect(slide, { left: 76, top: 142, width: 7, height: 188 }, C.ink, { name: "title-mark" });
    addText(
      slide,
      "Who Does the Work?",
      { left: 108, top: 136, width: 980, height: 96 },
      { fontSize: 78, bold: true, color: C.ink },
      "deck-title",
    );
    addText(
      slide,
      "How generative AI is reshaping the division of labor\nbetween humans and machines",
      { left: 110, top: 254, width: 970, height: 96 },
      { fontSize: 34, color: C.ink2 },
      "deck-subtitle",
    );
    addText(
      slide,
      "Central question",
      { left: 110, top: 406, width: 230, height: 28 },
      { fontSize: 18, bold: true, color: C.muted },
      "central-question-label",
    );
    addText(
      slide,
      "How is generative AI reorganizing the division of work between people and machines?",
      { left: 110, top: 440, width: 930, height: 60 },
      { fontSize: 27, bold: true, color: C.ink },
      "central-question",
    );
    addText(
      slide,
      "AUGUST 2026",
      { left: 76, top: 558, width: 260, height: 24 },
      { fontSize: 16, bold: true, color: C.muted },
      "title-date",
    );
    addRect(slide, { left: 0, top: 610, width: 520, height: 110 }, C.teal, { name: "executor-band" });
    addRect(slide, { left: 520, top: 610, width: 760, height: 110 }, C.coral, { name: "copilot-band" });
    addText(
      slide,
      "AI AS EXECUTOR",
      { left: 76, top: 646, width: 360, height: 32 },
      { fontSize: 23, bold: true, color: C.white },
      "executor-label",
    );
    addText(
      slide,
      "AI AS COPILOT",
      { left: 566, top: 646, width: 390, height: 32 },
      { fontSize: 23, bold: true, color: C.white },
      "copilot-label",
    );
    setNotes(
      slide,
      "Open with the distinction between AI presence and AI role. The project asks how work is divided, not simply whether a job is exposed.",
      [
        "AI_at_Work_Four_Question_Research_Story.docx (internal project narrative)",
        "figures/AI_at_Work_Unified_Dataset_Documentation.docx (internal metric definitions)",
      ],
    );
  }

  // Slide 2: Problem framing and analytical sequence.
  {
    const slide = presentation.slides.add();
    addHeader(
      slide,
      "The problem",
      "AI exposure does not tell us whether it replaces\nor supports work.",
      2,
      { titleHeight: 108 },
    );

    addText(
      slide,
      "Exposure",
      { left: 72, top: 236, width: 220, height: 34 },
      { fontSize: 32, bold: true, color: C.tealDark },
      "exposure-label",
    );
    addText(
      slide,
      "How much AI is used",
      { left: 72, top: 274, width: 350, height: 34 },
      { fontSize: 23, color: C.ink },
      "exposure-definition",
    );
    addText(
      slide,
      "Role",
      { left: 72, top: 346, width: 220, height: 34 },
      { fontSize: 32, bold: true, color: C.coralDark },
      "role-label",
    );
    addText(
      slide,
      "What AI does when it is used",
      { left: 72, top: 384, width: 390, height: 34 },
      { fontSize: 23, color: C.ink },
      "role-definition",
    );
    addRect(slide, { left: 486, top: 226, width: 6, height: 210 }, C.ink, { name: "problem-divider" });
    addText(
      slide,
      "The question is not only where AI appears.\nIt is whether AI executes the task, supports the worker, or does both inside the same occupation.",
      { left: 530, top: 225, width: 650, height: 210 },
      { fontSize: 33, bold: true, color: C.ink },
      "problem-question",
    );

    // Connector first, then nodes.
    addLine(slide, 118, 548, 1032, C.faint, 3, "research-sequence-line");
    const steps = [
      { x: 92, n: "01", h: "WHERE", b: "Locate AI" },
      { x: 366, n: "02", h: "ROLE", b: "Executor or copilot?" },
      { x: 640, n: "03", h: "TASKS", b: "Open the job black box" },
      { x: 914, n: "04", h: "CONTEXT", b: "Preparation and occupation" },
    ];
    steps.forEach((step, i) => {
      addCircle(slide, step.x, 526, 44, i % 2 === 0 ? C.teal : C.coral, `sequence-node-${i + 1}`);
      addText(
        slide,
        step.n,
        { left: step.x, top: 536, width: 44, height: 22 },
        { fontSize: 15, bold: true, color: C.white, alignment: "center" },
        `sequence-number-${i + 1}`,
      );
      addText(
        slide,
        step.h,
        { left: step.x - 6, top: 584, width: 198, height: 28 },
        { fontSize: 22, bold: true, color: C.ink },
        `sequence-heading-${i + 1}`,
      );
      addText(
        slide,
        step.b,
        { left: step.x - 6, top: 614, width: 230, height: 50 },
        { fontSize: 22, color: C.muted },
        `sequence-body-${i + 1}`,
      );
    });
    addFooter(slide, 2);
    setNotes(
      slide,
      "Use the sequence to frame the dashboard: locate AI, identify its role, inspect variation across tasks, then place the pattern in occupational context.",
      ["AI_at_Work_Four_Question_Research_Story.docx (internal research-question map)"],
    );
  }

  // Slide 3: Dataset and metric logic.
  {
    const slide = presentation.slides.add();
    addHeader(
      slide,
      "How we answer it",
      "One occupation-task dataset connects AI presence to AI's role.",
      3,
      { titleHeight: 92 },
    );

    addText(
      slide,
      "3,963",
      { left: 70, top: 176, width: 330, height: 72 },
      { fontSize: 58, bold: true, color: C.coral },
      "row-count",
    );
    addText(
      slide,
      "occupation-task pairs",
      { left: 72, top: 244, width: 330, height: 32 },
      { fontSize: 23, bold: true, color: C.ink },
      "row-count-label",
    );
    addLine(slide, 72, 294, 382, C.faint, 2, "metric-rule-1");
    addText(
      slide,
      "731 occupations  /  5 interaction modes",
      { left: 72, top: 314, width: 385, height: 62 },
      { fontSize: 24, bold: true, color: C.ink },
      "dataset-scope",
    );
    addText(
      slide,
      "Automation",
      { left: 72, top: 400, width: 220, height: 40 },
      { fontSize: 32, bold: true, color: C.tealDark },
      "automation-heading",
    );
    addText(
      slide,
      "directive + feedback loop",
      { left: 72, top: 444, width: 360, height: 32 },
      { fontSize: 22, color: C.muted },
      "automation-formula",
    );
    addText(
      slide,
      "Augmentation",
      { left: 72, top: 492, width: 250, height: 40 },
      { fontSize: 32, bold: true, color: C.coralDark },
      "augmentation-heading",
    );
    addText(
      slide,
      "iteration + validation + learning",
      { left: 72, top: 536, width: 390, height: 54 },
      { fontSize: 22, color: C.muted },
      "augmentation-formula",
    );
    addText(
      slide,
      "Role balance = augmentation - automation",
      { left: 72, top: 610, width: 410, height: 50 },
      { fontSize: 22, bold: true, color: C.ink },
      "role-balance-formula",
    );

    await addImageFrame(
      slide,
      "figures/20260812-005545.jpeg",
      { left: 520, top: 184, width: 690, height: 405 },
      "Tableau dashboard showing task-level AI role balance and interaction modes by job family",
      "method-dashboard",
    );
    addText(
      slide,
      "Grain: one unique soc_code x task_id pair",
      { left: 520, top: 610, width: 500, height: 24 },
      { fontSize: 17, color: C.muted },
      "grain-note",
    );
    addFooter(slide, 3);
    setNotes(
      slide,
      "Explain that exposure answers how much AI is observed, while the five interaction modes classify what AI is doing. Valid role observations require complete interactions, positive exposure, and the quality filter.",
      [
        "figures/AI_at_Work_Unified_Dataset_Documentation.docx (dataset grain and metric definitions)",
        "analysis_dataset.csv (3,963 rows; 731 distinct occupations)",
        "figures/20260812-005545.jpeg (team-provided Tableau export)",
      ],
    );
  }

  // Slide 4: Concentration finding.
  {
    const slide = presentation.slides.add();
    addHeader(
      slide,
      "Finding 1 - where AI enters work",
      "Observed AI use is concentrated in a small set\nof occupational families.",
      4,
      { titleHeight: 108, accent: C.green },
    );

    await addImageFrame(
      slide,
      "figures/20260812-013036.jpeg",
      { left: 62, top: 184, width: 806, height: 475 },
      "Tableau dashboard showing concentration of AI exposure by occupational family, occupation, and shared-task category",
      "concentration-dashboard",
    );
    addText(
      slide,
      "~39%",
      { left: 910, top: 202, width: 260, height: 74 },
      { fontSize: 60, bold: true, color: C.green },
      "concentration-stat",
    );
    addText(
      slide,
      "of observed AI exposure comes from Computer & Mathematical occupations.",
      { left: 912, top: 276, width: 295, height: 116 },
      { fontSize: 24, bold: true, color: C.ink },
      "concentration-stat-label",
    );
    addLine(slide, 912, 416, 285, C.faint, 2, "concentration-rule");
    addText(
      slide,
      "Concentration continues inside families: a few occupations and tasks account for much of the total.",
      { left: 912, top: 440, width: 290, height: 132 },
      { fontSize: 22, color: C.ink2 },
      "concentration-insight",
    );
    addText(
      slide,
      "Observed AI conversations - not employment share",
      { left: 912, top: 608, width: 292, height: 42 },
      { fontSize: 17, color: C.muted },
      "concentration-caveat",
    );
    addFooter(slide, 4);
    setNotes(
      slide,
      "Lead with concentration, then point to the treemap: AI enters the workplace through specific occupations and tasks rather than diffusing evenly across all work.",
      [
        "figures/20260812-013036.jpeg (team-provided Tableau export; 38.89% shown in the view)",
        "analysis_dataset.csv (occupation-family exposure verification)",
      ],
    );
  }

  // Slide 5: Overall automation/augmentation finding.
  {
    const slide = presentation.slides.add();
    addHeader(
      slide,
      "Finding 2 - what role AI plays",
      "Across observed AI use, augmentation leads\nautomation 57% to 43%.",
      5,
      { titleHeight: 108 },
    );

    addText(
      slide,
      "57%",
      { left: 72, top: 202, width: 300, height: 74 },
      { fontSize: 62, bold: true, color: C.coral },
      "augmentation-stat",
    );
    addText(
      slide,
      "augmentation / copilot",
      { left: 74, top: 278, width: 380, height: 42 },
      { fontSize: 32, bold: true, color: C.ink },
      "augmentation-stat-label",
    );
    addText(
      slide,
      "43%",
      { left: 72, top: 346, width: 300, height: 74 },
      { fontSize: 62, bold: true, color: C.tealDark },
      "automation-stat",
    );
    addText(
      slide,
      "automation / executor",
      { left: 74, top: 422, width: 380, height: 42 },
      { fontSize: 32, bold: true, color: C.ink },
      "automation-stat-label",
    );
    addLine(slide, 74, 486, 370, C.faint, 2, "role-stat-rule");
    addText(
      slide,
      "Directive is the largest single mode (30.5%), while learning + iteration contribute 53.3% together.",
      { left: 74, top: 510, width: 380, height: 126 },
      { fontSize: 22, color: C.ink2 },
      "interaction-mode-callout",
    );

    await addImageFrame(
      slide,
      "figures/20260812-005601.jpeg",
      { left: 500, top: 188, width: 710, height: 420 },
      "Tableau dashboard showing overall augmentation versus automation and five human-AI interaction modes",
      "overall-role-dashboard",
    );
    addText(
      slide,
      "AI behaves more like a copilot overall, even though direct execution remains the largest single interaction mode.",
      { left: 500, top: 620, width: 710, height: 54 },
      { fontSize: 22, bold: true, color: C.ink },
      "overall-role-takeaway",
    );
    addFooter(slide, 5);
    setNotes(
      slide,
      "Emphasize the distinction between the largest single mode and the overall grouped result: directive is the largest mode, but augmentation modes together produce the 57% majority.",
      [
        "figures/20260812-005601.jpeg (team-provided Tableau export)",
        "analysis_dataset.csv (56.98% augmentation; 43.02% automation; interaction-mode shares)",
      ],
    );
  }

  // Slide 6: Task-level variation.
  {
    const slide = presentation.slides.add();
    addHeader(
      slide,
      "Finding 3 - open the job black box",
      "Task-level variation breaks the idea of one AI role\nper job family.",
      6,
      { titleHeight: 108, accent: C.blue },
    );

    await addImageFrame(
      slide,
      "figures/20260812-005613.jpeg",
      { left: 62, top: 184, width: 820, height: 477 },
      "Tableau dashboard showing Core and Supplemental tasks and task-level AI role balance for Architecture and Engineering",
      "task-variation-dashboard",
    );
    addText(
      slide,
      "ARCHITECTURE & ENGINEERING",
      { left: 920, top: 202, width: 285, height: 28 },
      { fontSize: 17, bold: true, color: C.blue },
      "selected-family-label",
    );
    addBullet(
      slide,
      918,
      250,
      290,
      "Mostly copilot",
      "Most displayed tasks sit to the right of the zero line.",
      C.blue,
      "6a",
      94,
    );
    addBullet(
      slide,
      918,
      368,
      290,
      "Not uniform",
      "One Core task falls on the automation side.",
      C.orange,
      "6b",
      94,
    );
    addBullet(
      slide,
      918,
      486,
      290,
      "Different profiles",
      "Core and Supplemental tasks show different exposure and mode mixes.",
      C.coral,
      "6c",
      112,
    );
    addText(
      slide,
      "A family average can hide the task mix.",
      { left: 920, top: 620, width: 290, height: 44 },
      { fontSize: 24, bold: true, color: C.ink },
      "task-variation-takeaway",
    );
    addFooter(slide, 6);
    setNotes(
      slide,
      "Use the selected Architecture and Engineering view as an example. The core point is methodological: task-level marks reveal variation that a single family or occupation average can hide.",
      [
        "figures/20260812-005613.jpeg (team-provided Tableau export)",
        "AI_at_Work_Four_Question_Research_Story.docx (internal task-reconfiguration narrative)",
      ],
    );
  }

  // Slide 7: Occupational context and conclusion.
  {
    const slide = presentation.slides.add();
    addHeader(
      slide,
      "Finding 4 - occupational context",
      "Occupational context shifts the balance,\nbut the evidence is descriptive.",
      7,
      { titleHeight: 108, accent: C.orange },
    );

    await addImageFrame(
      slide,
      "figures/20260812-005637.jpeg",
      { left: 62, top: 184, width: 760, height: 449 },
      "Tableau dashboard showing occupational preparation levels and AI role balance for Green versus non-Green occupations",
      "context-dashboard",
    );
    addText(
      slide,
      "WHAT THE VIEW SUGGESTS",
      { left: 864, top: 200, width: 340, height: 28 },
      { fontSize: 17, bold: true, color: C.orange },
      "context-label",
    );
    addBullet(
      slide,
      862,
      250,
      345,
      "Preparation matters",
      "The strongest augmentation balances appear at the lowest and highest preparation levels.",
      C.gold,
      "7a",
      112,
    );
    addBullet(
      slide,
      862,
      386,
      345,
      "Direction changes",
      "Green versus non-Green differences change direction across levels.",
      C.orange,
      "7b",
      100,
    );
    addBullet(
      slide,
      862,
      510,
      345,
      "Interpret carefully",
      "These are descriptive associations, not causal effects.",
      C.coral,
      "7c",
      88,
    );

    addRect(slide, { left: 0, top: 642, width: W, height: 78 }, C.ink, { name: "conclusion-band" });
    addText(
      slide,
      "AI is redistributing tasks - not uniformly replacing entire occupations.",
      { left: 68, top: 661, width: 1144, height: 38 },
      { fontSize: 29, bold: true, color: C.white, alignment: "center" },
      "conclusion-statement",
    );
    setNotes(
      slide,
      "Frame these results as descriptive patterns. The strongest synthesis is that context matters, but no single occupational label determines whether AI is an executor or copilot.",
      [
        "figures/20260812-005637.jpeg (team-provided Tableau export)",
        "analysis_dataset.csv (Job Zone role-balance verification)",
        "AI_at_Work_Four_Question_Research_Story.docx (internal conclusion language)",
      ],
    );
  }

  // Slide 8: Lessons learned and close.
  {
    const slide = presentation.slides.add();
    addHeader(
      slide,
      "Lessons learned",
      "Clearer metrics made the story\nmore trustworthy.",
      8,
      { titleHeight: 112, dark: true, accent: C.coral },
    );

    const lessons = [
      {
        n: "01",
        y: 210,
        h: "Match measure to grain",
        b: "Use MIN/AVG for repeated occupation/task fields; SUM exposure components.",
        c: C.teal,
      },
      {
        n: "02",
        y: 306,
        h: "Separate exposure from role",
        b: "Ask how much AI appears and what it does as separate questions.",
        c: C.coral,
      },
      {
        n: "03",
        y: 402,
        h: "Choose charts by relationship",
        b: "Use bars to rank, 100% bars for balance, and heatmaps/scatters for association.",
        c: C.orange,
      },
      {
        n: "04",
        y: 498,
        h: "Make confidence visible",
        b: "Show exposure, task count, and coverage; label controls; remove nulls; lock semantic colors.",
        c: C.gold,
      },
    ];
    lessons.forEach((lesson) => {
      addText(
        slide,
        lesson.n,
        { left: 72, top: lesson.y, width: 56, height: 32 },
        { fontSize: 24, bold: true, color: lesson.c },
        `lesson-number-${lesson.n}`,
      );
      addText(
        slide,
        lesson.h,
        { left: 150, top: lesson.y - 2, width: 470, height: 40 },
        { fontSize: 32, bold: true, color: C.white },
        `lesson-heading-${lesson.n}`,
      );
      addText(
        slide,
        lesson.b,
        { left: 650, top: lesson.y - 2, width: 555, height: 66 },
        { fontSize: 22, color: "#D3DBE0" },
        `lesson-body-${lesson.n}`,
      );
      addLine(slide, 150, lesson.y + 68, 1055, "#3D4A54", 1, `lesson-rule-${lesson.n}`);
    });

    addText(
      slide,
      "The better question is not \"Will AI replace jobs?\"",
      { left: 72, top: 608, width: 560, height: 38 },
      { fontSize: 25, color: "#D3DBE0" },
      "closing-question-one",
    );
    addText(
      slide,
      "It is \"How is AI reallocating tasks between humans and machines?\"",
      { left: 650, top: 604, width: 555, height: 76 },
      { fontSize: 32, bold: true, color: C.white },
      "closing-question-two",
    );
    addFooter(slide, 8, true);
    setNotes(
      slide,
      "Close by connecting the analytical lessons to the substantive conclusion. The project became clearer once data grain, aggregation, semantic color, and chart purpose were treated as part of the argument.",
      [
        "figures/Final Presentation-fianl .pdf (internal structural reference for a lessons-learned close)",
        "figures/AI_at_Work_Unified_Dataset_Documentation.docx (aggregation and coverage rules)",
        "AI_at_Work_Four_Question_Research_Story.docx (internal closing narrative)",
      ],
    );
  }

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const png = await presentation.export({ slide, format: "png", scale: 1 });
    await fs.writeFile(path.join(RENDER_DIR, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(LAYOUT_DIR, `${stem}.layout.json`), await layout.text());
  }

  const montage = await presentation.export({ format: "webp", montage: true, scale: 1 });
  await fs.writeFile(path.join(BUILD, "deck-montage.webp"), new Uint8Array(await montage.arrayBuffer()));

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(FINAL_PPTX);
  console.log(FINAL_PPTX);
}

build().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
