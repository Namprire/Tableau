# Who Does the Work? — Website

This directory contains the Svelte application for the **Who Does the Work?** interactive data
story.

![Animated website tour](docs/media/website-tour.gif)

The complete project documentation—including findings, methodology, screenshots, architecture,
limitations, data regeneration, and the media workflow—is in the
[`repository README`](../README.md).

## Run locally

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

## Validate and build

```bash
npm run check
npm run build
npm run preview
```

The production build is written to `dist/`.

## Refresh the explorer data

```bash
npm run data
```

This rebuilds `public/data/occupation-profiles.json` from the packaged Tableau workbook in the
adjacent `figures/` directory.
