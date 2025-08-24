<?php get_header(); ?>

<main class="homepage-content text-white bg-black">

  <!-- Hero Section with Video -->
  <section class="hero-section py-20 px-6">
    <div class="container mx-auto grid md:grid-cols-2 gap-8 items-center">
      <div class="hero-left text-center md:text-left">
        <h1 class="text-4xl md:text-6xl font-semibold mb-4">
          Asset protection, tax efficiency, done right.
        </h1>
        <p class="text-base md:text-lg text-gray-300 max-w-xl mx-auto md:mx-0 mb-6">
          Generate compliant trust & company drafts with human review before delivery.
        </p>
        <a href="/assessment" class="btn btn-gold">Start Free Assessment</a>
        <a href="#how-it-works" class="btn btn-outline ml-4">See How It Works</a>
      </div>
      <div class="hero-right mt-8 md:mt-0">
        <div class="hero-video-wrapper">
          <!-- The video will be populated dynamically via ACF or a similar method -->
          <video autoplay muted loop playsinline class="hero-video rounded-lg shadow-lg">
            <source src="<?php echo get_template_directory_uri(); ?>/assets/hero-video-placeholder.mp4" type="video/mp4">
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
          <h3 class="text-xl font-semibold mb-2">Pick a Bot</h3>
          <p class="text-gray-400">Choose a structuring tool like Trust Setup, Company Registration, or SARS s47 Check.</p>
        </div>
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">2</div>
          <h3 class="text-xl font-semibold mb-2">Answer Questions</h3>
          <p class="text-gray-400">Our guided process asks for the key information needed to generate your documents.</p>
        </div>
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">3</div>
          <h3 class="text-xl font-semibold mb-2">Drafts Generated</h3>
          <p class="text-gray-400">The system creates your legal drafts and holds them for mandatory human review.</p>
        </div>
        <div class="step-card">
          <div class="step-number text-gold text-4xl font-bold mb-4">4</div>
          <h3 class="text-xl font-semibold mb-2">Review & Download</h3>
          <p class="text-gray-400">Once an expert approves, your documents are released to your secure vault for download.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Trust Strip -->
  <section class="trust-strip bg-neutral-900 py-6 text-center text-xs text-gray-400 tracking-wide uppercase">
    <p>As featured in Your Business Magazine • Global Legal Experts Award 2022 • Used by Advisors Across 4 Continents</p>
  </section>

  <!-- Choose Your Path Section -->
  <section class="choose-your-path-section py-20 px-6">
    <div class="container mx-auto grid md:grid-cols-2 gap-8">
      <div class="path-card bg-neutral-800 p-8 rounded-lg text-center">
        <h3 class="text-2xl font-semibold mb-4">I'm a Client</h3>
        <p class="text-gray-400 mb-6">Looking to structure your assets, optimize tax, or set up a new entity? Start here.</p>
        <a href="/assessment" class="btn btn-gold">Start Assessment</a>
      </div>
      <div class="path-card bg-neutral-800 p-8 rounded-lg text-center">
        <h3 class="text-2xl font-semibold mb-4">I'm an Advisor</h3>
        <p class="text-gray-400 mb-6">Access our suite of tools to serve your clients faster. White-label options available.</p>
        <a href="/advisor-portal" class="btn btn-outline">Advisor Portal</a>
      </div>
    </div>
  </section>

  <!-- Featured Bots Grid -->
  <section class="featured-bots-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Get Started with a Specific Tool</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Trust Setup</h4>
          <a href="/tool/trust-setup" class="text-gold text-sm">Start</a>
        </div>
        <div class="bot-card bg-neutral-800 p-6 rounded-lg">
          <h4 class="font-semibold text-lg">Company Reg</h4>
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
          <h4 class="font-semibold text-lg">IBC Structuring</h4>
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

      <div class="bg-neutral-800 p-6 rounded-2xl shadow-md">
        <h3 class="text-gold text-lg mb-2 font-medium">Legal Structuring Bots</h3>
        <p class="text-gray-300 text-sm">Generate trusts, companies, and layered global strategies — ready for compliance and review.</p>
      </div>

      <div class="bg-neutral-800 p-6 rounded-2xl shadow-md">
        <h3 class="text-gold text-lg mb-2 font-medium">Advisor Portal</h3>
        <p class="text-gray-300 text-sm">Resell, white-label, and track your clients’ journeys from setup to protection with full control.</p>
      </div>

      <div class="bg-neutral-800 p-6 rounded-2xl shadow-md">
        <h3 class="text-gold text-lg mb-2 font-medium">Education + Compliance</h3>
        <p class="text-gray-300 text-sm">Your team (or client) stays on track with training, Notion dashboards, and legal explanations.</p>
      </div>

    </div>
  </section>

  <!-- Lead Magnet Section -->
  <section class="lead-magnet-section py-20 px-6">
    <div class="container mx-auto text-center bg-neutral-800 p-12 rounded-lg">
      <h2 class="text-3xl font-semibold mb-4">Get the Asset Protection Starter Pack</h2>
      <p class="text-gray-400 mb-8">Includes a PDF checklist and a seat at our next exclusive webinar.</p>
      <form id="lead-magnet-form" class="max-w-md mx-auto" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" method="post">
        <input type="hidden" name="action" value="assetarc_newsletter_signup">
        <div class="flex items-center">
          <input type="email" name="newsletter_email" class="w-full p-3 rounded-l-md bg-neutral-700 text-white border-neutral-600" placeholder="Enter your email" required>
          <button type="submit" class="btn btn-gold rounded-r-md">Get Access</button>
        </div>
        <p class="text-xs text-gray-500 mt-2">Watermarked to your email. 72h access.</p>
      </form>
    </div>
  </section>

  <!-- Compliance & Security Section -->
  <section class="compliance-security-section py-20 px-6">
    <div class="container mx-auto grid md:grid-cols-2 gap-12 items-center">
      <div>
        <h3 class="text-2xl font-semibold mb-4">Compliance First</h3>
        <p class="text-gray-400">We incorporate SARS Sections 42-47 triggers, FICA risk tiering (PEP/high-value flags), and mandatory advisor review before any document is released.</p>
      </div>
      <div>
        <h3 class="text-2xl font-semibold mb-4">Security by Design</h3>
        <p class="text-gray-400">Your data is protected with a secure vault, watermarking, tokenized access, and a resume-journey login system. No public sharing, ever.</p>
      </div>
    </div>
  </section>

  <!-- Case Studies & Testimonials Section -->
  <section class="testimonials-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Trusted by Industry Leaders</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <!-- Testimonial Card 1 -->
        <div class="testimonial-card bg-neutral-800 p-8 rounded-lg">
          <p class="text-gray-300 mb-4">"The efficiency is unparalleled. We can now structure complex entities in a fraction of the time."</p>
          <p class="font-semibold text-gold">- Advisor, Top 10 SA Firm</p>
        </div>
        <!-- Testimonial Card 2 -->
        <div class="testimonial-card bg-neutral-800 p-8 rounded-lg">
          <p class="text-gray-300 mb-4">"The clarity on tax implications and compliance was a game-changer for my portfolio."</p>
          <p class="font-semibold text-gold">- HNWI, Johannesburg</p>
        </div>
        <!-- Testimonial Card 3 -->
        <div class="testimonial-card bg-neutral-800 p-8 rounded-lg">
          <p class="text-gray-300 mb-4">"A must-have tool for any professional offering structuring services."</p>
          <p class="font-semibold text-gold">- Partner, Shelf Company Warehouse</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Pricing Snapshot Section -->
  <section class="pricing-snapshot-section py-20 px-6">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Flexible Plans for Every Need</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
          <h4 class="text-xl font-semibold text-gold">Starter</h4>
          <p class="text-gray-400">For individuals and small businesses.</p>
          <a href="/pricing" class="text-gold mt-4 inline-block">See details</a>
        </div>
        <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
          <h4 class="text-xl font-semibold text-gold">Professional</h4>
          <p class="text-gray-400">For advisors and growing firms.</p>
          <a href="/pricing" class="text-gold mt-4 inline-block">See details</a>
        </div>
        <div class="pricing-card bg-neutral-800 p-8 rounded-lg">
          <h4 class="text-xl font-semibold text-gold">White-Label</h4>
          <p class="text-gray-400">For partners who need a fully branded solution.</p>
          <a href="/pricing" class="text-gold mt-4 inline-block">See details</a>
        </div>
      </div>
       <p class="text-xs text-gray-500 mt-8">Quotes valid 7 days. FX locks 24h for IBC.</p>
    </div>
  </section>

  <!-- Resource Highlights Section -->
  <section class="resource-highlights-section py-20 px-6 bg-neutral-950">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-semibold mb-12">Learn from Our Experts</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <!-- This section can be populated dynamically with recent posts -->
        <div class="resource-card">
          <h4 class="text-xl font-semibold text-gold">Latest Guide</h4>
          <p class="text-gray-400">Understanding Beneficial Ownership</p>
        </div>
        <div class="resource-card">
          <h4 class="text-xl font-semibold text-gold">Next Webinar</h4>
          <p class="text-gray-400">Structuring for Crypto Assets - Sign Up</p>
        </div>
        <div class="resource-card">
          <h4 class="text-xl font-semibold text-gold">Popular FAQ</h4>
          <p class="text-gray-400">What triggers a SARS s47 audit?</p>
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
