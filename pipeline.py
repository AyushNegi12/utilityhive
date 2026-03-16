"""
UtilityHive — FREE Stack Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI:      Groq API — llama-3.3-70b-versatile (FREE, 14,400 req/day)
DB:      Supabase FREE tier (500MB PostgreSQL)
Hosting: Vercel FREE hobby tier (Next.js SSG)
Cron:    GitHub Actions FREE (runs every 6 hours)
Cost:    $0/month until you're earning

Install:
  pip install groq supabase requests python-dotenv
"""

import os, json, time, itertools, re, argparse
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ── CONFIG ─────────────────────────────────────────────────────────────────────
GROQ_API_KEY    = os.getenv("GROQ_API_KEY")         # console.groq.com (free)
SUPABASE_URL    = os.getenv("SUPABASE_URL")          # supabase.com (free)
SUPABASE_KEY    = os.getenv("SUPABASE_KEY")
VERCEL_HOOK     = os.getenv("VERCEL_DEPLOY_HOOK")    # Optional: auto-deploy
GROQ_MODEL      = "llama-3.3-70b-versatile"          # Best free model on Groq
PAGES_PER_RUN   = int(os.getenv("PAGES_PER_RUN", 10))

# ── KEYWORD NICHES ─────────────────────────────────────────────────────────────
NICHES = {
    "gaming": {
        "heads": [
            "clash royale", "valorant", "minecraft", "elden ring",
            "pokemon go", "apex legends", "roblox", "genshin impact",
            "league of legends", "fortnite", "diablo 4", "warzone",
        ],
        "mods": [
            "best deck 2026", "tier list", "meta guide", "farming tips",
            "pro settings", "codes 2026", "best build", "hidden tricks",
            "complete guide", "beginners guide", "is it worth it",
            "how to get more", "fastest way to rank",
        ],
    },
    "tools": {
        "heads": [
            "roi calculator", "mortgage calculator", "bmi calculator",
            "compound interest calculator", "tax estimator", "word counter",
            "password generator", "qr code generator", "color picker",
            "percentage calculator", "age calculator", "currency converter",
        ],
        "mods": [
            "online free", "no signup", "instant 2026", "step by step",
            "download free", "for beginners", "easy to use", "accurate",
            "best free", "no ads",
        ],
    },
    "finance": {
        "heads": [
            "python automation", "excel formula", "google sheets template",
            "notion template", "power bi dashboard", "ai prompt for",
            "chatgpt prompt for", "automation script for",
        ],
        "mods": [
            "for beginners", "free download 2026", "complete tutorial",
            "step by step", "no coding needed", "advanced tips", "cheat sheet",
            "examples", "real world",
        ],
    },
    "health": {
        "heads": [
            "calorie calculator", "macro calculator", "intermittent fasting",
            "keto diet", "workout plan", "sleep tracker", "water intake calculator",
            "tdee calculator", "protein intake", "body fat percentage",
        ],
        "mods": [
            "calculator free", "plan for beginners", "2026 guide",
            "does it work", "how to start", "best app", "results reddit",
            "for women", "for men over 40", "7 day plan",
        ],
    },
}


@dataclass
class PageData:
    keyword:      str
    niche:        str
    slug:         str
    title:        str
    meta_desc:    str
    content_html: str
    word_count:   int
    has_tool:     bool   # Critical for Google 2026 "original data" requirement
    faq:          list


