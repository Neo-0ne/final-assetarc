<?php
/*
Template Name: Contact Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-4xl mx-auto">
  <!-- Jules: Synthesized content for review -->
  <div class="text-center">
      <h1 class="text-4xl font-bold mb-4">Get in Touch</h1>
      <p class="mb-12 text-gray-400">For questions about our platform, advisor subscriptions, or bespoke structuring projects, please reach out.</p>
  </div>

  <div class="grid md:grid-cols-2 gap-12">
    <div>
      <h2 class="text-2xl font-semibold text-gold mb-4">Contact Details</h2>
      <ul class="space-y-4 text-gray-300">
        <li class="flex items-center">
          <span class="mr-3 w-6 text-center">📍</span>
          <span>Cape Town, South Africa</span>
        </li>
        <li class="flex items-center">
          <span class="mr-3 w-6 text-center">✉️</span>
          <a href="mailto:support@asset-arc.com" class="hover:text-gold">support@asset-arc.com</a>
        </li>
        <li class="flex items-center">
          <span class="mr-3 w-6 text-center">📞</span>
          <span>+27 21 800 1234 (Placeholder)</span>
        </li>
      </ul>
      <p class="mt-6 text-sm text-gray-500">For support inquiries, please use the form. For strategic or partnership discussions, please email us directly.</p>
    </div>
    <div>
      <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" class="space-y-4 card p-8">
        <input type="hidden" name="action" value="assetarc_contact_form">
        <?php wp_nonce_field('contact_form_nonce'); ?>
        <div>
          <label for="name" class="block text-sm mb-1">Full Name</label>
          <input type="text" id="name" name="name" class="w-full p-2 rounded bg-neutral-800 text-white border border-neutral-600 focus:border-gold focus:ring-gold" required>
        </div>

        <div>
          <label for="email" class="block text-sm mb-1">Email Address</label>
          <input type="email" id="email" name="email" class="w-full p-2 rounded bg-neutral-800 text-white border border-neutral-600 focus:border-gold focus:ring-gold" required>
        </div>

        <div>
          <label for="message" class="block text-sm mb-1">Your Message</label>
          <textarea id="message" name="message" rows="5" class="w-full p-2 rounded bg-neutral-800 text-white border border-neutral-600 focus:border-gold focus:ring-gold" required></textarea>
        </div>

        <button type="submit" class="btn btn-gold w-full">Send Message</button>
      </form>
    </div>
  </div>
  <!-- End synthesized content -->
</main>

<?php get_footer(); ?>
