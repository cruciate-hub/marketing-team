# social.plus Email — HTML Components

All HTML components for building social.plus marketing emails. Use alongside the spec and assembly files.

---

## Base Template Shell

Every email starts with this HTML wrapper. Place all components inside `<body>`.

```html
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=yes">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>{{EMAIL_TITLE}}</title>
  <!--[if mso]>
  <style>* { font-family: sans-serif !important; }</style>
  <noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
  <![endif]-->
  <style type="text/css">
    html, body { margin: 0 !important; padding: 0 !important; width: 100% !important; height: 100% !important; }
    body { -webkit-font-smoothing: antialiased; background-color: #f5f5f5; }
    img { border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }
    table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    h1, h2, h3, h4, h5, p { margin: 0; word-break: break-word; }
    a[x-apple-data-detectors] { color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; }
    div[style*="margin: 16px 0;"] { margin: 0 !important; }
    .img-rounded { border-radius: 16px; }
    .btn-primary:hover { background-color: #272b9d !important; }
    .btn-outline:hover { background-color: #3b41ec !important; color: #ffffff !important; }
    @media all and (max-width: 789px) {
      .container { width: 100% !important; min-width: 100% !important; padding: 0 !important; }
      .row { padding-left: 20px !important; padding-right: 20px !important; }
      .mobile-stack { display: block !important; width: 100% !important; max-width: 100% !important; }
      .mobile-stack img { width: 100% !important; height: auto !important; margin-bottom: 16px !important; }
      .mobile-hide { display: none !important; }
      .mobile-center { text-align: center !important; }
      .mobile-full-width { width: 100% !important; }
      .header-cell { display: block !important; width: 100% !important; text-align: center !important; }
      .header-cell-btn { display: block !important; width: 100% !important; text-align: center !important; padding-top: 12px !important; }
      .btn-outline { font-size: 13px !important; padding: 8px 16px !important; }
      .img-rounded { border-radius: 12px !important; }
    }
    :root { color-scheme: light dark; supported-color-schemes: light dark; }
    @media (prefers-color-scheme: dark) {
      .body-bg { background-color: #1a1a1a !important; }
      .container-bg { background-color: #2d2d2d !important; }
      .text-dark { color: #f0f0f0 !important; }
      .text-body { color: #e0e0e0 !important; }
      .text-secondary { color: #a0a0a3 !important; }
      .link-muted { color: #a0a0a3 !important; }
      .link-brand { color: #7b7fff !important; }
      .footer-border { border-top-color: #444444 !important; }
      .footer-separator { color: #555555 !important; }
      .btn-outline { border-color: #7b7fff !important; color: #7b7fff !important; }
      .logo-light { display: none !important; }
      .logo-dark { display: block !important; }
      .preheader-ghost { color: #1a1a1a !important; }
    }
    [data-ogsc] .text-dark { color: #f0f0f0 !important; }
    [data-ogsc] .text-body { color: #e0e0e0 !important; }
    [data-ogsc] .text-secondary { color: #a0a0a3 !important; }
    [data-ogsc] .link-brand { color: #7b7fff !important; }
    [data-ogsc] .logo-light { display: none !important; }
    [data-ogsc] .logo-dark { display: block !important; }
    [data-ogsb] .body-bg { background-color: #1a1a1a !important; }
    [data-ogsb] .container-bg { background-color: #2d2d2d !important; }
    [data-ogsb] .logo-light { display: none !important; }
    [data-ogsb] .logo-dark { display: block !important; }
  </style>
</head>
<body class="body-bg" style="margin:0; padding:0; background-color:#f5f5f5;">
  <!-- EMAIL CONTENT GOES HERE -->
</body>
</html>
```

---

## Component: Preheader

