<?php
/**
 * The template for displaying all single posts
 * @package AssetArc
 */

get_header(); ?>

<main class="single-post-wrapper">
  <?php
  while ( have_posts() ) :
    the_post();
    ?>
    <article class="single-post">
      <header class="post-header">
        <h1 class="post-title"><?php the_title(); ?></h1>
        <div class="post-meta">
          <span>Published on <?php echo get_the_date(); ?></span>
          <span> | By <?php the_author(); ?></span>
        </div>
      </header>

      <div class="post-content">
        <?php the_content(); ?>
      </div>

      <footer class="post-footer">
        <p class="return-link"><a href="<?php echo home_url('/blog'); ?>">&larr; Back to Blog</a></p>
      </footer>
    </article>
  <?php endwhile; ?>
</main>

<style>
.single-post-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  color: #fff;
  background-color: #111;
}

.post-header {
  margin-bottom: 2rem;
}

.post-title {
  font-size: 2.2rem;
  color: #FFD700;
}

.post-meta {
  font-size: 0.9rem;
  color: #888;
}

.post-content {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #eee;
}

.post-footer {
  margin-top: 3rem;
}

.return-link a {
  color: #FFD700;
  text-decoration: none;
}
</style>

<?php get_footer(); ?>
