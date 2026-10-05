#!/usr/bin/env python3
"""Tests for product_claims.py (run: python3 scripts/product_claims_test.py). Uses its own small scope table,
so it does not depend on the contents of messaging/product-capabilities.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from product_claims import check_text, load_scope  # noqa: E402

SCOPE = [("Payments and wallets", ["payment", "wallet"]), ("Biometric authentication", ["biometric", "fingerprint"]),
         ("Gamification", ["gamification", "leaderboard"])]
CASES = [
    ("names social.plus + outside-scope word", "# T\n\nsocial.plus handles payments for your app.\n", 1),
    ("negated sentence is fine", "# T\n\nsocial.plus does not process payments; use your provider.\n", 0),
    ("product link attributes", "# T\n\nOur [chat](https://www.social.plus/chat) supports wallets.\n", 1),
    ("claim spread over the paragraph is a WARN, not a FAIL", "# T\n\nBiometrics and gamification keep users. The [product overview](https://www.social.plus/product) covers how these pieces fit together.\n", 0),
    ("blog link does not attribute", "# T\n\nRead our [post](https://www.social.plus/blog/x) about biometrics.\n", 0),
    ("no social.plus, no claim", "# T\n\nBiometrics matter for banks.\n", 0),
    ("disclosure line does not attribute", "# T\n\nWe looked at banking, wallet and investing apps. Disclosure: social.plus publishes this blog.\n", 0),
    ("table rows are separate units", "# T\n\n| App | Feature |\n|---|---|\n| Strava | leaderboards |\n| social.plus | [chat](https://www.social.plus/chat) |\n", 0),
    ("'instead of' is not a negation", "# T\n\nAdd leaderboards through social.plus instead of building them.\n", 1),
    ("another company's feature in an attributing paragraph is a WARN", "# T\n\nStrava built leaderboards. The same patterns are available through social.plus.\n", 0),
    ("negation after the word does not count", "# T\n\nsocial.plus leaderboards are not hard to set up.\n", 1),
    ("change-summary note under the H1 is skipped", "# T\n\nRemoved the claim that social.plus offers leaderboards.\n\n## H\n\nText.\n", 0),
    ("'has no' before the word is a negation", "# T\n\nsocial.plus has no native leaderboard, so teams build one.\n", 0),
    ("a section heading is not a claim", "# T\n\n## Payments and social.plus\n\nText about something else.\n", 0),
    ("the page's own topic word is a WARN", "# What is an In-App Purchase?\n\nsocial.plus connects to in-app purchases in two ways.\n", 0),
    ("metadata block is skipped", "# T\n\nMeta description: social.plus and payments\n\n## H\n\nText.\n", 0),
    ("text under social.plus's own list entry is a FAIL", "# T\n\n## 6 Best SDKs\n\n### social.plus: Best for apps that want chat\n\nKey strengths: chat with threads, leaderboards and media sharing.\n", 1),
    ("numbered entry heading", "# T\n\n### 1\\. social.plus\n\nIncludes payments out of the box.\n", 1),
    ("bold entry heading", "# T\n\n### **social.plus: Best for consumer apps**\n\nIncludes payments out of the box.\n", 1),
    ("the entry ends at the next heading of the same level", "# T\n\n### social.plus: Best for chat\n\nChat and feeds.\n\n### Stream: Best for feeds\n\nStream offers leaderboards.\n", 0),
    ("a negation under the entry still counts", "# T\n\n### social.plus: Best for chat\n\nIt does not offer leaderboards.\n", 0),
    ("a section heading naming social.plus gives a WARN, not a FAIL", "# T\n\n## Where social.plus fits\n\nTeams add leaderboards next to chat.\n", 0),
    ("a limit the customer handles is a WARN", "# T\n\n### social.plus: Best for retail apps\n\nConnecting tagged products to your payment system requires integration work on your team's side.\n", 0),
    ("list items are separate units", "# T\n\n- **Agora:** fits games with a native leaderboard feature.\n- **social.plus:** fits apps that want chat and feeds.\n", 0),
    ("an H1 naming social.plus sets no context", "# Why social.plus\n\nGamification keeps users.\n", 0),
]


def main() -> int:
    bad = 0
    w = check_text("# T\n\nBiometrics and gamification keep users. The [product overview](https://www.social.plus/product) covers how these pieces fit together.\n", SCOPE)
    ok = len(w["hits"]) == 2 and all(h["level"] == "WARN" for h in w["hits"])
    bad += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] paragraph-level claim is reported as 2 WARN hits")
    w = check_text("# T\n\n## Where social.plus fits\n\nTeams add leaderboards next to chat.\n", SCOPE)
    ok = len(w["hits"]) == 1 and w["hits"][0]["level"] == "WARN" and len(w["claims"]) == 1
    bad += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] a paragraph under a social.plus section heading is listed and WARNs")
    for name, md, want in CASES:
        got = len(check_text(md, SCOPE)["fails"])
        ok = got == want
        bad += not ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} (hits {got}, want {want})")
    real = load_scope(Path(__file__).resolve().parents[1] / "messaging" / "product-capabilities.md")
    ok = len(real) > 0
    bad += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] messaging/product-capabilities.md has an Outside social.plus scope table ({len(real)} rows)")
    print("ALL TESTS PASSED" if not bad else f"{bad} TEST(S) FAILED")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
