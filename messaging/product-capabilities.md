# social.plus product capabilities

Source of truth for what social.plus offers, for everyone who writes about the product. Compiled 2026-10-05 from, in order of authority: the official docs at https://learn.social.plus, the website inventory in this repo (`website/pages-*.json`) and the live product pages on https://www.social.plus. Every row is backed by a docs URL. Claims found only on the website are not in the tables; the content team is confirming them with the product owner. Refresh a row when a release note changes it, and check the whole file every quarter.

## How to use this file

- **Every sentence or link that says or implies "social.plus does X" must match a row here.** That includes product-page links: link only to a page that describes a capability listed in this file.
- **If it is not here, do not claim it.** Ask the product owner, or check the docs and add a row with the docs URL and the date you checked.
- **Never attribute anything in "Outside social.plus scope" to social.plus**, not even as "you can use social.plus for X".
- **Use the wording in the "What it does" column, not stronger.** Do not add "automatically", "real-time", "AI-powered", "any", "every platform" or "out of the box" unless the row says so.
- **Check "Platforms / limits" before you generalise.** Many features are missing on one SDK or UIKit platform (most often Flutter). "Enabled on request" means social.plus support switches the feature on: say "available", not "included by default".
- **Anything not in a table is not claimable**, including claims that appear only on the website or the pricing page, until the product owner confirms them and they move into a table.
- **The check.** `scripts/product_claims.py` (compliance check `product_claims`, FAIL) flags any paragraph that names social.plus or links a product page and contains a word from the second column of the "Outside social.plus scope" table, unless that sentence is negated ("social.plus does not process payments"). It cannot see a claim that is simply not in the tables; the reviewer's "Claims about social.plus" list in the review Doc covers that.
- **No prices.** Plan names and allowances only as written in a row.
- **Names:** APIs, SDKs, UIKit (code components), UI Kit (Figma design files), Console, Portal, Dashboard. "Community" is fine for the product feature (communities, community management), not as the category.

