<?php
/*
Template Name: Education Hub
*/
get_header(); ?>

<main class="p-8 text-white max-w-6xl mx-auto">
    <div class="text-center mb-16">
        <h1 class="text-4xl font-bold mb-4">Education Hub</h1>
        <p class="text-lg text-gray-400">Deep-dive guides, video tutorials, and podcast episodes on strategic structuring.</p>
    </div>

    <section class="grid md:grid-cols-3 gap-8">
        <!-- Podcast Section -->
        <div class="education-card bg-gray-800 p-8 rounded-lg text-center">
            <h2 class="text-2xl font-semibold text-gold mb-4">Podcast</h2>
            <p class="text-gray-300 mb-6">Listen to our weekly podcast, "Unseen Shields", for expert insights and case studies.</p>
            <a href="/education/podcast" class="btn btn-outline">Listen Now</a>
        </div>

        <!-- Videos Section -->
        <div class="education-card bg-gray-800 p-8 rounded-lg text-center">
            <h2 class="text-2xl font-semibold text-gold mb-4">Videos</h2>
            <p class="text-gray-300 mb-6">Watch tutorials and explainers on complex topics like s42-47 and IBC structuring.</p>
            <a href="/education/videos" class="btn btn-outline">Watch Now</a>
        </div>

        <!-- Blog Section -->
        <div class="education-card bg-gray-800 p-8 rounded-lg text-center">
            <h2 class="text-2xl font-semibold text-gold mb-4">Blog & Articles</h2>
            <p class="text-gray-300 mb-6">Read in-depth articles on compliance, tax strategy, and asset protection.</p>
            <a href="/education/blog" class="btn btn-outline">Read Now</a>
        </div>
    </section>
</main>

<?php get_footer(); ?>
