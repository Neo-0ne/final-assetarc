</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-columns">
      <div class="footer-left">
        <p>&copy; <?php echo date("Y"); ?> <?php bloginfo('name'); ?>. All rights reserved.</p>
      </div>
      <div class="footer-right">
        <nav class="footer-nav">
          <?php
            wp_nav_menu(array(
              'theme_location' => 'footer',
              'menu_class'     => 'footer-menu',
              'container'      => false
            ));
          ?>
        </nav>
      </div>
    </div>
  </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
