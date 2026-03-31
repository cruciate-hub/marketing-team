# social.plus Email — Structure

Base shell, preheader, header, intro text, and hero image. Use alongside blocks, spec, and assembly files.

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
      img.icon-img { width: 16px !important; height: 16px !important; margin-bottom: 0 !important; }
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
