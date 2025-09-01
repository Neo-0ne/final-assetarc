<?php
/*
Template Name: Podcast Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-5xl mx-auto">
  <h1 class="text-4xl font-bold mb-4">🎙️ The AssetArc Podcast</h1>
  <p class="mb-6 text-lg">Listen in as we explore how to protect your assets, reduce tax exposure, and structure your legacy intelligently.</p>

  <section class="grid md:grid-cols-2 gap-8">
    <div class="bg-gray-900 p-6 rounded shadow">
      <h2 class="text-xl font-semibold mb-2">Ep. 1 – Trusts vs Companies</h2>
      <audio controls class="w-full">
        <source src="/media/ep1.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
      </audio>
    </div>

    <div class="bg-gray-900 p-6 rounded shadow">
      <h2 class="text-xl font-semibold mb-2">Ep. 2 – Offshore is Not Illegal</h2>
      <audio controls class="w-full">
        <source src="/media/ep2.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
      </audio>
    </div>
  </section>
</main>

<?php get_footer(); ?>
