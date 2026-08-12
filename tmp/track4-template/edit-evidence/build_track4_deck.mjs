import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const WORKSPACE = path.resolve(".");
const ROOT = path.resolve(WORKSPACE, "../..");
const STARTER = path.join(WORKSPACE, "template-starter.pptx");
const OUTPUT = path.join(ROOT, "output", "Who_Does_the_Work_Tableau_Final_Project_track4.pptx");

const presentation = await PresentationFile.importPptx(await FileBlob.load(STARTER));

const getShape = (slideIndex, sourceShapeId) => {
  const marker = `;${sourceShapeId};`;
  const shape = presentation.slides.getItem(slideIndex).shapes.items.find((item) => item.name?.includes(marker));
  if (!shape) throw new Error(`Missing source shape ${sourceShapeId} on slide ${slideIndex + 1}`);
  return shape;
};

const setText = (slideIndex, sourceShapeId, value) => {
  const shape = getShape(slideIndex, sourceShapeId);
  shape.text = value;
};

const setFontSize = (slideIndex, sourceShapeId, fontSize) => {
  getShape(slideIndex, sourceShapeId).text.style = { fontSize };
};

const notesBySlide = [
  `[Sources]\n- Project framing: AI_at_Work_Four_Question_Research_Story.docx`,
  `[Sources]\n- Project framing: AI_at_Work_Four_Question_Research_Story.docx\n- Assignment clarification supplied by the course instructor in the user prompt`,
  `[Sources]\n- figures/AI_at_Work_Unified_Dataset_Documentation.docx\n- analysis_dataset.csv\n- figures/20260812-005545.jpeg`,
  `[Sources]\n- analysis_dataset.csv\n- figures/20260812-013036.jpeg`,
  `[Sources]\n- analysis_dataset.csv\n- figures/20260812-005601.jpeg`,
  `[Sources]\n- analysis_dataset.csv\n- figures/20260812-005613.jpeg\n- figures/20260812-005545.jpeg`,
  `[Sources]\n- analysis_dataset.csv\n- figures/20260812-005637.jpeg`,
  `[Sources]\n- Project lessons synthesized from AI_at_Work_Four_Question_Research_Story.docx\n- figures/Final Presentation-fianl .pdf (structural reference for a concise lessons-learned close)`,
];

async function addImageToSlide(slideIndex, sourceShapeId, relativeImagePath, alt, fit = "contain") {
  const placeholder = getShape(slideIndex, sourceShapeId);
  const frame = { ...placeholder.frame };
  placeholder.text = `Figure ${slideIndex + 1}: ${alt}`;
  placeholder.text.style = { fontSize: 1, color: "#071F4A" };
  const blob = new Uint8Array(await fs.readFile(path.join(ROOT, relativeImagePath)));
  presentation.slides.getItem(slideIndex).images.add({
    blob,
    contentType: "image/jpeg",
    alt,
    fit,
    position: frame,
    geometry: "rect",
  });
}

// Slide 1 — title
setText(
  0,
  450,
  "Who Does the Work?",
);
setFontSize(0, 450, 32);
getShape(0, 451).text = "Tableau final project";
getShape(0, 451).text.style = { fontSize: 1, color: "#071F4A" };
getShape(0, 453).delete();

// Slide 2 — problem framing
setText(1, 514, "Exposure does not reveal AI's role.");
setFontSize(1, 514, 34);
setText(
  1,
  515,
  "EXPOSURE\nHow much AI is used\n\nROLE\nWhat AI does when it is used\n\n01  WHERE — Locate AI\n02  ROLE — Executor or copilot?\n03  TASKS — Open the job black box\n04  CONTEXT — Preparation and occupation",
);

// Slide 3 — method
setText(2, 530, "One dataset connects exposure to role.");
setFontSize(2, 530, 28);
setText(
  2,
  529,
  "3,963 occupation-task pairs\n731 occupations • 5 interaction modes\n\nAutomation = directive + feedback loop\nAugmentation = iteration + validation + learning\n\nRole balance = augmentation − automation",
);
await addImageToSlide(
  2,
  531,
  "figures/20260812-005545.jpeg",
  "Tableau dashboard showing task-level role balance and interaction modes",
);

// Slide 4 — concentration
setText(3, 542, "Observed AI use is concentrated.\n~39% comes from one family.");
setFontSize(3, 542, 18);
getShape(3, 544).text = "Computer & Mathematical occupations are the leading observed source.";
getShape(3, 544).text.style = { fontSize: 1, color: "#071F4A" };
await addImageToSlide(
  3,
  543,
  "figures/20260812-013036.jpeg",
  "Tableau dashboard showing concentration of observed AI exposure",
);

// Slide 5 — overall balance
setText(4, 555, "57%");
setText(4, 556, "augmentation / copilot\n43% automation / executor");
await addImageToSlide(
  4,
  554,
  "figures/20260812-005601.jpeg",
  "Tableau dashboard showing the overall augmentation and automation balance",
);

// Slide 6 — task variation
setText(5, 561, "AI's role changes by task.");
setFontSize(5, 561, 30);
setText(
  5,
  562,
  "Architecture & Engineering is mostly copilot-oriented, but one Core task sits on the automation side. A family average can hide the task mix.",
);
await addImageToSlide(
  5,
  563,
  "figures/20260812-005545.jpeg",
  "Tableau task-role detail view",
);
await addImageToSlide(
  5,
  564,
  "figures/20260812-005613.jpeg",
  "Tableau dashboard showing task variation in Architecture and Engineering",
);

// Slide 7 — occupational context
setText(6, 530, "Context shifts the balance.");
setFontSize(6, 530, 29);
setText(
  6,
  529,
  "Preparation matters: the strongest augmentation balances appear at the lowest and highest preparation levels.\n\nGreen versus non-Green differences change direction across levels.\n\nThese are descriptive associations, not causal effects.\n\nAI is redistributing tasks—not uniformly replacing occupations.",
);
await addImageToSlide(
  6,
  531,
  "figures/20260812-005637.jpeg",
  "Tableau heatmap comparing job preparation level and green occupation status",
);

// Slide 8 — lessons learned
setText(7, 592, "Clearer metrics made the story more trustworthy.");

setText(7, 599, "01  Match measure to grain");
setText(7, 594, "Use MIN/AVG for repeated occupation or task fields; SUM exposure components.");
setText(7, 600, "02  Separate exposure from role");
setText(7, 595, "Ask how much AI appears and what it does as separate questions.");
setText(7, 601, "03  Choose charts by relationship");
setText(7, 597, "Bars rank; 100% bars compare balance; heatmaps and scatters show association.");

setText(7, 602, "04  Make confidence visible");
setText(7, 593, "Show exposure, valid task count, and coverage; label controls and remove nulls.");
setText(7, 603, "Better question");
setText(7, 596, "How is AI reallocating tasks between humans and machines?");
setText(7, 604, "Central takeaway");
setText(7, 598, "AI reshapes tasks inside jobs more than it replaces whole occupations.");

for (let i = 0; i < notesBySlide.length; i += 1) {
  presentation.slides.getItem(i).speakerNotes.textFrame.setText(notesBySlide[i]);
}

await fs.mkdir(path.dirname(OUTPUT), { recursive: true });
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(OUTPUT);
console.log(OUTPUT);