```html
<div class="preheader-ghost" style="display:none; max-height:0px; overflow:hidden; font-size:0px; line-height:0px; color:#f5f5f5;">
  {{PREHEADER_TEXT}} &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847; &#847;
</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" class="body-bg" style="background-color:#f5f5f5;">
  <tr>
    <td align="center" style="padding:10px 0;">
      <table role="presentation" class="container" width="750" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td class="row text-secondary" align="left" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; color:#717275; line-height:20px; padding:0 40px;">{{PREHEADER_TEXT}}</td>
          <td class="row" align="right" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; line-height:20px; padding:0 40px; white-space:nowrap;">
            <a href="{$url}" class="link-muted" style="color:#414347; text-decoration:underline;">View in browser</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

---

## Component: Header

Logo left, outlined CTA button right. Default: `{{HEADER_CTA_TEXT}}` = "Explore All Updates", `{{HEADER_CTA_URL}}` = "https://social.plus/product-updates"

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" class="body-bg" style="background-color:#f5f5f5;">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
        <tr>
          <td class="row" style="padding:24px 40px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td class="header-cell" align="left" valign="middle">
                  <a href="https://social.plus" target="_blank">
                    <!--[if !mso]><!-->
                    <img class="logo-dark" src="{{LOGO_WHITE_URL}}" alt="social.plus" width="140" style="display:none; border:0;" />
                    <!--<![endif]-->
                    <img class="logo-light" src="https://storage.mlcdn.com/account_image/958330/0OpCmydxj01SEFXO54Jr1WOrPLK15IhrfL3CzQdj.png" alt="social.plus" width="140" style="display:block; border:0;" />
                  </a>
                </td>
                <td class="header-cell-btn" align="right" valign="middle" style="white-space:nowrap;">
                  <a href="{{HEADER_CTA_URL}}" target="_blank" class="btn-outline" style="display:inline-block; padding:10px 10px; border:2px solid #3b41ec; border-radius:6px; font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:14px; font-weight:600; color:#3b41ec; text-decoration:none; line-height:20px; white-space:nowrap;">{{HEADER_CTA_TEXT}}</a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

---

## Component: Intro Text

Opening paragraph before the hero image.

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
        <tr>
          <td class="row" style="padding:24px 40px;">
            <p class="text-body" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:16px; font-weight:400; color:#414347; line-height:26px;">{{INTRO_TEXT}}</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

---

## Component: Hero Image

Full-width graphic. Links to the product update page.

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
        <tr>
          <td align="center">
            <a href="{{HERO_LINK}}" target="_blank">
              <img src="{{IMAGE_HERO}}" alt="{{HERO_ALT_TEXT}}" width="750" style="display:block; width:100%; max-width:750px; height:auto; border:0;" />
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

Body Intro (text below hero): same structure as Intro Text but with `padding:24px 40px 8px 40px`.

---

## Component: Tier 1 Feature

Lead feature — full-width image, heading, description, outlined CTA. Use `#f9f9f9` background.

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#f9f9f9;">
        <tr>
          <td align="center" style="padding:32px 0 0 0;">
            <img src="{{IMAGE_TIER1}}" alt="{{FEATURE_ALT}}" width="750" style="display:block; width:100%; max-width:750px; height:auto; border:0;" />
          </td>
        </tr>
        <tr>
          <td class="row" style="padding:24px 40px 8px 40px;">
            <h2 class="text-dark" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:22px; font-weight:700; color:#111111; line-height:30px;">{{FEATURE_HEADING}}</h2>
          </td>
        </tr>
        <tr>
          <td class="row" style="padding:0 40px 24px 40px;">
            <p class="text-body" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:16px; font-weight:400; color:#414347; line-height:26px;">{{FEATURE_DESCRIPTION}}</p>
          </td>
        </tr>
        <tr>
          <td class="row" align="center" style="padding:0 40px 32px 40px;">
            <a href="{{FEATURE_CTA_URL}}" target="_blank" class="btn-outline" style="display:inline-block; padding:10px 24px; border:2px solid #3b41ec; border-radius:6px; font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:14px; font-weight:600; color:#3b41ec; text-decoration:none; line-height:20px;">{{FEATURE_CTA_TEXT}}</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

---

## Component: Tier 2 Feature

Same as Tier 1 but with `background-color:#ffffff`. Alternate between `#ffffff` and `#f9f9f9` if multiple Tier 2 features.

---

## Component: Tier 3 Feature Row (Zigzag)

Image on one side, text on the other. Alternate direction for each row. Max 280 chars for description. Module tag is a separate `<p>` element — never inline inside the `<h3>`.

**Image Left, Text Right:**

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#f9f9f9;">
        <tr>
          <td class="row" style="padding:32px 40px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td class="mobile-stack" width="335" valign="top" style="padding-right:20px;">
                  <img class="img-rounded" src="{{IMAGE_TIER3}}" alt="{{FEATURE_ALT}}" width="315" style="display:block; width:315px; height:auto; border:0; border-radius:16px;" />
                </td>
                <td class="mobile-stack" width="335" valign="middle">
                  <h3 class="text-dark" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:18px; font-weight:700; color:#111111; line-height:26px; padding-bottom:4px;">{{FEATURE_HEADING}}</h3>
                  <p class="text-secondary" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:13px; font-weight:600; color:#717275; line-height:18px; padding-bottom:8px;">{{MODULE_TAG}}</p>
                  <p class="text-body" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:16px; font-weight:400; color:#414347; line-height:26px;">{{FEATURE_DESCRIPTION}}</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

**Text Left, Image Right:** Swap the two `<td>` elements. Remove padding from image cell. Set `valign="middle"` on image cell.

---

## Component: Tier 4 List

Simple bullet list — no images. Use for brief feature mentions.

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
        <tr>
          <td class="row" style="padding:24px 40px 8px 40px;">
            <p class="text-dark" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:16px; font-weight:600; color:#111111; line-height:26px; padding-bottom:12px;">We also added</p>
          </td>
        </tr>
        <tr>
          <td class="row" style="padding:0 40px 24px 40px;">
            <p class="text-body" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:16px; font-weight:400; color:#414347; line-height:32px;">
              &#8226;&nbsp; <span class="text-secondary" style="font-size:13px; font-weight:600; color:#717275;">{{MODULE_TAG}}</span>&nbsp; {{FEATURE_TITLE}}
            </p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

