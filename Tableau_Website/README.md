# Who Does the Work?

An original Svelte scrollytelling story about how generative AI redistributes workplace tasks
between automation and augmentation. The interaction architecture uses the supplied Yard Sale-style
template, while the reporting, visual identity, illustrations, and data story are original.

## Run locally

```bash
npm install
npm run dev
```

Open <http://localhost:5173>.

## Validate and build

```bash
npm run check
npm run build
npm run preview
```

The production build is written to `dist/`.

## Refresh the explorer data

The browser-ready occupation profiles are generated from the supplied Tableau workbook in the
adjacent `figures` directory:

```bash
npm run data
```

This writes `public/data/occupation-profiles.json`.

## Interaction architecture

- Each scrolly component keeps an `activeStep` selected by `IntersectionObserver`.
- The visual scene uses native `position: sticky` while narrative cards move over it.
- Scene layers stay mounted and switch between discrete state classes.
- CSS transitions interpolate transforms, opacity, color, and width between those states.
- JavaScript handles step detection, quiz state, and explorer data selection—not per-pixel scrolling.
- Reduced-motion preferences remove long transitions while retaining every story state.

## Experimental handoff simulation

The simulation is intentionally isolated behind `showHandoffSimulation` near the top of
`src/App.svelte`. Change that constant to `false` to revert the page to its previous narrative flow
without deleting the component or its work.
