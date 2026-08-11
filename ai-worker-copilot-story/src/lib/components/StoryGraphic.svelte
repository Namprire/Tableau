<script lang="ts">
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  type Zone = {
    zone: number;
    count: number;
    exposureShare: number;
    medianMultiple: number;
    workerShare: number;
    copilotShare: number;
  };

  type Family = {
    family: string;
    exposureShare: number;
    workerShare: number;
    copilotShare: number;
  };

  type SalaryGroup = {
    quartile?: string;
    zone?: number;
    count: number;
    exposureShare: number;
    workerShare: number;
    copilotShare: number;
  };

  export let scene = 0;
  export let zones: Zone[] = [];
  export let families: Family[] = [];
  export let salary: { quartiles: SalaryGroup[]; q4Zones: SalaryGroup[] } = { quartiles: [], q4Zones: [] };

  let frame: HTMLDivElement;
  let svg: SVGSVGElement;
  let width = 720;
  let height = 620;

  const colors = {
    ink: '#172336',
    muted: '#6d746f',
    line: '#d8d3c9',
    exposure: '#315f7d',
    worker: '#d66a4d',
    copilot: '#247d78',
    gold: '#c59a3d',
    paper: '#f4f0e8'
  };

  onMount(() => {
    const observer = new ResizeObserver(([entry]) => {
      width = entry.contentRect.width;
      height = Math.max(470, Math.min(670, width * 0.83));
      draw();
    });
    observer.observe(frame);
    draw();
    return () => observer.disconnect();
  });

  $: if (svg && zones.length && width && scene >= 0) draw();

  const fmt = d3.format('.0%');

  function base(title: string, note: string) {
    const root = d3.select(svg);
    root.interrupt();
    root.selectAll('*').interrupt();
    root.selectAll('*').remove();
    root.attr('viewBox', `0 0 ${width} ${height}`).attr('role', 'img').attr('aria-label', `${title}. ${note}`);

    root.append('text')
      .attr('class', 'chart-kicker')
      .attr('x', 24)
      .attr('y', 34)
      .text(`0${scene + 1} / 04`);

    root.append('text')
      .attr('class', 'chart-title')
      .attr('x', 24)
      .attr('y', 70)
      .text(title);

    root.append('text')
      .attr('class', 'chart-note')
      .attr('x', 24)
      .attr('y', height - 18)
      .text(note);

    return root.append('g').attr('transform', 'translate(24,104)');
  }

  function draw() {
    if (!svg || !zones.length) return;
    if (scene === 0) drawZones();
    else if (scene === 1) drawFamilies();
    else if (scene === 2) drawSalary();
    else drawQ4();
  }

  function drawZones() {
    const g = base('Most exposure sits in Job Zones 4 and 5', 'Share of summed occupation exposure');
    const sorted = [...zones].sort((a, b) => a.zone - b.zone);
    const margin = { left: width < 560 ? 80 : 118, right: 58, bottom: 64 };
    const innerWidth = width - 48 - margin.left - margin.right;
    const innerHeight = height - 145 - margin.bottom;
    const x = d3.scaleLinear().domain([0, 0.6]).range([0, innerWidth]);
    const y = d3.scaleBand().domain(sorted.map((d) => String(d.zone))).range([0, innerHeight]).padding(0.38);
    const plot = g.append('g').attr('transform', `translate(${margin.left},0)`);

    plot.selectAll('.grid').data([0, .2, .4, .6]).join('line')
      .attr('x1', (d) => x(d)).attr('x2', (d) => x(d)).attr('y1', 0).attr('y2', innerHeight)
      .attr('stroke', colors.line).attr('stroke-width', 1);

    plot.selectAll('.bar').data(sorted).join('rect')
      .attr('x', 0).attr('y', (d) => y(String(d.zone)) ?? 0).attr('height', y.bandwidth())
      .attr('width', 0).attr('fill', (d) => d.zone >= 4 ? colors.exposure : '#bcc9d1')
      .transition().duration(650).ease(d3.easeCubicOut).attr('width', (d) => x(d.exposureShare));

    plot.selectAll('.label').data(sorted).join('text')
      .attr('x', -12).attr('y', (d) => (y(String(d.zone)) ?? 0) + y.bandwidth() / 2 + 5)
      .attr('text-anchor', 'end').attr('class', 'axis-label').text((d) => `Zone ${d.zone}`);

    plot.selectAll('.value').data(sorted).join('text')
      .attr('x', (d) => x(d.exposureShare) + 10).attr('y', (d) => (y(String(d.zone)) ?? 0) + y.bandwidth() / 2 + 5)
      .attr('class', 'value-label').attr('opacity', 0).text((d) => fmt(d.exposureShare))
      .transition().delay(380).duration(300).attr('opacity', 1);

    plot.selectAll('.tick').data([0, .2, .4, .6]).join('text')
      .attr('x', (d) => x(d)).attr('y', innerHeight + 24).attr('text-anchor', 'middle')
      .attr('class', 'tick-label').text((d) => fmt(d));
  }

  function drawFamilies() {
    const selectedNames = [
      'Computer and Mathematical', 'Education, Training, and Library',
      'Arts, Design, Entertainment, Sports, and Media', 'Office and Administrative Support',
      'Life, Physical, and Social Science', 'Business and Financial Operations',
      'Healthcare Practitioners and Technical', 'Production'
    ];
    const label = new Map([
      ['Computer and Mathematical', 'Computing'], ['Education, Training, and Library', 'Education'],
      ['Arts, Design, Entertainment, Sports, and Media', 'Arts & media'], ['Office and Administrative Support', 'Office support'],
      ['Life, Physical, and Social Science', 'Science'], ['Business and Financial Operations', 'Business'],
      ['Healthcare Practitioners and Technical', 'Healthcare'], ['Production', 'Production']
    ]);
    const data = selectedNames.map((name) => families.find((d) => d.family === name)).filter(Boolean) as Family[];
    const g = base('The worker side is concentrated in computing', 'Bar length = share of all exposure · color = interaction role');
    const margin = { left: width < 560 ? 92 : 130, right: 82, bottom: 52 };
    const innerWidth = width - 48 - margin.left - margin.right;
    const innerHeight = height - 145 - margin.bottom;
    const x = d3.scaleLinear().domain([0, 0.44]).range([0, innerWidth]);
    const y = d3.scaleBand().domain(data.map((d) => d.family)).range([0, innerHeight]).padding(0.34);
    const plot = g.append('g').attr('transform', `translate(${margin.left},0)`);

    plot.selectAll('.grid').data([0, .1, .2, .3, .4]).join('line')
      .attr('x1', (d) => x(d)).attr('x2', (d) => x(d)).attr('y1', 0).attr('y2', innerHeight)
      .attr('stroke', colors.line);

    plot.selectAll('.worker').data(data).join('rect')
      .attr('x', 0).attr('y', (d) => y(d.family) ?? 0).attr('height', y.bandwidth())
      .attr('width', 0).attr('fill', colors.worker)
      .transition().duration(650).attr('width', (d) => x(d.exposureShare * d.workerShare));

    plot.selectAll('.copilot').data(data).join('rect')
      .attr('x', (d) => x(d.exposureShare * d.workerShare)).attr('y', (d) => y(d.family) ?? 0)
      .attr('height', y.bandwidth()).attr('width', 0).attr('fill', colors.copilot)
      .transition().duration(650).attr('width', (d) => x(d.exposureShare * d.copilotShare));

    plot.selectAll('.label').data(data).join('text')
      .attr('x', -12).attr('y', (d) => (y(d.family) ?? 0) + y.bandwidth() / 2 + 4)
      .attr('text-anchor', 'end').attr('class', 'axis-label').text((d) => label.get(d.family) ?? d.family);

    plot.selectAll('.value').data(data).join('text')
      .attr('x', (d) => x(d.exposureShare) + 8).attr('y', (d) => (y(d.family) ?? 0) + y.bandwidth() / 2 + 4)
      .attr('class', 'small-value').text((d) => `${fmt(d.exposureShare)} · ${fmt(d.copilotShare)} copilot`);

    addLegend(g, margin.left, innerHeight + 38);
  }

  function drawSalary() {
    const data = salary.quartiles;
    const g = base('High salary does not automatically mean copilot', 'Bar length = share of classified exposure');
    const margin = { left: width < 560 ? 106 : 142, right: 82, bottom: 58 };
    const innerWidth = width - 48 - margin.left - margin.right;
    const innerHeight = height - 145 - margin.bottom;
    const x = d3.scaleLinear().domain([0, 0.52]).range([0, innerWidth]);
    const y = d3.scaleBand().domain(data.map((d) => d.quartile ?? '')).range([0, innerHeight]).padding(0.42);
    const short = new Map([
      ['Q1 Lower', 'Q1 · lower'], ['Q2 Lower-middle', 'Q2 · lower-middle'],
      ['Q3 Upper-middle', 'Q3 · upper-middle'], ['Q4 Higher', 'Q4 · higher']
    ]);
    const plot = g.append('g').attr('transform', `translate(${margin.left},0)`);

    plot.selectAll('.grid').data([0, .1, .2, .3, .4, .5]).join('line')
      .attr('x1', (d) => x(d)).attr('x2', (d) => x(d)).attr('y1', 0).attr('y2', innerHeight).attr('stroke', colors.line);
    plot.selectAll('.worker').data(data).join('rect')
      .attr('x', 0).attr('y', (d) => y(d.quartile ?? '') ?? 0).attr('height', y.bandwidth()).attr('width', 0).attr('fill', colors.worker)
      .transition().duration(650).attr('width', (d) => x(d.exposureShare * d.workerShare));
    plot.selectAll('.copilot').data(data).join('rect')
      .attr('x', (d) => x(d.exposureShare * d.workerShare)).attr('y', (d) => y(d.quartile ?? '') ?? 0)
      .attr('height', y.bandwidth()).attr('width', 0).attr('fill', colors.copilot)
      .transition().duration(650).attr('width', (d) => x(d.exposureShare * d.copilotShare));
    plot.selectAll('.label').data(data).join('text')
      .attr('x', -12).attr('y', (d) => (y(d.quartile ?? '') ?? 0) + y.bandwidth() / 2 + 5)
      .attr('text-anchor', 'end').attr('class', 'axis-label').text((d) => short.get(d.quartile ?? '') ?? d.quartile ?? '');
    plot.selectAll('.value').data(data).join('text')
      .attr('x', (d) => x(d.exposureShare) + 9).attr('y', (d) => (y(d.quartile ?? '') ?? 0) + y.bandwidth() / 2 + 5)
      .attr('class', 'value-label').text((d) => `${fmt(d.exposureShare)} · ${fmt(d.copilotShare)} copilot`);
    addLegend(g, margin.left, innerHeight + 42);
  }

  function drawQ4() {
    const data = salary.q4Zones.filter((d) => (d.exposureShare ?? 0) >= 0.01).sort((a, b) => (b.exposureShare ?? 0) - (a.exposureShare ?? 0));
    const g = base('Inside Q4, Job Zone changes the picture', 'Share of the highest salary quartile’s classified exposure');
    const margin = { left: width < 560 ? 90 : 126, right: 100, bottom: 66 };
    const innerWidth = width - 48 - margin.left - margin.right;
    const innerHeight = height - 145 - margin.bottom;
    const x = d3.scaleLinear().domain([0, 0.85]).range([0, innerWidth]);
    const y = d3.scaleBand().domain(data.map((d) => String(d.zone))).range([0, innerHeight]).padding(0.52);
    const plot = g.append('g').attr('transform', `translate(${margin.left},0)`);

    plot.selectAll('.grid').data([0, .2, .4, .6, .8]).join('line')
      .attr('x1', (d) => x(d)).attr('x2', (d) => x(d)).attr('y1', 0).attr('y2', innerHeight).attr('stroke', colors.line);
    plot.selectAll('.worker').data(data).join('rect')
      .attr('x', 0).attr('y', (d) => y(String(d.zone)) ?? 0).attr('height', y.bandwidth()).attr('width', 0).attr('fill', colors.worker)
      .transition().duration(650).attr('width', (d) => x(d.exposureShare * d.workerShare));
    plot.selectAll('.copilot').data(data).join('rect')
      .attr('x', (d) => x(d.exposureShare * d.workerShare)).attr('y', (d) => y(String(d.zone)) ?? 0)
      .attr('height', y.bandwidth()).attr('width', 0).attr('fill', colors.copilot)
      .transition().duration(650).attr('width', (d) => x(d.exposureShare * d.copilotShare));
    plot.selectAll('.label').data(data).join('text')
      .attr('x', -12).attr('y', (d) => (y(String(d.zone)) ?? 0) + y.bandwidth() / 2 + 5)
      .attr('text-anchor', 'end').attr('class', 'axis-label').text((d) => `Zone ${d.zone}`);
    plot.selectAll('.value').data(data).join('text')
      .attr('x', (d) => x(d.exposureShare) + 10).attr('y', (d) => (y(String(d.zone)) ?? 0) + y.bandwidth() / 2 + 5)
      .attr('class', 'value-label').text((d) => `${fmt(d.exposureShare)} of Q4 · ${fmt(d.copilotShare)} copilot`);
    addLegend(g, margin.left, innerHeight + 44);
  }

  function addLegend(g: d3.Selection<SVGGElement, unknown, null, undefined>, x: number, y: number) {
    const legend = g.append('g').attr('transform', `translate(${x},${y})`);
    const values = [{ label: 'AI as worker', color: colors.worker }, { label: 'AI as copilot', color: colors.copilot }];
    const item = legend.selectAll('g').data(values).join('g').attr('transform', (_, i) => `translate(${i * 140},0)`);
    item.append('rect').attr('width', 18).attr('height', 8).attr('rx', 1).attr('fill', (d) => d.color);
    item.append('text').attr('x', 26).attr('y', 8).attr('class', 'legend-label').text((d) => d.label);
  }
</script>

<div class="frame" bind:this={frame}>
  <svg bind:this={svg}></svg>
</div>

<style>
  .frame { width: 100%; min-height: 30rem; }
  svg { display: block; width: 100%; height: auto; overflow: visible; }
  :global(.chart-kicker) { fill: var(--worker); font-size: 11px; font-weight: 800; letter-spacing: 1.3px; }
  :global(.chart-title) { fill: var(--ink); font-family: var(--display); font-size: clamp(18px, 3vw, 29px); font-weight: 600; letter-spacing: -0.8px; }
  :global(.chart-note) { fill: var(--muted); font-size: 11px; }
  :global(.axis-label) { fill: var(--ink); font-size: 12px; font-weight: 650; }
  :global(.value-label) { fill: var(--ink); font-size: 12px; font-weight: 750; }
  :global(.small-value) { fill: var(--muted-dark); font-size: 10.5px; font-weight: 650; }
  :global(.tick-label), :global(.legend-label) { fill: var(--muted); font-size: 10.5px; }
  @media (max-width: 560px) {
    .frame { min-height: 27rem; }
    :global(.axis-label), :global(.value-label) { font-size: 10px; }
    :global(.small-value) { font-size: 8.5px; }
  }
</style>
