<?php
/* Template Name: Metrics Dashboard */

get_header();
?>

<main class="metrics-dashboard">
  <section class="container mx-auto px-6 py-10 text-white">
    <h1 class="text-3xl font-bold mb-6">📊 Metrics Dashboard</h1>
    <div id="metrics-content" class="grid gap-6 md:grid-cols-2">
      <div class="p-4 bg-gray-900 rounded-xl shadow-lg">
        <h2 class="text-xl font-semibold mb-2">Email Open Rate</h2>
        <p id="open-rate">Loading...</p>
      </div>
      <div class="p-4 bg-gray-900 rounded-xl shadow-lg">
        <h2 class="text-xl font-semibold mb-2">Click Through Rate</h2>
        <p id="click-rate">Loading...</p>
      </div>
      <div class="p-4 bg-gray-900 rounded-xl shadow-lg">
        <h2 class="text-xl font-semibold mb-2">Conversion Rate</h2>
        <p id="conversion-rate">Loading...</p>
      </div>
      <div class="p-4 bg-gray-900 rounded-xl shadow-lg">
        <h2 class="text-xl font-semibold mb-2">Lifetime Value</h2>
        <p id="lifetime-value">Loading...</p>
      </div>
    </div>
  </section>
</main>

<?php get_footer(); ?>
