# social.plus Email — Content Blocks

Feature layouts, CTA button, closing text, and footer. Use alongside structure, spec, and assembly files.

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

**Text Left, Image Right:**

Image is first in the DOM so it stacks on top on mobile. `direction:rtl` on the inner table visually flips it to the right on desktop. Always use this pattern — never just swap the `<td>` elements.

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;" class="body-bg">
  <tr>
    <td align="center">
      <table role="presentation" class="container container-bg" width="750" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
        <tr>
          <td class="row" style="padding:32px 40px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="direction:rtl;">
              <tr>
                <td class="mobile-stack" width="335" valign="middle" style="direction:ltr; padding-left:20px;">
                  <img class="img-rounded" src="{{IMAGE_TIER3}}" alt="{{FEATURE_ALT}}" width="315" style="display:block; width:315px; height:auto; border:0; border-radius:16px;" />
                </td>
                <td class="mobile-stack" width="335" valign="middle" style="direction:ltr;">
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
                <td class="mobile-stack mobile-center" width="50%" valign="top">
                  <p class="text-dark" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:16px; font-weight:700; color:#111111; line-height:24px; padding-bottom:8px;">social.plus</p>
                  <p class="text-secondary" style="font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; font-size:14px; font-weight:400; color:#717275; line-height:22px; padding-bottom:16px;">The best version of every app is Social+</p>
                  <div style="padding-bottom:20px;">
                  <table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                      <td style="padding-right:8px;"><a href="https://www.linkedin.com/company/socialpluscorp/" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#0A66C2; text-align:center; line-height:36px; text-decoration:none; font-family:'Inter',Helvetica,Arial,sans-serif; font-size:13px; font-weight:700; color:#ffffff;">in</a></td>
                      <td style="padding-right:8px;"><a href="https://www.instagram.com/wearesocial.plus" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#E4405F; text-align:center; line-height:36px; text-decoration:none; font-family:'Inter',Helvetica,Arial,sans-serif; font-size:13px; font-weight:700; color:#ffffff;">ig</a></td>
                      <td style="padding-right:8px;"><a href="https://x.com/socialpluscorp" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#000000; text-align:center; line-height:36px; text-decoration:none; font-family:'Inter',Helvetica,Arial,sans-serif; font-size:15px; font-weight:700; color:#ffffff;">X</a></td>
                      <td style="padding-right:8px;"><a href="https://www.youtube.com/@wearesocialplus" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#FF0000; text-align:center; line-height:36px; text-decoration:none; font-family:'Inter',Helvetica,Arial,sans-serif; font-size:13px; font-weight:700; color:#ffffff;">yt</a></td>
                      <td><a href="https://github.com/Amityco" target="_blank" style="display:inline-block; width:36px; height:36px; border-radius:6px; background-color:#555555; text-align:center; line-height:36px; text-decoration:none; font-family:'Inter',Helvetica,Arial,sans-serif; font-size:13px; font-weight:700; color:#ffffff;">gh</a></td>
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
