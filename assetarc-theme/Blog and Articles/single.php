<?php
get_header();
?>

<main class="single-post">
  <div class="container">
    <?php
    if (have_posts()) :
      while (have_posts()) : the_post();
    ?>
        <article class="post">
          <h1 class="post-title"><?php the_title(); ?></h1>
          <div class="post-meta">
            <span class="author">By <?php the_author(); ?></span> |
            <span class="date"><?php the_date(); ?></span>
          </div>
          <div class="post-content">
            <?php the_content(); ?>
          </div>
        </article>
    <?php
      endwhile;
    else :
      echo '<p>No posts found.</p>';
    endif;
    ?>
  </div>
</main>

<?php
get_footer();
?>
