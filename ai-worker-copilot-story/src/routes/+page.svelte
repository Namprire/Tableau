<script lang="ts">
  import '../app.css';
  import Hero from '$lib/components/Hero.svelte';
  import Definition from '$lib/components/Definition.svelte';
  import Scrolly from '$lib/components/Scrolly.svelte';
  import OccupationExplorer from '$lib/components/OccupationExplorer.svelte';
  import Methods from '$lib/components/Methods.svelte';
  import meta from '$lib/data/meta.json';
  import zones from '$lib/data/job-zones.json';
  import families from '$lib/data/job-families.json';
  import salary from '$lib/data/salary-context.json';
  import occupations from '$lib/data/occupations.json';
</script>

<svelte:head>
  <title>Who is working—AI or me?</title>
  <meta name="description" content="An interactive data story about when AI acts as a worker and when it acts as a copilot across occupations." />
</svelte:head>

<main>
  <Hero zonesShare={meta.zones45ExposureShare} taskRows={meta.taskRows} occupations={meta.occupations} />
  <Definition />
  <Scrolly {zones} {families} {salary} />
  <OccupationExplorer {occupations} />
  <Methods taskRows={meta.taskRows} occupations={meta.occupations} classifiedOccupations={meta.classifiedOccupations} />
</main>