---

## Component: Divider

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
        <tr>
          <td style="padding:0 40px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="border-top:1px solid #e7e7e7; font-size:0; line-height:0; height:1px;">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

---

## Component: CTA Button

Primary filled button. One per email.

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
        <tr>
          <td align="center" style="padding:32px 40px;">
            <!--[if mso]>
            <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{{CTA_URL}}" style="height:48px;v-text-anchor:middle;width:220px;" arcsize="13%" fillcolor="#3b41ec">
              <w:anchorlock/>
              <center style="color:#ffffff;font-family:'Inter',Helvetica,Arial,sans-serif;font-size:16px;font-weight:600;">{{CTA_TEXT}}</center>
            </v:roundrect>
            <![endif]-->
            <!--[if !mso]><!-->
            <a href="{{CTA_URL}}" target="_blank" class="btn-primary" style="display:inline-block; padding:14px 32px; background-color:#3b41ec; border-radius:6px; font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:16px; font-weight:600; color:#ffffff; text-decoration:none; line-height:20px; text-align:center;">{{CTA_TEXT}}</a>
            <!--<![endif]-->
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

---

## Component: Closing Text

Warm sign-off. Use `font-weight:600`.

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
        <tr>
          <td class="row" style="padding:24px 40px 32px 40px;">
            <p class="text-body" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:16px; font-weight:600; color:#414347; line-height:26px; text-align:center;">{{CLOSING_TEXT}}</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

---

## Component: Footer

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg footer-border" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff; border-top:1px solid #e7e7e7;">
        <tr>
          <td class="row" style="padding:32px 40px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td class="mobile-stack" width="50%" valign="top">
                  <p class="text-dark" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:16px; font-weight:700; color:#111111; line-height:24px; padding-bottom:8px;">social.plus</p>
                  <p class="text-secondary" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:14px; font-weight:400; color:#717275; line-height:22px; padding-bottom:16px;">The best version of every app is Social+</p>
                  <div style="padding-bottom:20px;">
                  <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                      <td style="padding-right:8px;"><a href="https://www.linkedin.com/company/socialpluscorp/" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#0A66C2; text-align:center; line-height:36px; text-decoration:none;"><img src="https://cdn.jsdelivr.net/gh/gauravghongde/social-icons@master/PNG/White/LinkedIN_white.png" alt="LinkedIn" width="20" height="20" style="border:0; vertical-align:middle;" /></a></td>
                      <td style="padding-right:8px;"><a href="https://www.instagram.com/wearesocial.plus" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#E4405F; text-align:center; line-height:36px; text-decoration:none;"><img src="https://cdn.jsdelivr.net/gh/gauravghongde/social-icons@master/PNG/White/Instagram_white.png" alt="Instagram" width="20" height="20" style="border:0; vertical-align:middle;" /></a></td>
                      <td style="padding-right:8px;"><a href="https://x.com/socialpluscorp" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#000000; text-align:center; line-height:36px; font-family:'Inter',Helvetica,Arial,sans-serif; font-size:15px; font-weight:700; color:#ffffff; text-decoration:none;">X</a></td>
                      <td style="padding-right:8px;"><a href="https://www.youtube.com/@wearesocialplus" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#FF0000; text-align:center; line-height:36px; text-decoration:none;"><img src="https://cdn.jsdelivr.net/gh/gauravghongde/social-icons@master/PNG/White/Youtube_white.png" alt="YouTube" width="20" height="20" style="border:0; vertical-align:middle;" /></a></td>
                      <td><a href="https://github.com/Amityco" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#333333; text-align:center; line-height:36px; text-decoration:none;"><img src="https://cdn.jsdelivr.net/gh/gauravghongde/social-icons@master/PNG/White/Github_white.png" alt="GitHub" width="20" height="20" style="border:0; vertical-align:middle;" /></a></td>
                    </tr>
                  </table>
                  </div>
                </td>
                <td class="mobile-stack" width="50%" valign="top" align="left" style="text-align:left;">
                  <p class="text-secondary" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:14px; font-weight:400; color:#717275; line-height:22px; padding-bottom:24px; text-align:left;">If you no longer wish to receive this newsletter, you can unsubscribe here:</p>
                  <p style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:14px; line-height:22px; text-align:left;">
                    <a href="{$unsubscribe}" class="link-brand" style="color:#3b41ec; text-decoration:underline;">Unsubscribe</a>
                    <span class="footer-separator" style="color:#b3b3b3; padding:0 8px;">|</span>
                    <a href="{$preferences}" class="link-brand" style="color:#3b41ec; text-decoration:underline;">Update preferences</a>
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```
