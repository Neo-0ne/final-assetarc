<?php
/*
Template Name: Contact Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-4xl mx-auto">
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
          <span>Office: Cape Town, South Africa</span>
        </li>
        <li class="flex items-center">
          <span class="mr-3 w-6 text-center">✉️</span>
          <span>Email: <a href="mailto:support@asset-arc.com" class="hover:text-gold">support@asset-arc.com</a></span>
        </li>
        <li class="flex items-center">
          <span class="mr-3 w-6 text-center">📞</span>
          <span>Phone: +27 xxx xxx xxxx</span>
        </li>
      </ul>
      <div class="mt-8 border-t border-neutral-700 pt-6">
          <h3 class="text-xl font-semibold text-gold mb-2">Book a Demo</h3>
          <p class="text-sm text-gray-400">Use our booking calendar to schedule a live demo. <!-- Placeholder for booking calendar embed --></p>
          <h3 class="text-xl font-semibold text-gold mt-4 mb-2">Live Chat</h3>
          <p class="text-sm text-gray-400">Chat with our team during business hours. <!-- Placeholder for live chat widget --></p>
      </div>
    </div>
    <div>
      <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" class="space-y-4 card p-8 bg-neutral-900 rounded-lg">
        <input type="hidden" name="action" value="assetarc_contact">
        <?php wp_nonce_field('contact_form_nonce'); ?>
        <div>
          <label for="name" class="block text-sm mb-1">Name</label>
          <input type="text" id="name" name="name" class="w-full p-2 rounded bg-neutral-800 text-white border border-neutral-600 focus:border-gold focus:ring-gold" required>
        </div>

        <div>
          <label for="email" class="block text-sm mb-1">Email</label>
          <input type="email" id="email" name="email" class="w-full p-2 rounded bg-neutral-800 text-white border border-neutral-600 focus:border-gold focus:ring-gold" required>
        </div>

        <div>
          <label for="message" class="block text-sm mb-1">Message</label>
          <textarea id="message" name="message" rows="5" class="w-full p-2 rounded bg-neutral-800 text-white border border-neutral-600 focus:border-gold focus:ring-gold" required></textarea>
        </div>

        <button type="submit" class="btn btn-gold w-full">Send Message</button>
      </form>
    </div>
  </div>
</main>

<?php get_footer(); ?>
