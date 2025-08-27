<?php get_header(); ?>

<main class="homepage-content text-white bg-black">

  <!-- Hero Section with Video -->
  <section class="hero-section py-20 px-6">
    <div class="container mx-auto grid md:grid-cols-2 gap-8 items-center">
      <div class="hero-left text-center md:text-left">
        <h1 class="text-4xl md:text-6xl font-semibold mb-4">
          Asset Protection & Tax Structuring, Automated — With Human Review
        </h1>
        <p class="text-base md:text-lg text-gray-300 max-w-xl mx-auto md:mx-0 mb-6">
          Generate trusts, companies, and SARS s42–47 compliant drafts in minutes. All documents are verified by licensed professionals before delivery.
        </p>
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
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">1</div>
          <h3 class="text-xl font-semibold mb-2">Choose your process</h3>
          <p class="text-gray-400">Choose your process (Trust Setup, Company Registration, Compliance Check).</p>
        </div>
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">2</div>
          <h3 class="text-xl font-semibold mb-2">Answer guided questions</h3>
          <p class="text-gray-400">Answer guided questions to provide the necessary information.</p>
        </div>
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">3</div>
          <h3 class="text-xl font-semibold mb-2">Draft documents are generated</h3>
          <p class="text-gray-400">Your documents are instantly generated and held for verification.</p>
        </div>
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">4</div>
          <h3 class="text-xl font-semibold mb-2">Human expert reviews them</h3>
          <p class="text-gray-400">A human expert reviews them before release into your secure vault.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Trust Strip -->
  <section class="trust-strip bg-neutral-900 py-8 text-center">
    <div class="container mx-auto">
      <p class="text-sm text-gray-400 tracking-wide uppercase mb-4">Trusted by South African founders, global entrepreneurs, and licensed advisors.</p>
      <div class="flex justify-center space-x-8">
        <span class="text-xs font-semibold text-gold">FICA Compliant</span>
        <span class="text-xs font-semibold text-gold">SARS s42–47 Aware</span>
        <span class="text-xs font-semibold text-gold">Human Reviewed</span>
      </div>
    </div>
  </section>

  <!-- Choose Your Path Section -->
  <section class="choose-your-path-section py-20 px-6">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Choose Your Path</h2>
      <div class="grid md:grid-cols-2 gap-8">
        <div class="path-card bg-neutral-800 p-8 rounded-lg text-center">
          <h3 class="text-2xl font-semibold mb-4">I’m a Client</h3>
          <p class="text-gray-400 mb-6">Start your assessment, generate your draft pack, and access compliance-ready templates.</p>
          <a href="/assessment" class="btn btn-gold">Start Assessment</a>
        </div>
        <div class="path-card bg-neutral-800 p-8 rounded-lg text-center">
          <h3 class="text-2xl font-semibold mb-4">I’m an Advisor</h3>
          <p class="text-gray-400 mb-6">Offer white-label automation, manage tokens, and deliver branded packs to clients.</p>
          <a href="/advisor-portal" class="btn btn-outline">Explore Advisor Tools</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Featured Workflows Section -->
  <section class="featured-workflows-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Featured Workflows</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Trust Setup</h4>
          <p class="text-xs text-gray-400 mt-1">Local & Offshore</p>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Company Registration</h4>
          <p class="text-xs text-gray-400 mt-1">CIPC, BVI, St. Kitts</p>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">SARS Section 47 Test</h4>
          <p class="text-xs text-gray-400 mt-1">Compliance Check</p>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">FICA Intake</h4>
          <p class="text-xs text-gray-400 mt-1">Risk Tiering</p>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Intl. Structuring</h4>
          <p class="text-xs text-gray-400 mt-1">FX-locked USD Quotes</p>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Instant Quote</h4>
          <p class="text-xs text-gray-400 mt-1">ZAR, USD, Crypto</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Feature Cards Section Removed -->

  <!-- Lead Magnet Section -->
  <section class="lead-magnet-section py-20 px-6">
    <div class="container mx-auto text-center bg-neutral-800 p-12 rounded-lg">
      <h2 class="text-3xl font-semibold mb-4">Unlock the Asset Protection Starter Pack</h2>
      <p class="text-gray-400 mb-8">Get our free checklist, a seat at our next webinar, and a sample compliance report.</p>
      <form id="lead-magnet-form" class="max-w-md mx-auto" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" method="post">
        <input type="hidden" name="action" value="assetarc_newsletter_signup">
        <div class="flex items-center">
          <input type="email" name="newsletter_email" class="w-full p-3 rounded-l-md bg-neutral-700 text-white border-neutral-600" placeholder="Enter your email" required>
          <button type="submit" class="btn btn-gold rounded-r-md">Get Access</button>
        </div>
        <p class="text-xs text-gray-500 mt-2">Join our mailing list to receive your starter pack.</p>
      </form>
    </div>
  </section>

  <!-- Compliance & Security Section -->
  <section class="compliance-security-section py-20 px-6">
    <div class="container mx-auto grid md:grid-cols-2 gap-12 items-center">
      <div>
        <h3 class="text-2xl font-semibold mb-4">Compliance</h3>
        <ul class="list-disc list-inside text-gray-400 space-y-2">
            <li>Section 42–47 triggers built in</li>
            <li>FICA risk-tiering (PEP/high-value flags)</li>
            <li>Human review before release</li>
        </ul>
      </div>
      <div>
        <h3 class="text-2xl font-semibold mb-4">Security</h3>
        <ul class="list-disc list-inside text-gray-400 space-y-2">
            <li>Tokenized access</li>
            <li>Watermarked drafts</li>
            <li>Resume anytime with secure vault</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- Social Proof Section -->
  <section class="testimonials-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Success Stories</h2>
      <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <!-- Case Study -->
        <div class="testimonial-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-gold mb-2">Case Study: Family Restructure</h4>
          <p class="text-gray-300">“High-net-worth family restructured holdings — 30% tax saving, SARS compliant.”</p>
        </div>
        <!-- Testimonial -->
        <div class="testimonial-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-gold mb-2">Advisor Testimonial</h4>
          <p class="text-gray-300">“The only structuring system that actually understands SA compliance.”</p>
          <p class="text-xs text-gray-500 mt-3">– J.B., Advisor</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Pricing Snapshot Section -->
  <section class="pricing-snapshot-section py-20 px-6">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Pricing Snapshot</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
          <h4 class="text-xl font-semibold text-gold">Starter</h4>
          <p class="text-gray-400">From R1,200</p>
          <a href="/pricing" class="text-gold mt-4 inline-block">See details</a>
        </div>
        <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
          <h4 class="text-xl font-semibold text-gold">Professional</h4>
          <p class="text-gray-400">Multi-service bundles</p>
          <a href="/pricing" class="text-gold mt-4 inline-block">See details</a>
        </div>
        <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
          <h4 class="text-xl font-semibold text-gold">Advisor / White-label</h4>
          <p class="text-gray-400">Custom pricing, token allocation</p>
          <a href="/pricing" class="text-gold mt-4 inline-block">See details</a>
        </div>
      </div>
       <p class="text-xs text-gray-500 mt-8">Quotes valid 7 days. FX locks 24h for IBC.</p>
    </div>
  </section>

  <!-- Resource Highlights Section -->
  <section class="resource-highlights-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Resource Highlights</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <div class="resource-card">
          <h4 class="text-xl font-semibold text-gold">Latest Guide</h4>
          <p class="text-gray-400">Structuring Trusts in 2025</p>
        </div>
        <div class="resource-card">
          <h4 class="text-xl font-semibold text-gold">Upcoming Webinar</h4>
          <p class="text-gray-400">How to Stay s47 Compliant</p>
        </div>
        <div class="resource-card">
          <h4 class="text-xl font-semibold text-gold">FAQ</h4>
          <p class="text-gray-400">What triggers a SARS restructure test?</p>
        </div>
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
