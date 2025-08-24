<?php
/*
Template Name: Contact Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-xl mx-auto">
  <h1 class="text-4xl font-bold mb-4">Contact Us</h1>
  <p class="mb-6">Have a question about structuring, subscriptions, or token access? Drop us a message below.</p>

  <form method="post" action="" class="space-y-4">
    <?php wp_nonce_field('contact_form_nonce'); ?>
    <div>
      <label for="name" class="block text-sm">Name</label>
      <input type="text" id="name" name="name" class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600" required>
    </div>

    <div>
      <label for="email" class="block text-sm">Email</label>
      <input type="email" id="email" name="email" class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600" required>
    </div>

    <div>
      <label for="message" class="block text-sm">Message</label>
      <textarea id="message" name="message" rows="4" class="w-full p-2 rounded bg-gray-800 text-white border border-gray-600" required></textarea>
    </div>

    <button type="submit" class="bg-gold text-black px-6 py-2 rounded hover:bg-yellow-400">Send Message</button>
  </form>
</main>

<?php get_footer(); ?>
