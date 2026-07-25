"""
Auto Blog Post Generator untuk Trader Master
Digunakan oleh cron job untuk generate artikel harian tentang analisa trading.
"""
import json, os, sys
from datetime import datetime, timedelta
from pathlib import Path

BLOG_DIR = Path(__file__).parent / "blog"
POSTS_DIR = BLOG_DIR / "posts"
POSTS_JSON = BLOG_DIR / "posts.json"

# Pastikan direktori ada
POSTS_DIR.mkdir(parents=True, exist_ok=True)

TOPICS = [
    {
        "category": "Saham",
        "templates": [
            {
                "title_template": "Analisa IHSG {date}: {direction} di Level {level}",
                "keywords": "analisa IHSG, IHSG hari ini, rekomendasi saham, trading saham indonesia",
            }
        ]
    },
    {
        "category": "Forex",
        "templates": [
            {
                "title_template": "Analisa EUR/USD {date}: {direction} Pasca {event}",
                "keywords": "analisa EUR/USD, trading forex, analisa forex hari ini",
            }
        ]
    },
    {
        "category": "Gold",
        "templates": [
            {
                "title_template": "Analisa XAU/USD {date}: Gold {direction}, Level {level} Jadi Kunci",
                "keywords": "analisa gold, trading gold, XAUUSD analisa, harga emas hari ini",
            }
        ]
    },
    {
        "category": "Edukasi",
        "templates": [
            {
                "title_template": "{date}: {strategy} — Strategi Trading yang Wajib Kamu Kuasai",
                "keywords": "belajar trading, strategi trading, edukasi trading, tips trading",
            }
        ]
    },
]

DIRECTIONS = [
    ("Siap Rebound", "Bullish", ["Resistance Kunci", "Support Kuat", "MA-200"]),
    ("Lanjutkan Rally", "Bullish", ["Breakout", "All-Time High", "Resistance Ditembus"]),
    ("Terkoreksi", "Bearish", ["Support", "Oversold", "Konsolidasi"]),
    ("Sideways", "Neutral", ["Range Sempit", "MA-50", "Equilibrium"]),
]

EVENTS = [
    "Data NFP AS", "Rilis Inflasi Eurozone", "FOMC Minutes",
    "ECB Rate Decision", "GDP Data", "Retail Sales AS",
    "PMI Manufaktur", "CPI Data", "Claim Pengangguran"
]

STRATEGIES = [
    "Support & Resistance", "Moving Average Crossover", "RSI Divergence",
    "Price Action", "Breakout Trading", "Fibonacci Retracement",
    "Ichimoku Cloud", "Bollinger Bands Squeeze", "Volume Profile"
]

import random

def pick(items):
    return random.choice(items)

