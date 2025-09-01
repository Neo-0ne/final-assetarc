<?php
/*
Template Name: Course Page
*/

get_header();

// Include the course logic
require_once get_template_directory() . '/inc/course-handler.php';

// Define the course ID
$course_id = 1;

// Get user and course data
$user_token = get_current_user_token();
$is_enrolled = is_user_enrolled_in_course($user_token, $course_id);
$course_data = get_course_data($course_id);
$user_progress = $is_enrolled ? get_user_progress_data($user_token, $course_id) : [];

?>

<main class="p-8 text-white max-w-5xl mx-auto">
    <h1 class="text-4xl font-bold mb-2 text-gold">AssetArc Structuring Master Course</h1>
    <p class="mb-8 text-lg text-gray-300">A comprehensive course on asset protection, strategic structuring, and legacy planning.</p>

    <?php if ($is_enrolled) : ?>
        <!-- Enrolled User View: Course Curriculum -->
        <div class="bg-gray-900 p-6 rounded-lg shadow-lg">
            <h2 class="text-2xl font-bold mb-4">Your Curriculum</h2>
            <?php if ($course_data && !empty($course_data['modules'])) : ?>
                <div class="space-y-6">
                    <?php foreach ($course_data['modules'] as $module) : ?>
                        <div>
                            <h3 class="text-xl font-semibold text-gold mb-3"><?php echo esc_html($module['title']); ?></h3>
                            <ul class="space-y-2">
                                <?php foreach ($module['lessons'] as $lesson) : ?>
                                    <?php
                                        $is_completed = in_array($lesson['id'], $user_progress);
                                        $lesson_url = home_url('/lesson/' . $lesson['id']); // Assumes a permalink structure for lessons
                                    ?>
                                    <li class="flex items-center">
                                        <?php if ($is_completed) : ?>
                                            <span class="text-green-500 mr-2">&#10004;</span> <!-- Checkmark -->
                                        <?php else : ?>
                                            <span class="text-gray-500 mr-2">&#9675;</span> <!-- Circle -->
                                        <?php endif; ?>
                                        <a href="<?php echo esc_url($lesson_url); ?>" class="hover:text-gold transition-colors duration-300">
                                            <?php echo esc_html($lesson['title']); ?>
                                        </a>
                                    </li>
                                <?php endforeach; ?>
                            </ul>
                        </div>
                    <?php endforeach; ?>
                </div>
            <?php else : ?>
                <p>The course curriculum is currently being updated. Please check back soon.</p>
            <?php endif; ?>
        </div>
        <div class="mt-8 p-4 bg-gray-800 rounded-lg">
            <h3 class="text-lg font-semibold text-gold mb-2">Want an offline copy?</h3>
            <p class="text-gray-300">For a downloadable version of the course material and even more in-depth content, purchase the official book on Amazon.</p>
            <a href="#" class="inline-block mt-3 bg-gold text-black px-6 py-2 rounded text-md hover:bg-yellow-400 font-semibold">View on Amazon</a>
        </div>


    <?php else : ?>
        <!-- Not Enrolled User View -->
        <div class="bg-gray-900 p-8 rounded-lg shadow-lg text-center">
            <h2 class="text-2xl font-bold mb-4">Get Full Access</h2>
            <p class="mb-6 text-lg">Enroll in the AssetArc Structuring Master Course to unlock all modules, interactive quizzes, and expert strategies.</p>
            <a href="#" class="bg-gold text-black px-8 py-3 rounded text-lg hover:bg-yellow-400 font-semibold">Enroll Now for $299</a>
            <p class="text-sm text-gray-500 mt-4">One-time payment. Lifetime access.</p>
        </div>

        <div class="mt-8 p-6 bg-gray-800 rounded-lg">
            <h3 class="text-xl font-semibold mb-3">What You'll Learn</h3>
            <ul class="list-disc list-inside space-y-2">
                <li>How to shield your personal assets from business risks.</li>
                <li>The right way to structure your companies and trusts for growth.</li>
                <li>How to legally optimize your tax situation.</li>
                <li>Advanced strategies for estate planning and legacy protection.</li>
                <li>How to build a compliant, audit-proof global structure.</li>
            </ul>
        </div>
    <?php endif; ?>

</main>

<?php get_footer(); ?>
