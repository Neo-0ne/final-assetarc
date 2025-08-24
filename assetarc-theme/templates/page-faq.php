<?php
/*
Template Name: FAQ Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-5xl mx-auto">
  <h1 class="text-4xl font-bold mb-4">Frequently Asked Questions</h1>

  <div class="space-y-6">
    <details class="bg-gray-800 p-4 rounded">
      <summary class="font-semibold text-gold cursor-pointer">How do I access the vault?</summary>
      <p class="mt-2">Use the token provided by your advisor to access your secure vault. Tokens are one-time use unless otherwise configured.</p>
    </details>

    <details class="bg-gray-800 p-4 rounded">
      <summary class="font-semibold text-gold cursor-pointer">Can I generate documents before paying?</summary>
      <p class="mt-2">No. Document generation is only enabled after payment or verified advisor access.</p>
    </details>

    <details class="bg-gray-800 p-4 rounded">
      <summary class="font-semibold text-gold cursor-pointer">Is this platform secure?</summary>
      <p class="mt-2">Yes. All documents are generated behind a secure API, reviewed by a human advisor, and watermarked before release.</p>
    </details>
  </div>

  <div class="mt-10 text-center">
    <h2 class="text-xl mb-2">Need further assistance?</h2>
    <button onclick="window.open('/faq-nlp-bot')" class="bg-gold text-black px-4 py-2 rounded hover:bg-yellow-400">Ask the AI Help Bot</button>
  </div>
</main>

<?php get_footer(); ?>
