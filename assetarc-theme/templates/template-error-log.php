<?php
/*
Template Name: Error Log Viewer
*/
get_header(); ?>

<div class="min-h-screen bg-black text-white p-10">
  <h1 class="text-3xl font-bold text-yellow-400 mb-6">System Error Logs</h1>
  <div class="bg-gray-900 p-6 rounded-xl shadow-xl overflow-auto text-sm">
    <?php
    $log_file = get_template_directory() . '/logs/error.log';
    if (file_exists($log_file)) {
      $log_contents = file_get_contents($log_file);
      echo "<pre class='whitespace-pre-wrap'>$log_contents</pre>";
    } else {
      echo "<p>No log file found.</p>";
    }
    ?>
  </div>
</div>

<?php get_footer(); ?>
