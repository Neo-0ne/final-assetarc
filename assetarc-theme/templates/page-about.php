<?php
/*
Template Name: About Page
*/
get_header(); ?>

<main class="p-8 text-white max-w-5xl mx-auto">
    <h1 class="text-4xl font-bold mb-8 text-center text-gold">About AssetArc</h1>

    <section class="text-center max-w-3xl mx-auto">
        <h2 class="text-2xl font-semibold mb-4">Our Story</h2>
        <p class="text-gray-300 mb-8">
            AssetArc was built to give founders and advisors a single platform to manage structuring with compliance-first automation.
        </p>
        <h2 class="text-2xl font-semibold mb-4">Our Mission</h2>
        <p class="text-gray-300">
            To protect legacies, minimise tax exposure, and ensure compliance.
        </p>
    </section>

    <section class="mt-16">
        <h2 class="text-3xl font-semibold mb-6 text-center">Our Team</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Team Member 1 -->
            <div class="team-card text-center">
                <img src="<?php echo get_template_directory_uri(); ?>/assets/images/hanno-bekker-headshot.jpg" alt="Hanno Bekker" class="rounded-full w-32 h-32 mx-auto mb-4 border-2 border-gold">
                <h4 class="text-xl font-semibold">Hanno Bekker</h4>
                <p class="text-gold">Founder</p>
                <p class="text-sm text-gray-400 mt-2">Leading the mission to make asset protection accessible and transparent.</p>
            </div>
            <!-- Team Member 2 -->
            <div class="team-card text-center">
                <img src="/wp-content/uploads/Photos/Adam%20Coffey.jfif" alt="Adam Coffey" class="rounded-full w-32 h-32 mx-auto mb-4 border-2 border-gold">
                <h4 class="text-xl font-semibold">Adam Coffey</h4>
                <p class="text-gold">Advisor</p>
                <p class="text-sm text-gray-400 mt-2">Expert in corporate strategy and scaling ventures.</p>
            </div>
            <!-- Team Member 3 -->
            <div class="team-card text-center">
                <!-- Placeholder for large image -->
                <div class="rounded-full w-32 h-32 mx-auto mb-4 border-2 border-gold bg-neutral-700 flex items-center justify-center">
                    <span class="text-xs text-gray-400">Photo: George Ross</span>
                </div>
                <h4 class="text-xl font-semibold">George Ross</h4>
                <p class="text-gold">Advisor</p>
                <p class="text-sm text-gray-400 mt-2">Specializing in high-stakes negotiations and real estate structuring.</p>
            </div>
        </div>
    </section>
</main>

<?php get_footer(); ?>
