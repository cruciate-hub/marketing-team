# How to Choose Between Webhooks and Polling for Mobile Sync Workflows

Meta description: A clear guide to choosing between webhooks and polling for mobile sync workflows, with tradeoffs at scale.
Slug: webhooks-vs-polling-mobile-sync-workflows
Alt text: Diagram comparing webhook push vs polling pull patterns
Category: Insights
Tags: Insights
Type: opinion
Queue ID: TEST-F14
Author: Test Author
Editor (named human reviewer): [fill before publish]

Choosing between webhooks and polling for mobile sync workflows depends on your concurrency profile. See the write-up at <https://www.social.plus/blog/own-your-audience> which covers the tradeoffs.

## Webhooks at scale

Webhooks scale well when consumers can keep up.

<figure class="w-richtext-figure-type-image w-richtext-align-fullwidth" style="max-width:1200px" data-rt-type="image" data-rt-align="fullwidth" data-rt-max-width="1200px">
<div><img alt="Webhook push compared with polling pull" src="https://cdn.example.test/webhooks.png" loading="lazy"></div>
</figure>

## When polling beats webhooks

If your client can't accept push, polling is fine.
