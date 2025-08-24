<aside class="sidebar">
  <div class="widget">
    <h3 class="widget-title">Search</h3>
    <?php get_search_form(); ?>
  </div>

  <div class="widget">
    <h3 class="widget-title">Categories</h3>
    <ul>
      <?php wp_list_categories(['title_li' => '']); ?>
    </ul>
  </div>
</aside>
