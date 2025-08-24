<?php
/*
Template Name: Services Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-6xl mx-auto">
  <div class="text-center mb-16">
    <h1 class="text-4xl font-bold mb-4">Our Services</h1>
    <p class="text-lg text-gray-400">A suite of powerful tools for structuring, compliance, and asset protection.</p>
  </div>

  <section class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">

    <!-- Service Card 1: Company Setup -->
    <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl text-gold mb-3">Company Setup</h2>
      <p class="text-gray-300">Automated drafting for local (CIPC) and international companies, including BVI, Seychelles, and more.</p>
    </div>

    <!-- Service Card 2: Trust Formation -->
    <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl text-gold mb-3">Trust Formation</h2>
      <p class="text-gray-300">Create asset protection trusts with advisor-reviewed document packs and jurisdictional flexibility.</p>
    </div>

    <!-- Service Card 3: SARS Compliance -->
    <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl text-gold mb-3">SARS s42-47 Compliance</h2>
      <p class="text-gray-300">Assess and generate compliance reports for corporate rollover relief and restructuring.</p>
    </div>

    <!-- Service Card 4: IBC Structuring -->
    <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl text-gold mb-3">IBC Structuring</h2>
      <p class="text-gray-300">Design and deploy International Business Companies with USD-based quotes and a 24-hour FX lock.</p>
    </div>

    <!-- Service Card 5: Global Mobility -->
    <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl text-gold mb-3">Global Mobility & Citizenship</h2>
      <p class="text-gray-300">Explore pathways to residency and citizenship in jurisdictions like St. Kitts & Nevis and Mauritius.</p>
    </div>

    <!-- Service Card 6: Advisor & White-Label -->
    <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl text-gold mb-3">Advisor & White-Label Solutions</h2>
      <p class="text-gray-300">Offer our platform under your own brand with our tokenized access and subscription models.</p>
    </div>

  </section>

  <div class="mt-20 text-center">
    <h2 class="text-3xl font-semibold mb-4">Ready to Begin?</h2>
    <p class="text-gray-400 mb-8">Our assessment tool will guide you to the right solution.</p>
    <a href="/assessment" class="btn btn-gold text-lg">Start Free Assessment</a>
  </div>
</main>

<?php get_footer(); ?>
