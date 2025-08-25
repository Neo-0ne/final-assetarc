<?php
/*
Template Name: Lesson Page
Template Post Type: page
*/

get_header();

require_once get_template_directory() . '/inc/course-handler.php';

$lesson_id = get_query_var('lesson_id');
$user_token = get_current_user_token();
$lesson_data = null;

if ($lesson_id && $user_token) {
    $lesson_data = get_lesson_data($user_token, $lesson_id);
}

// For converting markdown to HTML
require_once get_template_directory() . '/inc/parsedown.php';
$parsedown = new Parsedown();

?>

<main class="p-8 text-white max-w-5xl mx-auto">
    <?php if ($lesson_data) : ?>
        <div class="bg-gray-900 p-8 rounded-lg shadow-lg">
            <h1 class="text-3xl font-bold mb-4 text-gold" id="lesson-title"><?php echo esc_html($lesson_data['title']); ?></h1>

            <div id="lesson-content" class="prose prose-invert max-w-none text-gray-300">
                <?php echo $parsedown->text($lesson_data['content']); ?>
            </div>

            <?php if (!empty($lesson_data['quiz'])) : ?>
                <hr class="my-8 border-gray-700" />
                <div id="quiz-container">
                    <h2 class="text-2xl font-semibold mb-4">Quiz</h2>
                    <div id="quiz-content">
                        <p class="mb-4"><?php echo esc_html($lesson_data['quiz']['question']); ?></p>
                        <form id="quiz-form" class="space-y-3">
                            <?php foreach ($lesson_data['quiz']['options'] as $index => $option) : ?>
                                <label class="block bg-gray-800 p-3 rounded hover:bg-gray-700 cursor-pointer">
                                    <input type="radio" name="quiz_option" value="<?php echo $index; ?>" data-correct="<?php echo $option['is_correct'] ? 'true' : 'false'; ?>" class="mr-2">
                                    <?php echo esc_html($option['text']); ?>
                                </label>
                            <?php endforeach; ?>
                        </form>
                        <p id="quiz-feedback" class="mt-4 font-semibold"></p>
                    </div>
                </div>
            <?php endif; ?>

            <div id="lesson-navigation" class="flex justify-between items-center mt-8 pt-6 border-t border-gray-700">
                <a href="#" id="prev-lesson" class="bg-gray-700 text-white px-6 py-2 rounded hover:bg-gray-600 <?php echo $lesson_data['prev_lesson_id'] ? '' : 'invisible'; ?>">&larr; Previous</a>
                <button id="complete-button" data-lesson-id="<?php echo esc_attr($lesson_id); ?>" class="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-500">Mark as Complete</button>
                <a href="#" id="next-lesson" class="bg-gold text-black px-6 py-2 rounded hover:bg-yellow-400 <?php echo $lesson_data['next_lesson_id'] ? '' : 'invisible'; ?>">Next &rarr;</a>
            </div>
            <div class="text-center mt-4"><a href="<?php echo home_url('/course'); ?>" class="text-sm text-gold hover:underline">Back to Curriculum</a></div>
        </div>
    <?php else : ?>
        <div class="bg-gray-900 p-8 rounded-lg shadow-lg text-center">
            <h2 class="text-2xl font-bold text-red-500 mb-4">Access Denied</h2>
            <p class="text-lg">You are either not logged in, not enrolled in this course, or the lesson does not exist.</p>
            <a href="<?php echo home_url('/course'); ?>" class="inline-block mt-6 bg-gold text-black px-6 py-2 rounded hover:bg-yellow-400">Return to Course Page</a>
        </div>
    <?php endif; ?>
</main>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const completeButton = document.getElementById('complete-button');
    if (completeButton) {
        completeButton.addEventListener('click', function() {
            const lessonId = this.dataset.lessonId;

            fetch(`/lifecycle/lesson/${lessonId}/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // The auth cookie is sent automatically by the browser
                },
            }).then(response => {
                if (response.ok) {
                    this.textContent = 'Completed!';
                    this.classList.remove('bg-green-600', 'hover:bg-green-500');
                    this.classList.add('bg-gray-600');
                    this.disabled = true;
                } else {
                    alert('Could not mark lesson as complete. Please try again.');
                }
            });
        });
    }

    const quizForm = document.getElementById('quiz-form');
    if (quizForm) {
        quizForm.addEventListener('change', function(e) {
            if (e.target.type === 'radio') {
                const isCorrect = e.target.dataset.correct === 'true';
                const feedbackEl = document.getElementById('quiz-feedback');
                if (isCorrect) {
                    feedbackEl.textContent = 'Correct!';
                    feedbackEl.className = 'mt-4 font-semibold text-green-500';
                } else {
                    feedbackEl.textContent = 'Not quite, try again!';
                    feedbackEl.className = 'mt-4 font-semibold text-red-500';
                }
            }
        });
    }
});
</script>

<?php get_footer(); ?>
