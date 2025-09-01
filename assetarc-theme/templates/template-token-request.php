<?php
/*
Template Name: Token Request
*/
get_header(); ?>

<div class="min-h-screen bg-black text-white flex flex-col items-center justify-center p-8">
  <h1 class="text-4xl font-bold text-yellow-400 mb-6">Request Access Token</h1>

  <form class="w-full max-w-lg bg-gray-900 p-6 rounded-xl shadow-xl" method="post">
    <?php wp_nonce_field('token_request_nonce'); ?>
    <label class="block mb-4">
      <span class="text-sm">Full Name</span>
      <input type="text" name="name" required class="w-full mt-1 p-2 rounded bg-black border border-gray-700 text-white" />
    </label>
    <label class="block mb-4">
      <span class="text-sm">Email Address</span>
      <input type="email" name="email" required class="w-full mt-1 p-2 rounded bg-black border border-gray-700 text-white" />
    </label>
    <label class="block mb-4">
      <span class="text-sm">Reason for Access</span>
      <textarea name="reason" rows="4" class="w-full mt-1 p-2 rounded bg-black border border-gray-700 text-white" required></textarea>
    </label>
    <button type="submit" class="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold py-2 px-4 rounded w-full">Submit Request</button>
  </form>
</div>

<?php get_footer(); ?>
