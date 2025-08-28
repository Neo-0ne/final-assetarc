<?php get_header(); ?>

<main class="homepage-content text-white bg-black">

  <!-- Hero Section with Video -->
  <section class="hero-section py-20 px-6">
    <div class="container mx-auto grid md:grid-cols-2 gap-8 items-center">
      <div class="hero-left text-center md:text-left">
        <!-- Jules: Synthesized content for review -->
        <h1 class="text-4xl md:text-6xl font-semibold mb-4">
          Structure is Not an Event—It’s a Strategy.
        </h1>
        <p class="text-base md:text-lg text-gray-300 max-w-xl mx-auto md:mx-0 mb-6">
          Control assets without owning them directly. Our platform translates the complex principles of legal and tax structuring into automated, compliant workflows, always with human-verified output.
        </p>
        <!-- End synthesized content -->
        <a href="/assessment" class="btn btn-gold">Start Free Assessment</a>
        <a href="#how-it-works" class="btn btn-outline ml-4">See How It Works</a>
      </div>
      <div class="hero-right mt-8 md:mt-0">
        <div class="hero-video-wrapper">
          <!-- The video will be populated dynamically via ACF or a similar method -->
          <video autoplay muted loop playsinline class="hero-video rounded-lg shadow-lg">
            <source src="<?php echo get_template_directory_uri(); ?>/assets/hero-video.mp4" type="video/mp4">
          </video>
        </div>
      </div>
    </div>
  </section>

  <!-- How It Works Section -->
  <section id="how-it-works" class="how-it-works-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">How It Works</h2>
      <div class="grid md:grid-cols-4 gap-8">
        <!-- Jules: Synthesized content for review -->
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">1</div>
          <h3 class="text-xl font-semibold mb-2">Select a Workflow</h3>
          <p class="text-gray-400">Choose a structuring process, such as Trust Formation, Company Registration, or a SARS s47 Compliance Check.</p>
        </div>
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">2</div>
          <h3 class="text-xl font-semibold mb-2">Provide Key Data</h3>
          <p class="text-gray-400">Our guided intake captures the essential information required for your legal and compliance documents.</p>
        </div>
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">3</div>
          <h3 class="text-xl font-semibold mb-2">Drafts are Generated</h3>
          <p class="text-gray-400">The platform generates your draft documents, which are immediately held for mandatory human review.</p>
        </div>
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">4</div>
          <h3 class="text-xl font-semibold mb-2">Review & Access</h3>
          <p class="text-gray-400">Once a qualified professional verifies the output, your documents are released to your secure vault.</p>
        </div>
        <!-- End synthesized content -->
      </div>
    </div>
  </section>

  <!-- Trust Strip -->
  <section class="trust-strip bg-neutral-900 py-6 text-center text-xs text-gray-400 tracking-wide uppercase">
    <p>As featured in Your Business Magazine • Global Legal Experts Award 2022 • Used by Advisors Across 4 Continents</p>
  </section>

  <!-- Choose Your Path Section -->
  <section class="choose-your-path-section py-20 px-6">
    <!-- Jules: Synthesized content for review -->
    <div class="container mx-auto grid md:grid-cols-2 gap-8">
      <div class="path-card bg-neutral-800 p-8 rounded-lg text-center">
        <h3 class="text-2xl font-semibold mb-4">For Founders & Individuals</h3>
        <p class="text-gray-400 mb-6">Shield your personal assets from business risks and ensure your legacy is protected with compliant, layered structures.</p>
        <a href="/assessment" class="btn btn-gold">Start Assessment</a>
      </div>
      <div class="path-card bg-neutral-800 p-8 rounded-lg text-center">
        <h3 class="text-2xl font-semibold mb-4">For Professional Advisors</h3>
        <p class="text-gray-400 mb-6">Elevate your practice. Deliver strategic, automated structuring solutions to your clients with our white-label portal.</p>
        <a href="/advisor-portal" class="btn btn-outline">Advisor Portal</a>
      </div>
    </div>
    <!-- End synthesized content -->
  </section>

  <!-- Featured Workflows Section -->
  <section class="featured-workflows-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <!-- Jules: Synthesized content for review -->
      <h2 class="text-3xl font-semibold mb-12">Core Structuring Workflows</h2>
      <!-- End synthesized content -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Trust Formation</h4>
          <a href="/tool/trust-setup" class="text-gold text-sm">Start</a>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Company Registration</h4>
          <a href="/tool/company-setup" class="text-gold text-sm">Start</a>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">SARS s47 Check</h4>
          <a href="/tool/sars-s47-check" class="text-gold text-sm">Start</a>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">FICA Intake</h4>
          <a href="/tool/fica-intake" class="text-gold text-sm">Start</a>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Global Structuring</h4>
          <a href="/tool/ibc-structuring" class="text-gold text-sm">Start</a>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Quote Generator</h4>
          <a href="/tool/quote-generator" class="text-gold text-sm">Start</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Feature Cards -->
  <section class="feature-section py-20 px-6">
    <div class="container mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- Jules: Synthesized content for review -->
      <div class="bg-neutral-800 p-6 rounded-2xl shadow-md">
        <h3 class="text-gold text-lg mb-2 font-medium">Automated Structuring</h3>
        <p class="text-gray-300 text-sm">Generate trusts, companies, and layered global strategies — built on proven legal models and ready for human review.</p>
      </div>

      <div class="bg-neutral-800 p-6 rounded-2xl shadow-md">
        <h3 class="text-gold text-lg mb-2 font-medium">White-Label for Advisors</h3>
        <p class="text-gray-300 text-sm">Resell, rebrand, and manage your clients’ entire structuring journey with our secure, multi-tenant advisor portal.</p>
      </div>

      <div class="bg-neutral-800 p-6 rounded-2xl shadow-md">
        <h3 class="text-gold text-lg mb-2 font-medium">Integrated Education</h3>
        <p class="text-gray-300 text-sm">Access guides, webinars, and explainers drawn directly from 'The Definitive Structuring Guide' to stay compliant.</p>
      </div>
      <!-- End synthesized content -->
    </div>
  </section>

  <!-- Lead Magnet Section -->
  <section class="lead-magnet-section py-20 px-6">
    <div class="container mx-auto text-center bg-neutral-800 p-12 rounded-lg">
      <h2 class="text-3xl font-semibold mb-4">Get The Definitive Structuring Guide</h3>
      <p class="text-gray-400 mb-8">Download the complete guide that powers AssetArc. Includes checklists, case studies, and compliance playbooks.</p>
      <form id="lead-magnet-form" class="max-w-md mx-auto" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" method="post">
        <input type="hidden" name="action" value="assetarc_newsletter_signup">
        <div class="flex items-center">
          <input type="email" name="newsletter_email" class="w-full p-3 rounded-l-md bg-neutral-700 text-white border-neutral-600" placeholder="Enter your email" required>
          <button type="submit" class="btn btn-gold rounded-r-md">Get The Guide</button>
        </div>
        <p class="text-xs text-gray-500 mt-2">Watermarked to your email. For educational purposes only.</p>
      </form>
    </div>
  </section>

  <!-- Compliance & Security Section -->
  <section class="compliance-security-section py-20 px-6">
    <div class="container mx-auto grid md:grid-cols-2 gap-12 items-center">
      <!-- Jules: Synthesized content for review -->
      <div>
        <h3 class="text-2xl font-semibold mb-4">Compliance by Design</h3>
        <p class="text-gray-400">Our workflows incorporate critical SARS provisions, FICA risk tiering, and BO Register alignment. Every output is verified by a human professional before release.</p>
      </div>
      <div>
        <h3 class="text-2xl font-semibold mb-4">Security as a Foundation</h3>
        <p class="text-gray-400">Your data is protected within a secure vault, with tokenized access controls, document watermarking, and end-to-end encryption. Privacy and security are paramount.</p>
      </div>
      <!-- End synthesized content -->
    </div>
  </section>

  <!-- Social Proof Section -->
  <section class="testimonials-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Trusted by Global Leaders & Industry Experts</h2>
      <!-- Jules: Synthesized content for review -->
      <div class="grid md:grid-cols-3 gap-8">
        <!-- Social Proof Card 1 -->
        <div class="testimonial-card bg-neutral-800 p-6 rounded-lg flex flex-col items-center">
          <img src="<?php echo get_template_directory_uri(); ?>/assets/images/social-proof/michael-douglas.jpg" alt="Michael Douglas" class="w-24 h-24 rounded-full mx-auto mb-4 object-cover border-2 border-gold-dark">
          <p class="font-semibold text-gold">Michael Douglas</p>
          <p class="text-xs text-gray-400 mb-3">Academy Award-Winning Actor</p>
          <p class="text-gray-300 text-sm">In conversation with our founder about structuring for legacy projects.</p>
        </div>
        <!-- Social Proof Card 2 -->
        <div class="testimonial-card bg-neutral-800 p-6 rounded-lg flex flex-col items-center">
          <img src="<?php echo get_template_directory_uri(); ?>/assets/images/social-proof/steve-wozniak.jpg" alt="Steve Wozniak" class="w-24 h-24 rounded-full mx-auto mb-4 object-cover border-2 border-gold-dark">
          <p class="font-semibold text-gold">Steve Wozniak</p>
          <p class="text-xs text-gray-400 mb-3">Co-founder, Apple Inc.</p>
          <p class="text-gray-300 text-sm">Discussing the future of technology and its impact on global asset management.</p>
        </div>
        <!-- Social Proof Card 3 -->
        <div class="testimonial-card bg-neutral-800 p-6 rounded-lg flex flex-col items-center">
          <img src="<?php echo get_template_directory_uri(); ?>/assets/images/social-proof/stedman-graham.jpg" alt="Stedman Graham" class="w-24 h-24 rounded-full mx-auto mb-4 object-cover border-2 border-gold-dark">
          <p class="font-semibold text-gold">Stedman Graham</p>
          <p class="text-xs text-gray-400 mb-3">Author & CEO, S. Graham & Associates</p>
          <p class="text-gray-300 text-sm">Sharing insights on leadership and building enduring personal brands.</p>
        </div>
      </div>
      <!-- End synthesized content -->
    </div>
  </section>

  <!-- Pricing Snapshot Section -->
  <section class="pricing-snapshot-section py-20 px-6">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Transparent Plans for Every Goal</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
          <h4 class="text-xl font-semibold text-gold">Starter</h4>
          <p class="text-gray-400">For individuals and single entities.</p>
          <a href="/pricing" class="text-gold mt-4 inline-block">See details</a>
        </div>
        <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
          <h4 class="text-xl font-semibold text-gold">Professional</h4>
          <p class="text-gray-400">For advisors and growing firms.</p>
          <a href="/pricing" class="text-gold mt-4 inline-block">See details</a>
        </div>
        <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
          <h4 class="text-xl font-semibold text-gold">White-Label</h4>
          <p class="text-gray-400">For partners requiring a fully branded, integrated solution.</p>
          <a href="/pricing" class="text-gold mt-4 inline-block">See details</a>
        </div>
      </div>
       <p class="text-xs text-gray-500 mt-8">Quotes valid 7 days. FX locks 24h for IBC.</p>
    </div>
  </section>

  <!-- Resource Highlights Section -->
  <section class="resource-highlights-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Learn from The Definitive Guide</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <!-- Jules: Synthesized content for review -->
        <!-- This section can be populated dynamically with recent posts -->
        <div class="resource-card">
          <h4 class="text-xl font-semibold text-gold">Core Concept</h4>
          <p class="text-gray-400">The Four-Structure Stack to Isolate Risk</p>
        </div>
        <div class="resource-card">
          <h4 class="text-xl font-semibold text-gold">Compliance Deep Dive</h4>
          <p class="text-gray-400">The Section 7C Loan Neutralization Playbook</p>
        </div>
        <div class="resource-card">
          <h4 class="text-xl font-semibold text-gold">Global Structuring</h4>
          <p class="text-gray-400">Substance vs. Shells in a CRS World</p>
        </div>
        <!-- End synthesized content -->
      </div>
      <a href="/resources" class="btn btn-outline mt-12">See All Resources</a>
    </div>
  </section>

  <!-- Final CTA Strip -->
  <section class="final-cta-section py-16">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-4">Ready to structure with confidence?</h2>
      <a href="/assessment" class="btn btn-gold mr-4">Start Free Assessment</a>
      <a href="/contact" class="btn btn-outline">Talk to Us</a>
    </div>
  </section>

</main>

<?php get_footer(); ?>