Platform abbreviations: SDKs are iOS, Android, TS (TypeScript, used for web and, with guidance, React Native) and Flutter. UIKits are iOS, Android, Web (React), RN (React Native) and Flutter. "All SDKs" or "all UIKits" means the docs mark every platform as supported. Platform data comes from the docs Feature Matrix (https://learn.social.plus/feature-matrix) unless the row cites another page.

## Social

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| Communities | Lets users create and join communities that are public, private and hidden, or private but discoverable. | Discoverable private communities: SDK iOS/Android/TS, UIKit iOS/Android/Web (not Flutter or RN). | https://learn.social.plus/social-plus-sdk/social/communities-spaces/overview | 2026-10-05 |
| Community membership and approval | Supports join requests that a moderator approves, community invitations, and adding or removing members. | Moderator approval: SDK iOS/Android/TS, UIKit iOS/Android/Web. | https://learn.social.plus/social-plus-sdk/social/communities-spaces/organization/join-leave-community | 2026-10-05 |
| Community categories and tags | Groups communities by category, and by tag, so users can browse and filter them. | Up to 10 categories per community (UIKit). Community tags on the iOS and Android SDKs. | https://learn.social.plus/social-plus-sdk/social/communities-spaces/organization/community-categories | 2026-10-05 |
| Community roles and moderation | Assigns community roles such as moderator, bans or unbans members, and checks what a member may do. | | https://learn.social.plus/social-plus-sdk/social/communities-spaces/organization/community-moderation | 2026-10-05 |
| Official community badge | Shows an "Official" badge on communities marked as official. | All SDKs and UIKits. | https://learn.social.plus/feature-matrix | 2026-10-05 |
| Trending and recommended communities | Returns trending communities and communities recommended for the current user. | Recommended list returns up to 15 communities. | https://learn.social.plus/social-plus-sdk/social/communities-spaces/discovery/trending-and-recommended-communities | 2026-10-05 |
| Posts: text, image, video, file, poll and custom | Lets users publish posts in these formats to a user feed or a community feed. | Text up to 20,000 characters; up to 10 images per post. Custom posts: SDK only, not in UIKit. | https://learn.social.plus/social-plus-sdk/social/content-management/posts/overview | 2026-10-05 |
| Audio posts | Lets users post audio files. | SDK iOS/Android/TS only. Not in any UIKit. | https://learn.social.plus/social-plus-sdk/social/content-management/posts/creation/audio-post | 2026-10-05 |
| Mixed media posts | Combines photos, videos and file attachments in one post. | SDK iOS/Android/TS (not Flutter). | https://learn.social.plus/social-plus-sdk/social/content-management/posts/creation/mixed-media-post | 2026-10-05 |
| Post titles and hashtags | Adds an optional title and searchable hashtags to posts. | SDK iOS/Android/TS; UIKit iOS/Android/Web (not RN or Flutter). | https://learn.social.plus/feature-matrix | 2026-10-05 |
| Mentions | Lets users @mention other users in posts, comments and messages. | | https://learn.social.plus/social-plus-sdk/core-concepts/content-handling/mentions | 2026-10-05 |
| Link previews and hyperlinks | Shows a preview for pasted URLs and lets users turn selected text into a hyperlink. | Link previews: all SDKs and UIKits. Creating text hyperlinks: web desktop; mobile UIKits only display them. | https://learn.social.plus/social-plus-sdk/social/content-management/posts/creation/text-post | 2026-10-05 |
| Edit and delete posts | Lets users edit their posts; posts can be soft-deleted (marked deleted) or hard-deleted (removed). | | https://learn.social.plus/social-plus-sdk/social/content-management/posts/moderation/delete-post | 2026-10-05 |
| Pinned and featured posts | Lets admins pin posts in a community or feature them globally. | Pinning is done in the Console (up to 20 pins per community); apps read pinned posts through the SDK. | https://learn.social.plus/social-plus-sdk/social/content-management/posts/moderation/pin-post | 2026-10-05 |
| Post review | Holds new community posts for moderator approval before they appear. | All SDKs and UIKits. | https://learn.social.plus/social-plus-sdk/social/content-management/posts/moderation/post-review | 2026-10-05 |
| Comments and replies | Lets users comment on posts, stories and custom content, reply to comments, and add images to comments. | Multi-level replies: SDK iOS/Android/TS, UIKit iOS/Android/Web (UIKit shows up to 2 levels). GIF comments not available. | https://learn.social.plus/social-plus-sdk/social/content-management/comments/overview | 2026-10-05 |
| Comment review | Holds new and edited comments for moderator approval, with a reviewer queue. | | https://learn.social.plus/social-plus-sdk/social/content-management/comments/moderation/comment-review | 2026-10-05 |
| Reactions | Lets users add named reactions (such as "like") to posts, comments, stories and messages. | Multiple reaction types: SDK iOS/Android/TS, UIKit iOS/Android/Web. | https://learn.social.plus/social-plus-sdk/core-concepts/content-handling/reactions | 2026-10-05 |
| Polls | Lets users create single- or multiple-choice polls with text or image answers, vote, change their vote and close the poll. | 2 to 10 answers; question up to 500 characters; manual close or expiry; a poll cannot be combined with other attachments in the same post. | https://learn.social.plus/use-cases/social/polls-and-interactive-content | 2026-10-05 |
| Stories | Lets users post image and video stories to a community, with optional hyperlink items, comments and reactions; stories expire after 24 hours. | Community stories only (user stories not available). Story stickers, polls and text overlays not available. Up to 10 hyperlink items per story. | https://learn.social.plus/social-plus-sdk/social/content-management/stories/overview | 2026-10-05 |
| Story impressions | Tracks story views, reach and hyperlink clicks. | | https://learn.social.plus/social-plus-sdk/social/content-management/stories/analytics/story-impressions | 2026-10-05 |
| Clips (short-form video) | Lets users post short vertical videos that play in a swipeable clips feed. | Up to 15 minutes and 2 GB per clip. Clips feed: all SDKs; UIKit iOS/Android/Web. | https://learn.social.plus/use-cases/social/short-form-video-clips | 2026-10-05 |
| User, community and global feeds | Returns a user's feed, a community feed and a global (following) feed in chronological order. | All SDKs and UIKits. Standard page size is 20 posts. | https://learn.social.plus/social-plus-sdk/social/discovery-engagement/feed/overview | 2026-10-05 |
| Custom post ranking | Ranks the global feed by a configured blend of engagement and freshness instead of time. | SDK only, not in UIKit. Configuration is adjusted with support. | https://learn.social.plus/social-plus-sdk/social/discovery-engagement/feed/custom-ranking | 2026-10-05 |
| For You feed | Returns a feed ranked by relevance for each user, drawn from joined and public communities, followed users, some exploration posts and live streams. | Network setting that must be enabled. SDK iOS/Android/TS; UIKit iOS/Android/Web. The SDK cannot change the ranking weights. | https://learn.social.plus/social-plus-sdk/social/discovery-engagement/feed/for-you-feed | 2026-10-05 |
| Search (Intelligent Search) | Searches posts by meaning or by hashtag, and searches communities by meaning. | Flutter added in Aug/Sep 2026 (the Feature Matrix still shows Flutter as unsupported). Indexes only posts created after the feature is enabled. | https://learn.social.plus/social-plus-sdk/social/discovery-engagement/search/overview | 2026-10-05 |
| User search | Finds users by display name and lists users with sorting. | Search keyword must be at least 3 characters. | https://learn.social.plus/social-plus-sdk/core-concepts/user-management/user-operations/search-and-query-users | 2026-10-05 |
| Topic-based discovery and Discovery Widget | Shows recommended community posts for a topic set up in the Console on other screens of the app, through the SDK or a UIKit carousel. | Enabled on request. Up to 25 topics. | https://learn.social.plus/analytics-and-moderation/console/management/discovery-widget | 2026-10-05 |
| User profiles | Stores and shows a user's display name, description, avatar and custom metadata. | | https://learn.social.plus/social-plus-sdk/core-concepts/user-management/user-operations/update-user-information | 2026-10-05 |
| Follow and follow requests | Lets users follow and unfollow others, approve or decline follow requests, and see follower and following lists and counts. | All SDKs and UIKits. | https://learn.social.plus/social-plus-sdk/social/user-relationship/overview | 2026-10-05 |
| Blocking | Lets users block and unblock other users and see who they have blocked. | SDK iOS/Android/TS; UIKit iOS/Android/Web/RN (not Flutter). | https://learn.social.plus/social-plus-sdk/social/user-relationship/blocking/block-unblock-user | 2026-10-05 |
| Media galleries | Shows a gallery of the media a user or a community has posted. | All SDKs and UIKits. | https://learn.social.plus/feature-matrix | 2026-10-05 |
| Events | Lets users and admins create virtual (livestream or external link) or in-person events with RSVP, an attendee list, reminders and an event post for discussion. | SDK iOS/Android/TS (not Flutter); UIKit iOS/Android/Web; also created in the Console. | https://learn.social.plus/social-plus-sdk/social/events/overview | 2026-10-05 |
| Content sharing and deep links | Generates shareable links for posts, communities, user profiles and live streams from URL patterns set in the Console. | The customer's app must handle the incoming link and open the right screen. | https://learn.social.plus/analytics-and-moderation/console/settings/deep-link | 2026-10-05 |
| Presence (online status) | Shows whether users or conversation members are online, and how many people are watching a live room. | User and channel presence: iOS and Android only. Room presence: iOS/Android/TS. Presence must be enabled for the network. | https://learn.social.plus/social-plus-sdk/core-concepts/realtime-communication/presence-state/overview | 2026-10-05 |
| Brand account (post as brand) | Lets admins post and comment from a brand account with a verification badge. | Console only; UIKits display brand posts. | https://learn.social.plus/analytics-and-moderation/console/settings/branding | 2026-10-05 |
| Moderator badge | Shows a "Moderator" badge on users with that role. | All SDKs and UIKits. | https://learn.social.plus/feature-matrix | 2026-10-05 |

## Chat

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| Channel types | Provides community (group) channels, conversation channels for 1:1 or small private groups, and live channels for event-style chat. | All SDKs. Creating a conversation with the same members returns the existing one by default. | https://learn.social.plus/social-plus-sdk/chat/conversation-management/channels/create-channel | 2026-10-05 |
| Broadcast channels | Lets only admins or authorized staff post while other members can read. | Set up in the Console. | https://learn.social.plus/analytics-and-moderation/console/chat-management/messaging-management | 2026-10-05 |
| Message types | Lets users send text, image, video, file, audio and custom messages. | Text up to 20,000 characters; up to 5 tags and 100 KB metadata per message; media files up to 1 GB. Audio messages only on SDKs that expose them. | https://learn.social.plus/use-cases/chat/sending-messages | 2026-10-05 |
| Replies (threads) | Lets users reply to a specific message to start a thread. | | https://learn.social.plus/social-plus-sdk/chat/messaging-features/message-creation/reply-to-a-message | 2026-10-05 |
| Edit and delete messages | Lets users edit text and custom messages and delete messages (deleted messages leave a placeholder). | | https://learn.social.plus/social-plus-sdk/chat/messaging-features/messages/edit-and-delete-messages | 2026-10-05 |
| Mentions and reactions in chat | Lets users mention others and react to messages. | | https://learn.social.plus/use-cases/chat/message-reactions-and-replies | 2026-10-05 |
| Unread counts | Shows unread counts per channel and in total. | Platform-specific gaps on TS and Flutter. | https://learn.social.plus/social-plus-sdk/chat/engagement-features/unread-status/channel-unread-count | 2026-10-05 |
| Read and delivery receipts | Marks messages as read or delivered and lists who read or received a message. | Delivery-receipt user lists and receipt sync are not in the Flutter SDK. | https://learn.social.plus/social-plus-sdk/chat/engagement-features/unread-status/message-delivery-status | 2026-10-05 |
| Message previews | Shows the latest message on channel lists. | | https://learn.social.plus/social-plus-sdk/chat/engagement-features/message-preview | 2026-10-05 |
| Channel and message search | Finds channels by name and messages by keyword, with filters such as sender, channel and content type. | All SDKs. | https://learn.social.plus/social-plus-sdk/chat/chat-search | 2026-10-05 |
| Channel membership and governance | Lets users join and leave channels, and lets moderators add or remove members, assign roles, ban members and mute them for a set time. | Banning removes the user and deletes their messages in the channel. | https://learn.social.plus/social-plus-sdk/chat/conversation-management/channels/governance/overview | 2026-10-05 |
| Archive channels | Lets users archive and unarchive channels. | Only where the SDK exposes archive APIs. | https://learn.social.plus/social-plus-sdk/chat/conversation-management/channels/archive-channels | 2026-10-05 |
| Member preview | Shows a short preview of up to 4 channel members. | | https://learn.social.plus/social-plus-sdk/chat/conversation-management/members/preview-members | 2026-10-05 |
| Pin a message in livestream chat | Pins one message to the top of a livestream chat. | Livestream channels only; one pinned message at a time. | https://learn.social.plus/social-plus-sdk/chat/messaging-features/messages/pin-message | 2026-10-05 |
| Message reporting | Lets users flag messages, with predefined reasons. | | https://learn.social.plus/social-plus-sdk/chat/messaging-features/message-flagging | 2026-10-05 |
| Per-user message rate limits | Slows down users who send messages too quickly, without a moderator stepping in. | Configured in network settings. | https://learn.social.plus/use-cases/chat/chat-moderation | 2026-10-05 |

## Video and live streaming

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| Live streaming (rooms) | Lets users and admins create a live room, go live and end the stream; the SDK returns the broadcast credentials the app hands to its media stack (a LiveKit client). | SDK iOS/Android/TS; the Flutter SDK has no room broadcasting API. UIKit iOS/Android/Web/RN (not Flutter). Legacy stream APIs are deprecated. | https://learn.social.plus/social-plus-sdk/video-new/broadcasting/overview | 2026-10-05 |
| Community and user live streams | Posts a live stream to a community feed or a user feed. | All SDKs; UIKit iOS/Android/Web/RN. | https://learn.social.plus/social-plus-sdk/social/content-management/posts/creation/room-post | 2026-10-05 |
| Co-hosted live streams | Lets a host invite co-hosts to broadcast together. | Community streams only. SDK iOS/Android/TS; UIKit iOS/Android/Web. | https://learn.social.plus/social-plus-sdk/video-new/broadcasting/co-host-management | 2026-10-05 |
| Live and recorded playback | Provides live and recorded playback URLs that the app plays in its own video player. | The customer's app owns the player, captions and DRM. | https://learn.social.plus/social-plus-sdk/video-new/playback/overview | 2026-10-05 |
| Recording and replay | Records live streams so they can be watched afterwards. | | https://learn.social.plus/social-plus-sdk/video-new/broadcasting/recorded-playback | 2026-10-05 |
| Live chat and live reactions | Lets viewers chat and send reactions during a stream; chat can be set to read-only. | Community streams only. SDK iOS/Android/TS; UIKit iOS/Android/Web. | https://learn.social.plus/use-cases/social/livestream/live-chat-and-engagement | 2026-10-05 |
| Viewer count | Shows how many people are watching, once a configurable threshold is reached. | SDK iOS/Android/TS; UIKit iOS/Android/Web. | https://learn.social.plus/social-plus-sdk/video-new/broadcasting/viewer-count-config | 2026-10-05 |
| "Live" rings | Shows active live streams in a story-style ring. | SDK iOS/Android/TS; UIKit iOS/Android/Web. | https://learn.social.plus/feature-matrix | 2026-10-05 |
| Livestream analytics | Shows viewers, unique viewers, minutes watched (per stream and per user), chat, reactions and concurrent viewers per stream in the Dashboard, with a viewer-count chart across each stream's timeline and comparison with the previous period. | Not automatic: the app records watch sessions through the SDK (create, update and sync them); without those calls no viewing data is recorded. | https://learn.social.plus/analytics-and-moderation/dashboard-new/livestream-analytics, https://learn.social.plus/social-plus-sdk/video-new/analytics/overview | 2026-10-05 |
| Livestream AI moderation | Samples video frames and audio during a stream, flags streams for review and ends streams that pass a set threshold. | Must be enabled. | https://learn.social.plus/analytics-and-moderation/console/moderation/livestream-moderation | 2026-10-05 |
| Live stream management in the Console | Lets admins create direct streams, monitor broadcast status, tag products and see moderation results. | Console streams are direct streams; co-streams start from the app. Title up to 150 characters; thumbnail up to 2 MB. | https://learn.social.plus/analytics-and-moderation/console/management/live-stream-management-new | 2026-10-05 |
| Multi-stream posts (legacy) | Lets admins create a parent stream with up to two child streams for device-specific views. | Legacy live stream management only. | https://learn.social.plus/analytics-and-moderation/console/management/live-stream-management | 2026-10-05 |
| Picture-in-picture | Keeps a live stream playing in a small floating window when the viewer leaves the player. | UIKit iOS and Android. | https://learn.social.plus/uikit/components/social/livestream | 2026-10-05 |
| Video upload and transcoding | Uploads videos and serves generated versions (original, 1080p, 720p, 480p, 360p where available). | Size and duration limits differ across docs pages: do not state them. | https://learn.social.plus/social-plus-sdk/core-concepts/content-handling/files-images-and-videos/video-handling | 2026-10-05 |

## Monetization: Commerce and Sponsored Content

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| Product Catalogue | Lets admins add products manually or by CSV upload and mark them active or archived. | Console. CSV files up to 15 MB. | https://learn.social.plus/analytics-and-moderation/console/product-management/overview | 2026-10-05 |
| Product tagging in posts | Tags catalogue products in post text and on images or videos; users open the product link in an in-app browser. | Up to 20 products per post and 5 per media item. SDK iOS/Android; UIKit iOS/Android/Web. Not available in comments. | https://learn.social.plus/use-cases/social/product-tagging-and-social-commerce | 2026-10-05 |
| Product tagging in live streams | Tags up to 20 products on a live stream and pins featured products for viewers. | SDK iOS/Android; UIKit iOS/Android/Web. | https://learn.social.plus/use-cases/social/livestream/product-tagging | 2026-10-05 |
| Sponsored Content (Premium Ads) | Lets the customer's admins create advertiser profiles and ads that appear as native posts, comments and stories, paced by frequency or time window. | Ads are created by the customer, not sourced by social.plus. Platform coverage differs across docs pages: do not state it. | https://learn.social.plus/analytics-and-moderation/console/premium-ads/README | 2026-10-05 |
| Ad impression and click tracking | Records ad impressions, clicks and reach. | | https://learn.social.plus/social-plus-sdk/core-concepts/content-handling/ads | 2026-10-05 |

## Moderation

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| User reports (flagging) | Lets users report posts, comments, messages, live stream chat and other users, with predefined reasons. | Predefined reasons for posts and comments: SDK iOS/Android/TS. Reporting stories is marked "Not Available" (docs pages disagree). | https://learn.social.plus/social-plus-sdk/social/content-management/moderation/content-flagging | 2026-10-05 |
| Moderation Feed | Collects flagged posts, comments, messages and user profiles in one Console queue to review and act on. | | https://learn.social.plus/analytics-and-moderation/console/user-and-content-management/mod-feed | 2026-10-05 |
| AI pre-moderation (images) | Blocks uploaded images before they are published when they score above set thresholds for nudity, suggestive content, violence or disturbing content. | Images only today (text and video "coming soon"). Enabled on request. | https://learn.social.plus/analytics-and-moderation/console/ai-content-moderation | 2026-10-05 |
| AI post-moderation | Scans published text, images and video and flags or removes content above set thresholds. | Text categories: hate, sexual, violence, self-harm. Enabled on request. Flat-rate packages have monthly allowances; when one runs out, Budget Guard switches that feature to rules-based moderation. | https://learn.social.plus/analytics-and-moderation/social+-portal/ai-moderation-usage | 2026-10-05 |
| AI user profile moderation | Flags display names, descriptions and avatars that break policy so an admin can review them. | Flag-only, never auto-deletes. Avatars set by external URL are not scanned. | https://learn.social.plus/analytics-and-moderation/console/ai-user-profile-moderation | 2026-10-05 |
| Admin profile reset | Lets admins reset a user's display name, avatar or description from the Console. | | https://learn.social.plus/analytics-and-moderation/console/ai-user-profile-moderation | 2026-10-05 |
| Blocklist and allowlist | Blocks listed words or phrases (profanity filter) and restricts links to allowed domains. | Exact-word or partial matching. | https://learn.social.plus/social-plus-sdk/technical-faq | 2026-10-05 |
| PII detection | Detects personal data such as emails, phone numbers and IP addresses in text and helps apps redact it. | Enabled server-side. SDK helpers on iOS and Android only. | https://learn.social.plus/social-plus-sdk/core-concepts/safety-privacy/pii-detection | 2026-10-05 |
| Hide posts and comments | Lets moderators hide content from public view without deleting it. | All SDKs and UIKits. | https://learn.social.plus/analytics-and-moderation/console/social-management/social-management/posts | 2026-10-05 |
| Ban and mute | Lets moderators ban users from a channel, a community or the whole network, and mute users in a channel or across the network. | A global ban can take up to 30 seconds to disconnect a user. A global mute can be set to expire. | https://learn.social.plus/analytics-and-moderation/console/user-and-content-management/global-mute | 2026-10-05 |
| Roles and permissions | Assigns roles such as moderator, and custom roles with chosen permissions, at community, channel and network level. | | https://learn.social.plus/use-cases/social/roles-permissions-and-governance | 2026-10-05 |
| Edit user content with history | Lets moderators edit posts and comments in the Console while keeping a change history. | Shows up to 10 recent edits plus the original. | https://learn.social.plus/analytics-and-moderation/console/moderation/edit-content-history | 2026-10-05 |
| User history | Shows a user's activity, flags, bans and moderation history in one Console view. | | https://learn.social.plus/analytics-and-moderation/console/user-and-content-management/user-social-history | 2026-10-05 |
| Moderation activity reports | Exports a CSV audit trail of moderation actions, including AI actions. | Must be enabled; no data from before enablement. | https://learn.social.plus/analytics-and-moderation/overview | 2026-10-05 |

Pre-hook events (custom server-side checks before content is accepted) are listed under APIs and webhooks.

## Analytics, Console and Portal

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| Console | Web admin tool for each application, used to moderate content, manage users, communities and channels, and change settings. | | https://learn.social.plus/analytics-and-moderation/console/overview | 2026-10-05 |
| Portal | Organization-level tool to create applications, manage team access and billing, and view usage. | Called "Admin Portal" in the docs. Up to 50 team members per organization. Sign-in by email or SAML SSO. The application cap differs across docs pages: do not state it. | https://learn.social.plus/analytics-and-moderation/social+-portal/README | 2026-10-05 |
| Admin on the go | Mobile-browser version of the Console for reviewing, moderating and publishing content. | Web app at go.social.plus; same accounts and permissions as the Console. | https://learn.social.plus/analytics-and-moderation/admin-on-the-go/overview | 2026-10-05 |
| Admin access control | Assigns admins a system role (Admin, Community Manager, Moderator, Content Creator, Brand Partner) or a custom role, limited to chosen communities. | | https://learn.social.plus/analytics-and-moderation/console/management/admin-access-control | 2026-10-05 |
| Analytics Dashboard | Shows active and new users, content published, monthly active users, concurrent connections and top communities, with date filters and CSV export per widget. | Redesigned in Aug 2026; the legacy view is still available. | https://learn.social.plus/analytics-and-moderation/dashboard-new/overview | 2026-10-05 |
| Chat analytics | Shows message volume, participation, channel activity and flagged-message rates. | | https://learn.social.plus/analytics-and-moderation/social+-portal/dashboard/chat-analytics | 2026-10-05 |
| Post and content analytics | Shows impressions, reach and engagement per post and over time. | | https://learn.social.plus/analytics-and-moderation/social+-portal/dashboard/post-analytics | 2026-10-05 |
| Social Insights | Surfaces topics, sentiment, search trends and AI research answers from community conversations. | Enabled on request. | https://learn.social.plus/analytics-and-moderation/social+-portal/dashboard/social-insights | 2026-10-05 |
| Sentiment Analysis | Detects topics, classifies sentiment and summarizes threads; admins can set custom keywords and categories and override results. | Monthly credit allocation. | https://learn.social.plus/analytics-and-moderation/dashboard-new/sentiment-analysis | 2026-10-05 |
| User Insights | Scores each user's contribution level and content quality in the Console. | Admin-facing only. Content quality labels must be enabled and cover text only. | https://learn.social.plus/analytics-and-moderation/console/user-and-content-management/user-insights | 2026-10-05 |
| User tags | Lets admins create tags, assign them to users and filter users by tag. | Tag name up to 20 characters; filter by up to 10 tags at once. | https://learn.social.plus/analytics-and-moderation/console/user-and-content-management/tag-management | 2026-10-05 |
| Raw data export | Downloads CSV files of posts, comments, reactions, reach and impressions. | Scheduled exports are "on roadmap". | https://learn.social.plus/analytics-and-moderation/social+-portal/dashboard/raw-data-export | 2026-10-05 |
| Scheduled posts and stories | Lets admins schedule posts and stories to publish later. | Console (and API) only. Stories: at least 1 hour and up to 30 days ahead. | https://learn.social.plus/analytics-and-moderation/console/social-management/stories | 2026-10-05 |

## Notifications

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| Push notifications | Sends push notifications for chat, community, story, live stream and event activity through APNs, FCM or Baidu. | All SDKs and UIKits. Configured in the Console; one active certificate per platform. | https://learn.social.plus/analytics-and-moderation/console/settings/integrations | 2026-10-05 |
| Notification settings | Lets users choose which push notifications they get for their account, a channel or a community. | | https://learn.social.plus/social-plus-sdk/core-concepts/realtime-communication/push-notifications/settings/overview | 2026-10-05 |
| Push events and message templates | Lets admins choose which events send a push and edit the message text. | | https://learn.social.plus/analytics-and-moderation/console/settings/integrations | 2026-10-05 |
| Notification tray | Provides an in-app notification inbox with seen and unseen states. | SDK iOS/Android/TS; UIKit iOS/Android/Web/RN (not Flutter). | https://learn.social.plus/social-plus-sdk/social/discovery-engagement/notifications/overview | 2026-10-05 |
| Event and live stream notifications | Reminds users who RSVP'd before an event starts and notifies followers when a stream starts; admins can turn off standalone live stream pushes network-wide. | | https://learn.social.plus/analytics-and-moderation/console/settings/integrations | 2026-10-05 |

## UIKit

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| UIKit components | Prebuilt, customizable UI components for chat and social features. | iOS, Android, Web (React), RN and Flutter; coverage differs per feature (see the Feature Matrix). | https://learn.social.plus/uikit/overview | 2026-10-05 |
| Chat UIKit | Provides a recent chats list, 1:1 and group conversations, live chat and chat search screens. | | https://learn.social.plus/uikit/components/chat/overview | 2026-10-05 |
| Social UIKit | Provides feeds, posts, communities, comments and reactions, stories, clips, live stream, events, user profiles and moderation screens. | | https://learn.social.plus/uikit/components/social/overview | 2026-10-05 |
| Open source (fork and extend) | Publishes UIKit source on GitHub so teams can fork it and change any part. | | https://learn.social.plus/uikit/customization/advanced-customization | 2026-10-05 |
| Dynamic UI | Changes theme colors from a remote configuration without an app release. | Colors today; typography and spacing are on the roadmap. | https://learn.social.plus/uikit/customization/dynamic-ui | 2026-10-05 |
| Component styling | Overrides styles and theme values per component. | | https://learn.social.plus/uikit/customization/component-styling | 2026-10-05 |
| Light and dark themes | Supports light and dark themes. | Runtime theme switching in Flutter UIKit; dark mode for chat UIKit on iOS/Android (Aug 2026) and RN/Flutter (Sep 2026). | https://learn.social.plus/uikit/customization/set-preferred-theme | 2026-10-05 |
| Localization | Lets teams add languages or override UI text without forking. | English is the only built-in language. | https://learn.social.plus/uikit/customization/localization | 2026-10-05 |
| UI Kit (Figma) | Figma design files for the social and chat UI. | Linked from the docs FAQ; requested through forms on social.plus/social/uikit and /chat/uikit. | https://learn.social.plus/social-plus-sdk/technical-faq | 2026-10-05 |

## SDKs and platforms

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| Client SDKs | Native SDKs for iOS (Swift), Android (Kotlin/Java), TypeScript (web) and Flutter. | iOS also has an Objective-C bridge for login. React Native uses the TypeScript SDK with platform guidance. | https://learn.social.plus/social-plus-sdk/overview | 2026-10-05 |
| Web framework compatibility | The TypeScript SDK works with React, Next.js, Vue, Angular, Svelte and other web frameworks. | Modern browsers; Internet Explorer 11 not supported. | https://learn.social.plus/social-plus-sdk/getting-started/platform-setup/web/web-quick-start | 2026-10-05 |
| Platform coverage differences | Some features are missing on some platforms; Flutter currently lacks events, room-based live streaming, presence and the notification tray. | Always check the Feature Matrix before saying "on every platform". | https://learn.social.plus/feature-matrix | 2026-10-05 |
| Real-time data | Keeps app screens in sync through live objects, live collections and real-time event subscriptions. | | https://learn.social.plus/social-plus-sdk/core-concepts/realtime-communication/live-objects-collections/overview | 2026-10-05 |
| File, image and video handling | Uploads files, images and videos and serves resized images and transcoded video. | Images up to 1 GB, up to 10 per post. Format and size limits differ across docs pages: do not state them. | https://learn.social.plus/social-plus-sdk/core-concepts/content-handling/files-images-and-videos/image-handling | 2026-10-05 |
| Local database encryption | Encrypts the SDK's local database on Android. | Android; may slow local reads and writes by up to 15%. | https://learn.social.plus/social-plus-sdk/getting-started/platform-setup/mobile/android-quick-start | 2026-10-05 |
| API rate limit | Limits each user to 100 requests per 5 seconds across all their devices. | | https://learn.social.plus/social-plus-sdk/technical-faq | 2026-10-05 |
| Changelogs | Publishes versioned changelogs for every SDK and UIKit platform. | | https://learn.social.plus/social-plus-sdk/changelogs/ios-sdk-changelog | 2026-10-05 |

## Users and access

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| User identity | Identifies users by a stable user ID from the customer's own system; credentials and private profile data stay with the customer. | | https://learn.social.plus/social-plus-sdk/core-concepts/user-management/user-identity | 2026-10-05 |
| Authentication and Secure Mode | Signs users in with the application's API key; Secure Mode adds a short-lived token issued by the customer's server, optionally with mTLS. | Secure Mode auth tokens are valid for 10 minutes. | https://learn.social.plus/analytics-and-moderation/console/settings/security | 2026-10-05 |
| Visitor mode | Lets anonymous users browse public content read-only without signing in, and lets search-engine bots index it. | Enabled on request. Visitor MAUs are counted separately; visitors above a monthly fair-use threshold count as signed-in usage. | https://learn.social.plus/social-plus-sdk/getting-started/visitor-mode | 2026-10-05 |
| Permission checks | Lets the app check whether the current user may perform a protected action. | | https://learn.social.plus/social-plus-sdk/core-concepts/user-management/roles-permissions | 2026-10-05 |
| User deletion | Lets admins permanently delete users, one at a time or in bulk jobs. | Server-side only, not from client SDKs. Cannot be undone. | https://learn.social.plus/social-plus-sdk/core-concepts/user-management/user-operations/delete-user | 2026-10-05 |
| Last activity report | Exports each user's last read and write time to spot inactive accounts. | | https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/generate-user-last-activity-report | 2026-10-05 |

## APIs and webhooks

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| REST APIs | Server-to-server APIs for administration, moderation, automation and data access. | Admin token required; regional endpoints. | https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/README | 2026-10-05 |
| Admin tokens | Lets admins generate, rotate and revoke Console admin tokens. | Tokens expire after 1 year by default. | https://learn.social.plus/analytics-and-moderation/console/settings/admin-tokens | 2026-10-05 |
| Webhook events | Sends event notifications (posts, comments, messages, users, communities, follows, files, polls, live streams) to the customer's endpoint as they happen. | Docs say Private Beta, enabled through support in about 5 business days. Up to 10 webhooks per network; 1.5-second timeout; signed payloads. | https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/webhook-event | 2026-10-05 |
| Pre-hook events | Lets the customer's server allow, change or block actions such as sending a message or creating a post before social.plus processes them. | Max plan only. | https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/pre-hook-event | 2026-10-05 |
| Network settings API | Changes network-wide settings with an admin token. | | https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/network-settings | 2026-10-05 |
| First-party data export | Downloads reports of recent engagement data, including sentiment fields, through an API. | | https://learn.social.plus/api-reference/admin/get-first-party-data-export | 2026-10-05 |
| Data model references | Documents the chat and social data entities, including guidance for importing data. | | https://learn.social.plus/api-reference/social-data-model | 2026-10-05 |

## AI tools for teams and developers

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| Agentry | Lets authorized team members ask questions about their network's engagement data in plain language from ChatGPT, Claude or another MCP-capable AI app. | Preview, enabled on request. Read-only, limited to the customer's own network, roughly the last 90 days. | https://learn.social.plus/ai/agentry/overview | 2026-10-05 |
| Documentation MCP server | Gives AI coding tools direct access to the public social.plus docs. | Public endpoint, no authentication. | https://learn.social.plus/ai/docs-mcp-server | 2026-10-05 |
| Vise | Local CLI and coding-agent skill that plans, checks and documents social.plus SDK integrations built by AI coding agents. | Runs on the developer's machine; needs Node.js 20 or newer. | https://learn.social.plus/ai/vise/overview | 2026-10-05 |

## Security, data and hosting

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Source (docs URL) | Checked |
|---|---|---|---|---|
| Managed hosting | social.plus hosts the backend services behind the SDK features. | | https://learn.social.plus/social-plus-sdk/overview | 2026-10-05 |
| Regions and data residency | Runs each application in the US, EU or SG region, chosen at creation. | The region cannot be changed later. | https://learn.social.plus/analytics-and-moderation/social+-portal/application-management | 2026-10-05 |
| Separate applications | Lets an organization run separate applications for environments or to isolate data. | Applications cannot be deleted, only renamed. The application cap differs across docs pages: do not state it. | https://learn.social.plus/analytics-and-moderation/social+-portal/application-management | 2026-10-05 |
| SAML SSO for admins | Lets admins sign in to the Portal with SAML single sign-on. | | https://learn.social.plus/analytics-and-moderation/social+-portal/getting-started | 2026-10-05 |
| Data boundary | Keeps credentials, email and private profile data in the customer's system; social.plus stores only the social profile fields the SDK needs. | | https://learn.social.plus/social-plus-sdk/core-concepts/user-management/overview | 2026-10-05 |

Security certifications, encryption standards and uptime figures are not listed: the docs do not confirm them. Confirm with the product owner before using any of them.

## Recently added

Releases from the last 12 months (since October 2025). "Released" is the month of the social.plus monthly product update that announced the feature; September 2026 items have no monthly update yet, so they carry the release-note date. Release notes with a 4 February 2026 date were backfilled when the release-note collection launched; their real dates come from the monthly updates. Product update index: https://www.social.plus/product-updates

| Capability | What it does (one plain line) | Platforms / limits worth knowing | Released | Source (docs URL) | Checked |
|---|---|---|---|---|---|
| Visitor mode | Lets anonymous users browse public content read-only without signing in. | Enabled on request. | Oct 2025 | https://learn.social.plus/social-plus-sdk/getting-started/visitor-mode | 2026-10-05 |
| User Insights (contribution and content quality) | Scores users' contribution level and content quality in the Console. | Admin-facing. | Oct 2025 | https://learn.social.plus/analytics-and-moderation/console/user-and-content-management/user-insights | 2026-10-05 |
| Flutter Chat UIKit additions | Added message and chat search, URL previews, mentions and moderator mute to the Flutter Chat UIKit. | Flutter UIKit. | Oct 2025 | https://learn.social.plus/uikit/changelogs/flutter-uikit-changelog | 2026-10-05 |
| Multi-stream posts in the Console | Lets admins create parent and child streams for device-specific views. | Legacy live stream management. | Oct 2025 | https://learn.social.plus/analytics-and-moderation/console/management/live-stream-management | 2026-10-05 |
| Inactive user list | Lets admins download all users with their last activity date. | | Oct 2025 | https://learn.social.plus/analytics-and-moderation/social+-apis-and-services/generate-user-last-activity-report | 2026-10-05 |
| Livestream events and co-streaming | Added scheduled livestream events with RSVP and reminders, co-streaming, public live streams, "Live" rings, a watching-now count and live chat moderation in the Console and UIKit. | See Video rows for platform limits. | Nov-Dec 2025 | https://learn.social.plus/use-cases/social/livestream/overview | 2026-10-05 |
| Mixed media posts | Combines photos, videos and files in one post. | SDK iOS/Android/TS. | Nov-Dec 2025 | https://learn.social.plus/social-plus-sdk/social/content-management/posts/creation/mixed-media-post | 2026-10-05 |
| Hyperlinks in posts and comments | Lets users link selected text and remove URL previews. | Creation on web desktop; mobile displays. | Nov-Dec 2025 | https://learn.social.plus/feature-matrix | 2026-10-05 |
| Livestream analytics dashboard | Shows viewers, engagement, watch time and retention per stream. | | Jan 2026 | https://learn.social.plus/analytics-and-moderation/dashboard-new/livestream-analytics | 2026-10-05 |
| Content performance widgets | Shows impressions, reach and engagement trends per post. | | Jan 2026 | https://learn.social.plus/analytics-and-moderation/social+-portal/dashboard/post-analytics | 2026-10-05 |
| Network-level livestream push control | Lets admins turn off pushes for standalone live streams. | | Jan 2026 | https://learn.social.plus/analytics-and-moderation/console/settings/integrations | 2026-10-05 |
| Events in the Console | Lets admins create and manage livestream, external-link and in-person events. | | Feb 2026 | https://learn.social.plus/analytics-and-moderation/console/management/events-management | 2026-10-05 |
| User tags in the Console | Lets admins create, assign and filter by user tags. | | Feb 2026 | https://learn.social.plus/analytics-and-moderation/console/user-and-content-management/tag-management | 2026-10-05 |
| Product Catalogue and tagging in posts | Added a product catalogue and product tags in posts. | SDK iOS/Android; UIKit iOS/Android/Web. | Mar 2026 | https://learn.social.plus/analytics-and-moderation/console/product-management/overview | 2026-10-05 |
| Product tagging and pinning in live streams | Tags up to 20 products on a live stream and pins them as overlays. | SDK iOS/Android; UIKit iOS/Android/Web. | Mar 2026 | https://learn.social.plus/use-cases/social/livestream/product-tagging | 2026-10-05 |
| Room-based live stream management | Lets admins create, manage and monitor live streams in the Console. | | Mar 2026 | https://learn.social.plus/analytics-and-moderation/console/management/live-stream-management-new | 2026-10-05 |
| Multi-level comment replies | Supports two levels of nested replies in posts and feeds. | | Apr 2026 | https://learn.social.plus/uikit/components/social/comments-reactions | 2026-10-05 |
| AI profile moderation and admin reset | Flags inappropriate profile photos, names and descriptions; admins can reset them. | | Apr 2026 | https://learn.social.plus/analytics-and-moderation/console/ai-user-profile-moderation | 2026-10-05 |
| Documentation MCP server | Connects AI coding tools to the social.plus docs. | | Apr-May 2026 | https://learn.social.plus/ai/docs-mcp-server | 2026-10-05 |
| Post views CSV via API | Generates a CSV of post views and impressions. | Refreshed every 3 hours, rolling 7 days (per the product update). | Apr 2026 | https://learn.social.plus/social-plus-sdk/social/content-management/posts/analytics/post-impressions | 2026-10-05 |
| Auto-generated live stream thumbnail | Creates a thumbnail for the replay when none was set. | | Apr 2026 | https://learn.social.plus/analytics-and-moderation/console/management/live-stream-management-new | 2026-10-05 |
| Sentiment configuration | Lets admins set custom sentiment keywords and categories, override results per post, cover all comments and filter by user tags. | | May 2026 | https://learn.social.plus/analytics-and-moderation/dashboard-new/sentiment-analysis | 2026-10-05 |
| UIKit localization API | Lets teams add languages or override UI text without forking. | English built in. | May 2026 | https://learn.social.plus/uikit/customization/localization | 2026-10-05 |
| AI Moderation allowances and Budget Guard | Tracks monthly AI moderation allowances and falls back to rules-based moderation when one runs out. | Flat-rate packages. | Jun 2026 | https://learn.social.plus/analytics-and-moderation/social+-portal/ai-moderation-usage | 2026-10-05 |
| Visitor usage limits | Counts visitors above a monthly fair-use threshold as signed-in usage. | | Jun 2026 | https://learn.social.plus/social-plus-sdk/getting-started/visitor-mode | 2026-10-05 |
| Hide posts and comments | Lets moderators hide content without deleting it. | | Jun 2026 | https://learn.social.plus/analytics-and-moderation/console/social-management/social-management/posts | 2026-10-05 |
| Community tags | Tags communities by topic for filtering and search. | iOS and Android SDK. | Jun 2026 | https://learn.social.plus/social-plus-sdk/social/communities-spaces/discovery/query-communities | 2026-10-05 |
| For You feed | Adds a relevance-ranked feed next to the Following feed. | Must be enabled; SDK iOS/Android/TS, UIKit iOS/Android/Web. | Jul 2026 | https://learn.social.plus/social-plus-sdk/social/discovery-engagement/feed/for-you-feed | 2026-10-05 |
| Vise | Gives AI coding agents a checked workflow for social.plus SDK integrations. | | Jul 2026 | https://learn.social.plus/ai/vise/overview | 2026-10-05 |
| Admin on the go | Mobile-browser Console for community management. | | Jul 2026 | https://learn.social.plus/analytics-and-moderation/admin-on-the-go/overview | 2026-10-05 |
| Shareable event links | Lets hosts copy a link that opens the event page, using the Console deep-link setup. | | Jul 2026 | https://learn.social.plus/analytics-and-moderation/console/settings/deep-link | 2026-10-05 |
| 1:1 chat in iOS and Android UIKit | Lets users start direct conversations without a group chat. | | Jul 2026 | https://learn.social.plus/uikit/components/chat/conversation-chat | 2026-10-05 |
| Visitor mode in React Native UIKit | Adds visitor mode to the RN UIKit. | | Jul 2026 | https://learn.social.plus/uikit/getting-started/visitor-access | 2026-10-05 |
| Analytics Dashboard redesign | New Overview, Users, Content and Communities pages with CSV export per widget. | Legacy view still available. | Aug 2026 | https://learn.social.plus/analytics-and-moderation/dashboard-new/overview | 2026-10-05 |
| Event pushes, pinned and featured event posts | Lets admins send a push when creating an event and pin or feature event posts. | | Aug 2026 | https://learn.social.plus/analytics-and-moderation/console/management/events-management | 2026-10-05 |
| Profile reports with reasons | Lets users report profiles with a reason and comment; moderators see context and reset history. | | Aug 2026 | https://learn.social.plus/use-cases/social/user-profile-moderation | 2026-10-05 |
| Intelligent Search on Flutter | Adds meaning-based post and community search to the Flutter SDK and UIKit. | | Aug 2026 | https://learn.social.plus/social-plus-sdk/social/discovery-engagement/search/overview | 2026-10-05 |
| Dark mode in chat UIKit | Adds dark mode to the chat UIKit. | iOS/Android (Aug 2026), RN and Flutter (29 Sep 2026). | Aug-Sep 2026 | https://learn.social.plus/uikit/customization/set-preferred-theme | 2026-10-05 |
| Agentry | Lets teams ask questions about their engagement data in AI apps. | Preview. | 28 Sep 2026 | https://learn.social.plus/ai/agentry/overview | 2026-10-05 |
| Discovery Widget | Shows topic-based community posts on other screens of the app. | Enabled on request; up to 25 topics. | 29 Sep 2026 | https://learn.social.plus/uikit/components/social/discovery-widget | 2026-10-05 |
| Pin messages in livestream chat | Pins one message at the top of a livestream chat. | Livestream channels only. | 29 Sep 2026 | https://learn.social.plus/social-plus-sdk/chat/messaging-features/messages/pin-message | 2026-10-05 |
| Global mute | Stops a user posting anywhere on the network while they can still sign in and read. | Can expire. | 22 Sep 2026 | https://learn.social.plus/analytics-and-moderation/console/user-and-content-management/global-mute | 2026-10-05 |
| Direct profile reset | Lets admins clear a user's avatar, bio or username without an existing report. | | 22 Sep 2026 | https://learn.social.plus/analytics-and-moderation/console/ai-user-profile-moderation | 2026-10-05 |
| Comment approval | Holds comments and replies for review before others see them. | | 21 Sep 2026 | https://learn.social.plus/social-plus-sdk/social/content-management/comments/moderation/comment-review | 2026-10-05 |
| Livestream picture-in-picture | Keeps a live stream playing in a floating window. | UIKit iOS and Android. | 11 Sep 2026 | https://learn.social.plus/uikit/components/social/livestream | 2026-10-05 |
| Viewer count threshold | Lets admins set when the viewer count appears. | | 11 Sep 2026 | https://learn.social.plus/social-plus-sdk/video-new/broadcasting/viewer-count-config | 2026-10-05 |

## Outside social.plus scope (do not attribute)

Things writers often attach to an engagement or community platform. None of them is in the docs. Never write or imply that social.plus offers them. The second column lists the words the compliance check looks for; add words when a new wrong claim slips through. Where a closer real capability exists, write about that instead, using its row above. "Customer could build" means the SDK or webhooks make it possible for the customer's own engineers; social.plus does not ship it, so never present it as a social.plus feature.

| Topic | Words the check looks for | Status | Closest real capability (what you may say instead) |
|---|---|---|---|
| Payments and wallets | payment processing, process payments, processes payments, payment gateway, in-app payments, in-app wallet, wallet feature, money transfer | Not in the docs as of 2026-10-05. | None. Product tags link out to the brand's own product page. |
| Paid subscriptions, paywalls, in-app purchases | paywall, in-app purchase, paid subscription, subscription billing | Not in the docs as of 2026-10-05. The monetization page mentions subscriber-only groups (awaiting product-owner confirmation). | Private communities, roles and user tags can restrict access; billing stays in the customer's own systems. |
| KYC and identity verification | kyc, identity verification, verify identity, verifies identity, verify the identity, know your customer | Not in the docs as of 2026-10-05. | None. The customer's app owns identity; social.plus receives a user ID. The brand account badge and "Official" community badge are not identity verification. |
| Biometric authentication | biometric, fingerprint, facial recognition, face id, face scan | Not in the docs as of 2026-10-05. | Authentication runs through the customer's login, with optional Secure Mode tokens. |
| Budgeting or financial tools | budgeting, budget tracking, budget tool, spending insights, expense tracking, financial planning | Not in the docs as of 2026-10-05. | None. ("Budget Guard" is an AI moderation usage control for admins, not an end-user tool.) |
| Loyalty points and rewards | loyalty program, loyalty points, reward points, cashback | Not in the docs as of 2026-10-05. | None for users. User Insights scores contribution for admins only; user tags can mark members for the customer's own programs. |
| Gamification (badges, streaks, leaderboards, points, achievements) | gamification, gamified, leaderboard, streak, achievement badge, xp points | Not in the docs as of 2026-10-05. | Polls and reactions exist; gamification does not. Only role and verification badges exist ("Moderator", "Official", brand account). Leaderboards exist only as admin analytics tables (top communities). Customer could build game mechanics with custom posts, metadata and webhooks. |
| AI support chatbots for end users | chatbot, support bot, ai support agent, virtual assistant | Not in the docs as of 2026-10-05. The pricing page lists a "Chatbots" add-on (awaiting product-owner confirmation): do not attribute until confirmed. | Agentry answers admins' questions about engagement data; it is not a user-facing chatbot. "Bot" sessions in visitor mode are search-engine crawlers. |
| CRM and marketing automation | built-in crm, crm features, marketing automation | Not in the docs as of 2026-10-05; positioning says social.plus is not a CRM or marketing automation tool. | Webhooks can send events to the customer's CRM (customer could build). |
| Email marketing or email notifications | email marketing, email campaign, email notification | Not in the docs as of 2026-10-05. | Push notifications and the in-app notification tray. Customer could trigger emails from webhooks. |
| Ad serving, ad network, programmatic ads | ad network, ad serving, programmatic advertising, programmatic ads, ad exchange | Not in the docs as of 2026-10-05; social.plus does not sell media or bring advertisers. | Sponsored Content: the customer's admins place their own or partners' ads in feeds, comments and stories. |
| Video calling and voice calling (1:1 or group) | video call, voice call, video calling, voice calling, audio call | Not in the docs as of 2026-10-05. | Live streaming with co-hosts; video and audio messages in chat. |
| E-commerce store (cart, checkout, orders) | shopping cart, checkout, order management, e-commerce store, online store | Not in the docs as of 2026-10-05. | Product Catalogue and product tagging in posts and live streams. |
| Standalone product analytics for the whole app | app-wide analytics, full product analytics, product analytics suite | Not in the docs as of 2026-10-05; positioning says social.plus is not a standalone analytics suite. | Analytics on social.plus features (users, content, chat, live streams) in the Dashboard. |
| Typing indicators | typing indicator | The docs say the SDK does not expose typing-indicator state. | Presence (online status) on iOS and Android; read and delivery receipts. |
| End-user message translation | message translation, translate messages, auto-translation, automatic translation, real-time translation | Not in the docs as of 2026-10-05. | UIKit localization translates the interface text, not user messages. (A moderator translation tool is awaiting product-owner confirmation.) |
| End-to-end encrypted messaging | end-to-end encryption, end-to-end encrypted, e2ee | Not in the docs as of 2026-10-05. | Secure Mode and mTLS for authentication (encryption claims are awaiting product-owner confirmation). |
| GIF uploads and sticker packs | gif upload, gif keyboard, sticker pack | GIF upload is "not supported" and GIF comments "not available" per the docs. | Reactions; image messages and comments. |
| Recommended follows ("people you may know") | people you may know, follow suggestions, suggested follows, recommended follows | Marked "Not Available" in the Feature Matrix. | Recommended and trending communities; user search. |
| Bookmarks, saved posts and reposts | bookmark, saved posts, save posts, repost, reposting, reshare | Not in the docs; the docs FAQ lists metadata workarounds the customer would build. | Content sharing links (the website's "share internally" claim is awaiting product-owner confirmation). |
| Stories on user profiles; story stickers, polls and text overlays | profile stories, story stickers, story polls, text overlays | Marked "Not Available" in the Feature Matrix. | Community stories with hyperlink items, comments and reactions. |
| Comment ranking and comment locking | comment ranking, lock comments, comment locking, locked comments | Marked "Not Available" in the Feature Matrix. | Comment review and hiding comments. |
| Self-hosted or on-premise deployment | self-hosted, on-premise, on-premises, on-prem | Not in the docs as of 2026-10-05; the docs describe social.plus-hosted infrastructure. | Choice of US, EU or SG region. |
| Game-engine SDKs (Unity, Unreal) | unity sdk, unreal sdk, unity plugin, unreal engine | Not in the docs as of 2026-10-05. | iOS, Android, TypeScript and Flutter SDKs. |
| Scheduled data exports | scheduled export, scheduled data export, automated export | Described as "on roadmap" in the docs. | Manual CSV exports from the Dashboard; first-party data export API. |