def generate_post():
    """Generate satu artikel blog."""
    topic = pick(TOPICS)
    tpl = pick(topic["templates"])
    
    direction, sentiment, levels = pick(DIRECTIONS)
    event = pick(EVENTS)
    strategy = pick(STRATEGIES)
    
    date = datetime.now()
    date_str = date.strftime("%Y-%m-%d")
    date_display = date.strftime("%d %B %Y")
    level = pick(levels)
    
    # Generate title
    if topic["category"] == "Forex":
        title = tpl["title_template"].format(date=date_display, direction=direction, event=event)
    elif topic["category"] == "Edukasi":
        title = tpl["title_template"].format(date=date_display, strategy=strategy, level=level)
    else:
        title = tpl["title_template"].format(date=date_display, direction=direction, level=level)
    
    # Slug
    slug = tpl["title_template"].lower()
    slug = slug.replace("{date}", date_str).replace("{direction}", direction.lower().replace(" ", "-"))
    slug = slug.replace("{level}", level.lower().replace(" ", "-"))
    slug = slug.replace("{event}", event.lower().replace(" ", "-"))
    slug = slug.replace("{strategy}", strategy.lower().replace(" ", "-"))
    slug = "".join(c if c.isalnum() or c == "-" else "-" for c in slug)
    slug = slug.strip("-").replace("--", "-")
    
    read_time = random.randint(4, 7)
    
    # Generate excerpt
    excerpts = {
        "Bullish": f"Potensi {direction.lower()} terlihat pada timeframe daily. Level {level} menjadi area krusial. Simak analisa lengkap dengan target harga dan manajemen risiko.",
        "Bearish": f"Tekanan jual masih mendominasi. Level {level} perlu diwaspadai. Analisa lengkap dengan skenario dan level support-resistance.",
        "Neutral": f"Market konsolidasi di area {level}. Tunggu konfirmasi breakout untuk entry. Baca analisa selengkapnya.",
    }
    excerpt = excerpts.get(sentiment, f"Analisa {topic['category'].lower()} terbaru untuk {date_display}. Simak level kunci dan rekomendasi trading.")
    
    # Build HTML content
    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Trader Master</title>
  <meta name="description" content="{excerpt}">
  <meta name="keywords" content="{tpl['keywords']}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{excerpt}">
  <meta property="og:type" content="article">
  <meta property="article:published_time" content="{date_str}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "datePublished": "{date_str}",
    "description": "{excerpt}"
  }}
  </script>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --primary: #1a56db; --green: #16a34a; --red: #dc2626;
      --bg: #f8fafc; --text: #1e293b; --text-muted: #64748b;
      --white: #ffffff; --border: #e2e8f0; --radius: 12px;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      color: var(--text); background: var(--bg); line-height: 1.85;
    }}
    .container {{ max-width: 780px; margin: 0 auto; padding: 0 20px; }}
    nav {{
      background: rgba(255,255,255,0.95); border-bottom: 1px solid var(--border);
      position: sticky; top: 0; z-index: 100; backdrop-filter: blur(12px);
    }}
    nav .container {{ display: flex; align-items: center; justify-content: space-between; height: 64px; }}
    .logo {{ font-size: 1.3rem; font-weight: 800; color: var(--primary); text-decoration: none; }}
    .nav-link {{ color: var(--text-muted); text-decoration: none; font-weight: 500; }}
    .nav-link:hover {{ color: var(--primary); }}
    article {{ padding: 40px 0 60px; }}
    .post-header {{ margin-bottom: 32px; }}
    .post-tag {{
      display: inline-block; background: #eef2ff; color: var(--primary);
      padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin-bottom: 16px;
    }}
    .post-header h1 {{ font-size: 2.2rem; font-weight: 800; letter-spacing: -0.5px; line-height: 1.3; margin-bottom: 12px; }}
    .post-meta {{ color: var(--text-muted); font-size: 0.9rem; }}
    .post-content h2 {{ font-size: 1.5rem; font-weight: 700; margin: 36px 0 14px; }}
    .post-content h3 {{ font-size: 1.2rem; font-weight: 600; margin: 24px 0 10px; }}
    .post-content p {{ margin-bottom: 16px; }}
    .post-content ul, .post-content ol {{ margin: 0 0 20px 24px; }}
    .post-content li {{ margin-bottom: 8px; }}
    .callout {{
      background: #fef3c7; border-left: 4px solid #f59e0b; padding: 16px 20px;
      border-radius: 0 8px 8px 0; margin: 24px 0; font-size: 0.95rem;
    }}
    .callout strong {{ color: #92400e; }}
    .signal-box {{
      background: linear-gradient(135deg, #ecfdf5, #d1fae5);
      border: 1px solid #6ee7b7; border-radius: var(--radius); padding: 20px 24px; margin: 28px 0;
    }}
    .signal-box h3 {{ color: #065f46; margin-bottom: 12px; }}
    .signal-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #a7f3d0; }}
    .signal-row:last-child {{ border-bottom: none; }}
    .signal-label {{ font-weight: 600; }}
    .signal-value {{ font-weight: 700; }}
    .bullish {{ color: var(--green); }}
    .bearish {{ color: var(--red); }}
    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }}
    th {{ background: #f1f5f9; padding: 12px 16px; text-align: left; font-weight: 600; font-size: 0.9rem; }}
    td {{ padding: 10px 16px; border-top: 1px solid var(--border); font-size: 0.9rem; }}
    .share-section {{ margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--border); }}
    .share-section h4 {{ margin-bottom: 12px; }}
    footer {{
      background: var(--text); color: #94a3b8; padding: 40px 20px; text-align: center; font-size: 0.85rem;
    }}
    footer a {{ color: #cbd5e1; text-decoration: none; margin: 0 12px; }}
    footer a:hover {{ color: var(--white); }}
    footer .copyright {{ margin-top: 16px; }}
    @media (max-width: 600px) {{ .post-header h1 {{ font-size: 1.6rem; }} }}
  </style>
</head>
<body>
<nav>
  <div class="container">
    <a href="/" class="logo">📊 Trader Master</a>
    <a href="/blog/" class="nav-link">← Blog</a>
  </div>
</nav>
<main class="container">
<article>
  <header class="post-header">
    <span class="post-tag">{topic['category']}</span>
    <h1>{title}</h1>
    <p class="post-meta">📅 {date_display} · ⏱️ {read_time} menit baca</p>
  </header>
  <div class="post-content">
    <p><strong>{topic['category']}</strong> — Analisa terbaru untuk {date_display}. Berikut adalah breakdown teknikal lengkap dengan level support-resistance, skenario pergerakan, dan rekomendasi trading.</p>
    <div class="callout">
      <strong>📊 Ringkasan Cepat:</strong> Market menunjukkan sinyal <strong>{direction.lower()}</strong> di timeframe daily. Level <strong>{level}</strong> menjadi area krusial yang perlu diperhatikan trader. Simak analisa selengkapnya di bawah.
    </div>
    <h2>Kondisi Market</h2>
    <p>Pasar global menunjukkan pergerakan mixed dalam 24 jam terakhir. Data ekonomi terbaru memberikan sinyal beragam bagi pelaku pasar. Trader disarankan untuk tetap waspada dan mengikuti level-level kunci yang telah diidentifikasi.</p>
    <p>Dari sisi teknikal, beberapa indikator mulai memberikan sinyal yang menarik. Mari kita breakdown satu per satu.</p>
    <h2>Analisa Teknikal</h2>
    <h3>Support & Resistance</h3>
    <table>
      <thead><tr><th>Level</th><th>Harga</th><th>Keterangan</th></tr></thead>
      <tbody>
        <tr><td>Resistance 2</td><td><strong>R2</strong></td><td>Resistance dari swing high sebelumnya</td></tr>
        <tr><td>Resistance 1</td><td><strong>R1</strong></td><td>Resistance MA-50 daily</td></tr>
        <tr><td>Support 1</td><td><strong>S1</strong></td><td>Support psikologis</td></tr>
        <tr><td>Support 2</td><td><strong>S2</strong></td><td>Support dari low sebelumnya</td></tr>
      </tbody>
    </table>
    <h3>Indikator</h3>
    <ul>
      <li><strong>RSI (14):</strong> Menunjukkan momentum yang menarik — perlu konfirmasi lebih lanjut</li>
      <li><strong>MACD:</strong> Histogram memberikan sinyal awal perubahan trend</li>
      <li><strong>Moving Average:</strong> Perhatikan posisi harga terhadap MA-20, MA-50, dan MA-200</li>
      <li><strong>Volume:</strong> Volume menjadi konfirmasi penting untuk validitas pergerakan</li>
    </ul>
    <h2>Skenario Pergerakan</h2>
    <h3>🟢 Skenario Bullish</h3>
    <p>Jika harga berhasil bertahan di atas support kunci dan mengkonfirmasi dengan candlestick reversal, target upside berada di resistance terdekat. Konfirmasi dari RSI dan volume akan memperkuat skenario ini.</p>
    <h3>🔴 Skenario Bearish</h3>
    <p>Breakdown di bawah support dengan volume tinggi akan membuka jalan menuju support berikutnya. Trader disarankan untuk memasang stop loss yang ketat.</p>
    <h2>Rekomendasi Trading</h2>
    <div class="signal-box">
      <h3>🎯 Sinyal Hari Ini</h3>
      <div class="signal-row">
        <span class="signal-label">Bias</span>
        <span class="signal-value">
          {'<span class="bullish">BUY — Cari entry di support</span>' if sentiment == 'Bullish' else ('<span class="bearish">SELL — Wait for breakdown</span>' if sentiment == 'Bearish' else 'WAIT — Tunggu konfirmasi breakout')}
        </span>
      </div>
      <div class="signal-row">
        <span class="signal-label">Entry</span>
        <span class="signal-value">Area Support / Resistance kunci</span>
      </div>
      <div class="signal-row">
        <span class="signal-label">Target</span>
        <span class="signal-value">Resistance / Support berikutnya</span>
      </div>
      <div class="signal-row">
        <span class="signal-label">Stop Loss</span>
        <span class="signal-value">2-3% dari entry</span>
      </div>
    </div>
    <h2>Manajemen Risiko</h2>
    <ul>
      <li><strong>Posisi maksimal:</strong> Jangan melebihi risiko yang ditoleransi</li>
      <li><strong>Stop loss:</strong> Selalu pasang stop loss di setiap posisi</li>
      <li><strong>Diversifikasi:</strong> Jangan taruh semua modal di satu instrumen</li>
      <li><strong>Money management:</strong> Risiko per trade maksimal 1-2% dari total modal</li>
    </ul>
    <div class="callout">
      <strong>⚠️ Disclaimer:</strong> Analisa ini bersifat informatif dan edukatif. Bukan rekomendasi investasi. Semua keputusan trading ada di tangan Anda. Pastikan selalu menggunakan manajemen risiko yang baik.
    </div>
    <div class="share-section">
      <h4>📤 Bagikan artikel ini:</h4>
      <a href="https://t.me/share/url?url=https://aitrading.biz.id/blog/posts/{slug}.html" class="share-btn" style="display:inline-block;padding:8px 18px;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.85rem;margin-right:8px;color:white;background:#0088cc;" target="_blank">Telegram</a>
      <a href="https://twitter.com/intent/tweet?url=https://aitrading.biz.id/blog/posts/{slug}.html" class="share-btn" style="display:inline-block;padding:8px 18px;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.85rem;margin-right:8px;color:white;background:#1da1f2;" target="_blank">Twitter</a>
    </div>
  </div>
</article>
</main>
<footer>
  <div>
    <a href="/">Home</a>
    <a href="/blog/">Blog</a>
    <a href="/#pricing">Pricing</a>
  </div>
  <p class="copyright">© 2026 Trader Master. Trading mengandung risiko. Hasil masa lalu tidak menjamin hasil masa depan.</p>
</footer>
</body>
</html>"""

    return {
        "slug": slug,
        "title": title,
        "date": date_str,
        "readTime": read_time,
        "category": topic["category"],
        "excerpt": excerpt,
        "html": html
    }


def main():
    # Load existing posts
    existing = []
    if POSTS_JSON.exists():
        try:
            existing = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
        except:
            pass
    
    # Generate new post
    post = generate_post()
    
    # Check if slug already exists
    existing_slugs = {p["slug"] for p in existing}
    if post["slug"] in existing_slugs:
        print(f"Slug {post['slug']} already exists, regenerating...")
        for _ in range(5):
            post = generate_post()
            if post["slug"] not in existing_slugs:
                break
    
    # Write HTML file
    html_path = POSTS_DIR / f"{post['slug']}.html"
    html_path.write_text(post["html"], encoding="utf-8")
    print(f"✅ Written: {html_path}")
    
    # Update posts.json (prepend new post)
    meta = {k: post[k] for k in ["slug", "title", "date", "readTime", "category", "excerpt"]}
    existing.insert(0, meta)
    POSTS_JSON.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Updated: {POSTS_JSON}")
    
    return post["slug"]


if __name__ == "__main__":
    slug = main()
    print(f"\n🚀 Post generated: {slug}")
