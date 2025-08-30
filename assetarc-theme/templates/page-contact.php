<?php
/*
Template Name: Contact Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-4xl mx-auto">
  <div class="text-center">
      <?php if( get_field('contact_headline') ): ?>
        <h1 class="text-4xl font-bold mb-4"><?php the_field('contact_headline'); ?></h1>
      <?php endif; ?>
      <?php if( get_field('contact_intro') ): ?>
        <p class="mb-12 text-gray-400"><?php the_field('contact_intro'); ?></p>
      <?php endif; ?>
  </div>

  <div class="grid md:grid-cols-2 gap-12">
    <div>
      <?php if( get_field('details_headline') ): ?>
        <h2 class="text-2xl font-semibold text-gold mb-4"><?php the_field('details_headline'); ?></h2>
      <?php endif; ?>
      <ul class="space-y-4 text-gray-300">
        <?php if( get_field('contact_office') ): ?>
          <li class="flex items-center">
            <span class="mr-3 w-6 text-center">📍</span>
            <span><?php the_field('contact_office'); ?></span>
          </li>
        <?php endif; ?>
        <?php if( get_field('contact_email') ): ?>
          <li class="flex items-center">
            <span class="mr-3 w-6 text-center">✉️</span>
            <span>Email: <a href="mailto:<?php the_field('contact_email'); ?>" class="hover:text-gold"><?php the_field('contact_email'); ?></a></span>
          </li>
        <?php endif; ?>
        <?php if( get_field('contact_phone') ): ?>
          <li class="flex items-center">
            <span class="mr-3 w-6 text-center">📞</span>
            <span>Phone: <?php the_field('contact_phone'); ?></span>
          </li>
        <?php endif; ?>
      </ul>
      <div class="mt-8 border-t border-neutral-700 pt-6">
          <?php if( get_field('demo_headline') ): ?>
            <h3 class="text-xl font-semibold text-gold mb-2"><?php the_field('demo_headline'); ?></h3>
          <?php endif; ?>
          <?php if( get_field('demo_content') ): ?>
            <div class="text-sm text-gray-400"><?php the_field('demo_content'); ?></div>
          <?php endif; ?>
          <?php if( get_field('chat_headline') ): ?>
            <h3 class="text-xl font-semibold text-gold mt-4 mb-2"><?php the_field('chat_headline'); ?></h3>
          <?php endif; ?>
          <?php if( get_field('chat_content') ): ?>
            <div class="text-sm text-gray-400"><?php the_field('chat_content'); ?></div>
          <?php endif; ?>
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
