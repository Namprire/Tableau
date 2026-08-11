# AI worker or copilot?

An interactive, static data story built with SvelteKit, TypeScript, D3, sticky scrolling, and preprocessed JSON.

## Run locally

```bash
npm install
npm run data
npm run dev
```

## Validate and build

```bash
npm run check
npm run build
```

The static production site is written to `build/`.

## Data workflow

`scripts/preprocess_data.py` reads `../analysis_dataset.csv` and produces compact JSON files in `src/lib/data/`. Re-run `npm run data` after the source dataset changes.

## Story structure

1. Immediate hook and 77% headline finding
2. Worker/copilot definition as a spectrum
3. Sticky four-scene D3 narrative
4. Searchable occupation and task explorer
5. Conclusion, methods, and limitations
