import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const p = await PresentationFile.importPptx(await FileBlob.load("template-starter.pptx"));
for (const slideIndex of [0, 2, 5]) {
  const s0 = p.slides.getItem(slideIndex);
  console.log("slide", slideIndex + 1, "summary", JSON.stringify(s0.placeholders.summary()));
  console.log("shapes", s0.shapes.count, s0.shapes.items?.map(o => ({name:o.name, type:o.placeholderType, text:String(o.text ?? "").slice(0,30), replace:typeof o.replace, del:typeof o.delete, ctor:o.constructor?.name})));
}
const s = p.slides.getItem(2);
for (const key of ["title", "body", "picture"]) {
  try {
    const o = s.placeholders.getItem(key);
    console.log("ph", key, o?.constructor?.name, {
      replace: typeof o?.replace,
      delete: typeof o?.delete,
      placeholderType: o?.placeholderType,
      frame: o?.frame,
    });
  } catch (e) {
    console.log("pherr", key, String(e));
  }
}
