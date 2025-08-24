<?php
/*
Template Name: About Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-5xl mx-auto">
  <!-- Jules: Synthesized content for review -->
  <h1 class="text-4xl font-bold mb-8 text-center text-gold">Our Mission: Structure, Protect, Endure</h1>

  <section class="grid md:grid-cols-3 gap-12 items-center">
    <div class="md:col-span-1">
      <img src="<?php echo get_template_directory_uri(); ?>/assets/images/hanno-bekker-headshot.jpg" alt="Hanno Bekker, Founder of AssetArc" class="rounded-lg shadow-lg w-full">
    </div>
    <div class="md:col-span-2">
      <h2 class="text-3xl font-semibold mb-4">A Note From Our Founder</h2>
      <p class="mb-4 text-gray-300">
        "I wrote 'The Definitive Structuring Guide' because I have seen what happens when good people build good businesses—but on the wrong legal foundation. Too many founders, professionals, and investors spend their lives accumulating value without securing it."
      </p>
      <p class="mb-4 text-gray-300">
        "This platform was born from that experience. It is not a motivational tool; it is a structural blueprint brought to life. We built AssetArc to transform the complex, often intimidating, world of asset protection into a logical, accessible, and transparent process."
      </p>
      <p class="text-gray-300">
        "Our promise is simple: to provide the tools and logic you need to do things right from the start. This is where understanding becomes execution, and execution becomes protection."
      </p>
      <p class="mt-4 font-semibold text-gold">- Hanno Bekker</p>
    </div>
  </section>

  <section class="mt-16">
    <h2 class="text-3xl font-semibold mb-6 text-center">Why We Built AssetArc</h2>
    <div class="grid md:grid-cols-2 gap-8 text-center">
      <div class="card p-6">
        <h3 class="text-xl font-bold text-gold mb-2">To Replace Complexity with Clarity</h3>
        <p>Protection is not paperwork. It is logic. It is law. It is layered structure. We translate these principles into automated workflows that guide you through every step, ensuring you understand the 'why' behind every decision.</p>
      </div>
      <div class="card p-6">
        <h3 class="text-xl font-bold text-gold mb-2">To Make Governance Accessible</h3>
        <p>We believe robust, compliant structuring shouldn't be reserved for the ultra-rich. We provide the tools for entrepreneurs, families, and advisors to build resilient governance frameworks that protect assets across generations.</p>
      </div>
    </div>
  </section>
  <!-- End synthesized content -->
</main>

<?php get_footer(); ?>
