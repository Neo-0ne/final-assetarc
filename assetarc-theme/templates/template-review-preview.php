<?php
/*
Template Name: Review Preview
*/
get_header(); ?>

<div class="min-h-screen bg-black text-white p-8">
  <h1 class="text-3xl font-bold text-yellow-400 mb-6">Review Preview</h1>
  <div class="bg-gray-900 p-6 rounded-xl shadow-xl">
    <?php
    $review_files = glob(wp_upload_dir()['basedir'] . '/review-uploads/*');
    if ($review_files) {
      echo '<ul>';
      foreach ($review_files as $file) {
        $file_url = str_replace(wp_upload_dir()['basedir'], wp_upload_dir()['baseurl'], $file);
        echo '<li>';
        echo '<a href="' . esc_url($file_url) . '" target="_blank" class="underline text-yellow-400">';
        echo 'Download ' . basename($file);
        echo '</a>';
        echo '</li>';
      }
      echo '</ul>';
    } else {
      echo '<p>No files to review.</p>';
    }
    ?>
  </div>
</div>

<?php get_footer(); ?>
