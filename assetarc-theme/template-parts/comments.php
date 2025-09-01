<?php
// comments.php - Comments area
if (post_password_required()) return;
?>

<div id="comments" class="comments-area mt-12">
    <?php if (have_comments()) : ?>
        <h2 class="text-xl font-bold mb-4">
            <?php comments_number(); ?>
        </h2>
        <ol class="comment-list space-y-6">
            <?php wp_list_comments(array('style' => 'ol')); ?>
        </ol>
    <?php endif; ?>

    <?php comment_form(array(
        'class_submit' => 'bg-gold text-black px-6 py-2 rounded hover:opacity-90',
        'comment_field' => '<textarea id="comment" name="comment" class="w-full p-3 rounded mb-4" rows="5" required></textarea>',
    )); ?>
</div>