# ── GROQ CONTENT GENERATOR ─────────────────────────────────────────────────────
def generate_page(keyword: str, niche: str) -> Optional[PageData]:
    """
    Generate a full SEO page using Groq (FREE).
    Includes mandatory 'original data' element for Google compliance.
    Rate: ~14,400 pages/day free on Groq.
    """
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)

    # Determine what type of original data to include
    tool_types = {
        "gaming":  "comparison table with stats (damage, DPS, win rate %)",
        "tools":   "interactive calculator with real formula",
        "finance": "step-by-step checklist with downloadable template",
        "health":  "personalized calculator (enter weight/age → get result)",
    }
    tool_type = tool_types.get(niche, "data table with real statistics")

    prompt = f"""You are an expert SEO content writer for a utility/tool website.
Write a complete, high-quality page for the search keyword: "{keyword}"

MANDATORY REQUIREMENTS (Google 2026 compliance):
1. JSON response only — no markdown, no preamble
2. Include ORIGINAL DATA: a {tool_type}
   (This prevents Google's "AI spam" flag — every page needs unique interactive data)
3. Natural keyword placement — not spammy
4. FAQ based on "People Also Ask" for this keyword

Return ONLY this JSON (no backticks, no extra text):
{{
  "title": "H1 title with keyword (max 60 chars)",
  "meta_desc": "Meta description 150-160 chars with keyword",
  "intro": "Hook paragraph 120 words. Answer the query immediately.",
  "section1_heading": "Section heading with LSI keyword",
  "section1_body": "300 words of genuinely useful content with real facts/numbers",
  "original_data": "HTML for the {tool_type} — real numbers, not placeholder",
  "section2_heading": "Practical tips heading",
  "section2_body": "250 words of actionable tips. Use <ul><li> list.",
  "faq": [
    {{"q": "Question 1?", "a": "Answer 1 (2-3 sentences)."}},
    {{"q": "Question 2?", "a": "Answer 2."}},
    {{"q": "Question 3?", "a": "Answer 3."}},
    {{"q": "Question 4?", "a": "Answer 4."}},
    {{"q": "Question 5?", "a": "Answer 5."}}
  ],
  "conclusion": "100 word conclusion with soft CTA to use the tool/calculator"
}}"""

    try:
        chat = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3500,
            temperature=0.7,
        )
        raw = chat.choices[0].message.content.strip()

        # Clean up any accidental markdown fences
        raw = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(raw)

        # Build full HTML
        content_html = f"""
<h1>{data['title']}</h1>
<p>{data['intro']}</p>
<h2>{data['section1_heading']}</h2>
<p>{data['section1_body']}</p>
<div class="original-data">{data['original_data']}</div>
<h2>{data['section2_heading']}</h2>
<p>{data['section2_body']}</p>
<h2>Frequently Asked Questions</h2>
{"".join(f'<details><summary>{f["q"]}</summary><p>{f["a"]}</p></details>' for f in data["faq"])}
<p>{data['conclusion']}</p>
"""
        word_count = len(re.sub(r'<[^>]+>', '', content_html).split())

        return PageData(
            keyword=keyword,
            niche=niche,
            slug=keyword.lower().replace(" ", "-").replace("/", "-"),
            title=data["title"],
            meta_desc=data["meta_desc"],
            content_html=content_html,
            word_count=word_count,
            has_tool=True,
            faq=data.get("faq", []),
        )

    except json.JSONDecodeError as e:
        print(f"  ✗ JSON parse error for '{keyword}': {e}")
        return None
    except Exception as e:
        print(f"  ✗ Groq error for '{keyword}': {e}")
        return None


# ── SUPABASE SAVE ──────────────────────────────────────────────────────────────
def save_to_supabase(page: PageData, db) -> bool:
    """Save page to Supabase PostgreSQL (free 500MB)."""
    try:
        result = db.table("pages").upsert({
            "keyword":      page.keyword,
            "niche":        page.niche,
            "slug":         page.slug,
            "title":        page.title,
            "meta_desc":    page.meta_desc,
            "content_html": page.content_html,
            "word_count":   page.word_count,
            "has_tool":     page.has_tool,
            "status":       "draft",
        }, on_conflict="keyword").execute()
        return True
    except Exception as e:
        print(f"  ✗ Supabase error: {e}")
        return False


# ── VERCEL DEPLOY TRIGGER ──────────────────────────────────────────────────────
def trigger_vercel_deploy():
    """
    Trigger Vercel rebuild after new pages are saved.
    Set up your deploy hook in: Vercel → Project Settings → Git → Deploy Hooks
    """
    if not VERCEL_HOOK:
        print("  ⚠ VERCEL_DEPLOY_HOOK not set — skipping auto-deploy")
        return
    import requests
    try:
        r = requests.post(VERCEL_HOOK, timeout=10)
        if r.status_code == 201:
            print("  ✓ Vercel deploy triggered — pages live in ~60s")
        else:
            print(f"  ✗ Vercel returned: {r.status_code}")
    except Exception as e:
        print(f"  ✗ Vercel hook error: {e}")


# ── KEYWORD MATRIX ─────────────────────────────────────────────────────────────
def get_pending_keywords(niche: str, db, limit: int) -> list[str]:
    """Get keywords not yet generated from Supabase."""
    cfg     = NICHES[niche]
    all_kws = [f"{h} {m}" for h, m in itertools.product(cfg["heads"], cfg["mods"])]

    try:
        # Get already-generated slugs from Supabase
        existing = db.table("pages").select("keyword").eq("niche", niche).execute()
        done_set = {r["keyword"] for r in (existing.data or [])}
        pending  = [k for k in all_kws if k not in done_set]
        return pending[:limit]
    except Exception:
        # If table doesn't exist yet, return all
        return all_kws[:limit]


