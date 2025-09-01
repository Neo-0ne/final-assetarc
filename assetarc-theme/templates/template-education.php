<?php
/*
Template Name: Education Hub
*/
get_header(); ?>

<main class="p-8 text-white">
  <h1 class="text-4xl font-bold text-center mb-10">Education Hub</h1>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
    <div class="bg-gray-800 p-6 rounded-lg text-center">
      <h2 class="text-2xl font-semibold text-gold mb-4">Podcast</h2>
      <p class="mb-4">Listen to our latest discussions on asset protection and tax strategies.</p>
      <a href="/podcast" class="text-gold hover:underline">Explore episodes</a>
    </div>

    <div class="bg-gray-800 p-6 rounded-lg text-center">
      <h2 class="text-2xl font-semibold text-gold mb-4">Blog</h2>
      <p class="mb-4">Read our in-depth articles on global finance and legal structuring.</p>
      <a href="/blog" class="text-gold hover:underline">Read the blog</a>
    </div>

    <div class="bg-gray-800 p-6 rounded-lg text-center">
      <h2 class="text-2xl font-semibold text-gold mb-4">Courses</h2>
      <p class="mb-4">Enroll in our guided courses to master asset protection.</p>
      <a href="/course" class="text-gold hover:underline">View curriculum</a>
    </div>
  </div>

  <div class="text-center mt-12">
    <h2 class="text-3xl font-bold mb-4">Ready to Learn More?</h2>
    <p class="text-lg mb-6">Download our free guide to offshore structuring.</p>
    <a href="/lead-magnet" class="inline-block bg-gold text-black font-semibold px-6 py-3 rounded-full hover:bg-yellow-400 transition">Download Free Guide</a>
  </div>
</main>

<?php get_footer(); ?>
