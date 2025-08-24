<?php
/*
Template Name: Upload Review Document
*/
get_header(); ?>

<div class="min-h-screen bg-black text-white p-8 flex flex-col items-center">
  <h1 class="text-3xl font-bold text-yellow-400 mb-6">Upload Document for Review</h1>
  <form class="w-full max-w-lg bg-gray-900 p-6 rounded-xl shadow-xl" method="post" enctype="multipart/form-data">
    <?php wp_nonce_field('upload_review_nonce'); ?>
    <label class="block mb-4">
      <span class="text-sm">Choose File (PDF/DOCX only, max 5MB)</span>
      <input type="file" name="review_file" accept=".pdf,.docx" class="w-full mt-1 text-white" required />
    </label>
    <button type="submit" class="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold py-2 px-4 rounded w-full">Upload</button>
  </form>
</div>

<?php get_footer(); ?>