# ── ARBITRAGE ANALYZER ────────────────────────────────────────────────────────
def analyze_arbitrage(db) -> None:
    """
    Print pages where RPM > CPC × 1000 — these are profitable to buy traffic for.
    Phase 2: start Taboola/MGID on these pages at $5/day budget.
    """
    print("\n📊 ARBITRAGE OPPORTUNITIES (pages to buy traffic for)")
    print("─" * 60)

    try:
        pages = db.table("pages").select("keyword,rpm,sessions").gt("rpm", 0).execute()
        TABOOLA_CPC = 0.08   # Your negotiated Taboola CPC

        profitable = []
        for p in (pages.data or []):
            spread = p["rpm"] - (TABOOLA_CPC * 1000)
            if spread > 0:
                roi = (spread / (TABOOLA_CPC * 1000)) * 100
                profitable.append((p["keyword"], p["rpm"], spread, roi))

        if not profitable:
            print("  No pages with RPM data yet. Run pipeline first.")
            return

        for kw, rpm, spread, roi in sorted(profitable, key=lambda x: x[2], reverse=True)[:10]:
            print(f"  {kw:<45} RPM:${rpm:.2f}  Spread:${spread:.2f}  ROI:{roi:.0f}%  → {'SCALE' if roi>50 else 'TEST'}")

    except Exception as e:
        print(f"  Error: {e}")


# ── MAIN PIPELINE ──────────────────────────────────────────────────────────────
def run(niche: str, batch: int, dry_run: bool = False):
    print(f"\n{'━'*62}")
    print(f"  UtilityHive FREE Pipeline — Niche: {niche.upper()}")
    print(f"  Stack: Groq (free) + Supabase (free) + Vercel (free)")
    print(f"{'━'*62}\n")

    if dry_run:
        cfg = NICHES[niche]
        kws = [f"{h} {m}" for h, m in itertools.product(cfg["heads"], cfg["mods"])]
        print(f"DRY RUN — {len(kws)} total keyword combinations for [{niche}]:\n")
        for i, k in enumerate(kws[:30], 1):
            print(f"  {i:3}. {k}")
        if len(kws) > 30:
            print(f"  ... and {len(kws)-30} more")
        print(f"\n  Run without --dry-run to generate pages.")
        return

    # Init Supabase
    from supabase import create_client
    db = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Get pending keywords
    pending = get_pending_keywords(niche, db, batch)
    if not pending:
        print(f"  ✓ All keywords for [{niche}] already generated!")
        analyze_arbitrage(db)
        return

    print(f"[ Scout ] {len(pending)} keywords queued for generation\n")

    success = 0
    for i, kw in enumerate(pending, 1):
        print(f"[ Writer ] ({i}/{len(pending)}) '{kw}'")
        page = generate_page(kw, niche)

        if page:
            saved = save_to_supabase(page, db)
            if saved:
                print(f"  ✓ Saved — {page.word_count} words, has_tool={page.has_tool}")
                success += 1
            # Respect Groq rate limits (free tier = ~1 req/sec safe)
            time.sleep(1.2)
        else:
            print(f"  ✗ Skipped")

    print(f"\n[ Deploy ] Triggering Vercel rebuild...")
    trigger_vercel_deploy()

    print(f"\n{'━'*62}")
    print(f"  ✓ Complete: {success}/{len(pending)} pages generated")
    print(f"  Next run: in 6 hours via GitHub Actions cron")
    print(f"{'━'*62}\n")

    analyze_arbitrage(db)


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UtilityHive Free Pipeline")
    parser.add_argument("--niche",   default="gaming",  choices=list(NICHES.keys()))
    parser.add_argument("--batch",   default=PAGES_PER_RUN, type=int)
    parser.add_argument("--dry-run", action="store_true", help="Preview keywords without API calls")
    parser.add_argument("--arb",     action="store_true", help="Show arbitrage opportunities only")
    args = parser.parse_args()

    if args.arb:
        from supabase import create_client
        analyze_arbitrage(create_client(SUPABASE_URL, SUPABASE_KEY))
    else:
        run(args.niche, args.batch, args.dry_run)

"""
USAGE:
  # Preview keyword list (no API calls):
  python pipeline.py --dry-run --niche gaming

  # Generate 10 pages (uses Groq + Supabase):
  python pipeline.py --niche gaming --batch 10

  # Generate more at once:
  python pipeline.py --niche tools --batch 50

  # Check arbitrage opportunities:
  python pipeline.py --arb

REQUIRED ENV VARS (.env.local):
  GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx    # console.groq.com → free
  SUPABASE_URL=https://xxx.supabase.co  # supabase.com → free
  SUPABASE_KEY=eyJxxxxxxxxxxxxxxxxxxx   # supabase.com → free
  VERCEL_DEPLOY_HOOK=https://api.vercel.com/v1/integrations/deploy/xxx  # optional

GROQ FREE LIMITS:
  - 14,400 requests/day
  - ~600 pages/day (with 1.2s delay)
  - Resets midnight UTC
  - Model: llama-3.3-70b-versatile (best quality free)

SUPABASE FREE LIMITS:
  - 500MB database (holds ~500,000 pages easily)
  - 50,000 rows
  - Resets never (persistent)

VERCEL FREE LIMITS:
  - Unlimited deploys
  - 100GB bandwidth/month
  - Edge network CDN (global)
  - Custom domain support
"""
