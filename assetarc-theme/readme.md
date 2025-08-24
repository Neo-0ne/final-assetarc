# AssetArc Theme

## Overview
This is the official WordPress theme for AssetArc, designed for:
- Asset protection
- Tax structuring
- Professional consulting platforms

## Structure
- **Dark Mode**: Black base with gold gradient (#FFD700 → #8C6239)
- **Header/Footer**: Fully responsive with menu injection
- **Bot Integration**: Flask endpoints embedded in dashboard & vault
- **Calendly**: Embedded via token flow
- **Newsletter**: Connected via `newsletter-handler.php`

## Customization
- Upload logo & favicon via Appearance > Customize
- Edit theme colors in `style.css`
- Dashboard available via `/dashboard/` (requires plugin logic)

## Installation
1. Upload theme ZIP
2. Activate from Appearance > Themes
3. Customize from WP Customizer

## Support
All bot logic runs via Flask; see documentation in `/bots/` and `/vault-access.php`.

## Newsletter
To add a newsletter signup form to your site, you can add the following HTML to any page or widget:

```html
<form method="post" action="">
  <label for="newsletter_email">Subscribe to our newsletter:</label>
  <input type="email" id="newsletter_email" name="newsletter_email" placeholder="Enter your email">
  <button type="submit">Subscribe</button>
</form>
```

## Developed for: AssetArc © 2025
