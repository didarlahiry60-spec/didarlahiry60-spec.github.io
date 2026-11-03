import os
from PIL import Image, ImageDraw, ImageFont

def make_perfect_poster(filename, app_name, url_bar, accent_color, hero_tag, hero_title, hero_desc, ui_cards, sidebar_items, status_text):
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (14, 17, 26, 255))
    draw = ImageDraw.Draw(im)

    font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font_bengali = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"

    f_title_main = ImageFont.truetype(font_bold, 36)
    f_title_b = ImageFont.truetype(font_bengali, 34)
    f_h2 = ImageFont.truetype(font_bold, 20)
    f_card_title = ImageFont.truetype(font_bold, 20)
    f_body = ImageFont.truetype(font_reg, 17)
    f_desc = ImageFont.truetype(font_reg, 16)
    f_tag = ImageFont.truetype(font_bold, 14)
    f_pill = ImageFont.truetype(font_bold, 14)
    f_sm = ImageFont.truetype(font_reg, 14)
    f_nav = ImageFont.truetype(font_bold, 16)
    f_browser = ImageFont.truetype(font_reg, 15)

    # Lighter soft text color derived from accent
    accent_text = (
        min(255, accent_color[0] + 50),
        min(255, accent_color[1] + 50),
        min(255, accent_color[2] + 50)
    )

    # Outer Browser / OS Window Frame
    draw.rounded_rectangle([(25, 20), (1255, 700)], radius=16, fill=(18, 22, 34, 255), outline=(50, 62, 88, 255), width=2)

    # Top Window Bar
    draw.rounded_rectangle([(25, 20), (1255, 80)], radius=16, fill=(24, 29, 45, 255))
    draw.line([(25, 80), (1255, 80)], fill=(45, 55, 80, 255), width=1)

    # Window dots
    draw.ellipse([(50, 42), (66, 58)], fill=(255, 110, 100, 255))
    draw.ellipse([(76, 42), (92, 58)], fill=(250, 200, 80, 255))
    draw.ellipse([(102, 42), (118, 58)], fill=(120, 220, 160, 255))

    # Browser URL Address Bar
    draw.rounded_rectangle([(180, 35), (880, 67)], radius=8, fill=(13, 16, 26, 255), outline=(55, 68, 96, 255), width=1)
    draw.text((205, 42), f"https://{url_bar}", fill=(210, 220, 240), font=f_browser)

    # Window right status
    draw.text((940, 42), f"● {status_text}", fill=accent_color, font=f_nav)
    draw.text((1140, 42), "PROD v2.6", fill=(160, 175, 205), font=f_sm)

    # Left Sidebar (width: 255px)
    draw.rectangle([(25, 81), (280, 698)], fill=(15, 18, 28, 255))
    draw.line([(280, 81), (280, 698)], fill=(42, 52, 75, 255), width=1)

    # Sidebar Header
    draw.text((45, 110), app_name.upper(), fill=(245, 248, 255), font=f_h2)
    draw.line([(45, 145), (260, 145)], fill=(42, 52, 75, 255), width=1)

    # Sidebar Navigation items
    y_nav = 165
    for idx, (label, is_active) in enumerate(sidebar_items):
        if is_active:
            # Active sidebar item: Soft tinted frosted glass with delicate border & light accent text
            draw.rounded_rectangle([(40, y_nav - 5), (265, y_nav + 34)], radius=8, fill=(accent_color[0], accent_color[1], accent_color[2], 42), outline=(accent_color[0], accent_color[1], accent_color[2], 130), width=1)
            draw.text((55, y_nav + 4), label, fill=accent_text, font=f_nav)
        else:
            draw.text((55, y_nav + 4), label, fill=(170, 182, 205), font=f_nav)
        y_nav += 48

    # Sidebar bottom system status
    draw.rounded_rectangle([(40, 580), (265, 665)], radius=10, fill=(22, 27, 42, 255), outline=(50, 62, 88, 255), width=1)
    draw.text((55, 595), "SYSTEM TELEMETRY", fill=(160, 175, 205), font=f_sm)
    
    # Status Pill
    draw.rounded_rectangle([(50, 622), (255, 654)], radius=6, fill=(accent_color[0], accent_color[1], accent_color[2], 38), outline=(accent_color[0], accent_color[1], accent_color[2], 120), width=1)
    draw.text((65, 628), "99.98% High Uptime", fill=accent_text, font=f_pill)

    # Main Workspace Hero Card (width: 920px: 305 to 1225)
    hero_box_x1, hero_box_x2 = 305, 1225
    draw.rounded_rectangle([(hero_box_x1, 110), (hero_box_x2, 275)], radius=14, fill=(21, 26, 40, 255), outline=(accent_color[0], accent_color[1], accent_color[2], 110), width=1)
    
    # Top Tag Pill
    pill_text = f"★ {hero_tag.upper()}"
    bbox_pill = draw.textbbox((0, 0), pill_text, font=f_pill)
    text_w = bbox_pill[2] - bbox_pill[0]
    pill_x1 = 330
    pill_y1 = 130
    pill_x2 = pill_x1 + text_w + 28
    pill_y2 = pill_y1 + 34

    draw.rounded_rectangle([(pill_x1, pill_y1), (pill_x2, pill_y2)], radius=7, fill=(accent_color[0], accent_color[1], accent_color[2], 42), outline=(accent_color[0], accent_color[1], accent_color[2], 130), width=1)
    draw.text((pill_x1 + 14, pill_y1 + 8), pill_text, fill=accent_text, font=f_pill)

    # Hero Title
    draw.text((330, 178), hero_title[0], fill=(255, 255, 255), font=f_title_main)
    if len(hero_title) > 1 and hero_title[1]:
        bbox = draw.textbbox((0, 0), hero_title[0], font=f_title_main)
        w_title = bbox[2] - bbox[0]
        draw.text((330 + w_title + 14, 180), hero_title[1], fill=accent_color, font=f_title_b)

    # Hero Subtitle (Guaranteed strictly inside box, with safe right margin)
    max_desc_w = hero_box_x2 - 330 - 24 # 871px available
    bbox_desc = draw.textbbox((0, 0), hero_desc, font=f_desc)
    desc_w = bbox_desc[2] - bbox_desc[0]
    safe_desc = hero_desc
    if desc_w > max_desc_w:
        # Ellipsis clamp if ever needed
        while desc_w > max_desc_w and len(safe_desc) > 5:
            safe_desc = safe_desc[:-2]
            bbox_desc = draw.textbbox((0, 0), safe_desc + "...", font=f_desc)
            desc_w = bbox_desc[2] - bbox_desc[0]
        safe_desc = safe_desc + "..."

    draw.text((330, 234), safe_desc, fill=(200, 212, 230), font=f_desc)

    # 4 UI Content Dashboard Cards
    card_coords = [
        ((305, 305), (745, 475)),
        ((775, 305), (1225, 475)),
        ((305, 500), (745, 670)),
        ((775, 500), (1225, 670))
    ]

    for (c_tl, c_br), (c_title, c_badge, c_items, c_tag) in zip(card_coords, ui_cards):
        draw.rounded_rectangle([c_tl, c_br], radius=12, fill=(19, 24, 38, 255), outline=(50, 62, 88, 255), width=1)
        
        # Card header bar
        draw.rounded_rectangle([c_tl, (c_br[0], c_tl[1] + 42)], radius=12, fill=(25, 32, 50, 255))
        draw.line([(c_tl[0], c_tl[1] + 42), (c_br[0], c_tl[1] + 42)], fill=(48, 60, 85, 255), width=1)
        
        # Header text
        draw.text((c_tl[0] + 16, c_tl[1] + 10), c_title, fill=(245, 248, 255), font=f_card_title)
        
        # Header right badge - precisely right-aligned with safe padding
        bbox_b = draw.textbbox((0, 0), c_badge, font=f_sm)
        badge_w = bbox_b[2] - bbox_b[0]
        draw.text((c_br[0] - badge_w - 18, c_tl[1] + 13), c_badge, fill=accent_color, font=f_sm)

        # Content lines
        y_c = c_tl[1] + 55
        max_line_w = (c_br[0] - c_tl[0]) - 48
        for line in c_items:
            draw.ellipse([(c_tl[0] + 16, y_c + 7), (c_tl[0] + 24, y_c + 15)], fill=accent_color)
            # Safe width clamp
            bbox_line = draw.textbbox((0, 0), line, font=f_body)
            lw = bbox_line[2] - bbox_line[0]
            safe_line = line
            if lw > max_line_w:
                while lw > max_line_w and len(safe_line) > 5:
                    safe_line = safe_line[:-2]
                    bbox_line = draw.textbbox((0, 0), safe_line + "...", font=f_body)
                    lw = bbox_line[2] - bbox_line[0]
                safe_line = safe_line + "..."
            draw.text((c_tl[0] + 32, y_c), safe_line, fill=(225, 235, 250), font=f_body)
            y_c += 28

        # Card bottom pill tag
        bbox_tag = draw.textbbox((0, 0), c_tag, font=f_tag)
        tag_w = bbox_tag[2] - bbox_tag[0]
        tag_x1 = c_tl[0] + 16
        tag_y1 = c_br[1] - 36
        tag_x2 = min(tag_x1 + tag_w + 26, c_br[0] - 16)
        tag_y2 = tag_y1 + 28
        draw.rounded_rectangle([(tag_x1, tag_y1), (tag_x2, tag_y2)], radius=6, fill=(accent_color[0], accent_color[1], accent_color[2], 38), outline=(accent_color[0], accent_color[1], accent_color[2], 120), width=1)
        draw.text((tag_x1 + 13, tag_y1 + 5), c_tag, fill=accent_text, font=f_tag)

    # Save outputs
    out1 = os.path.join("/home/didar-lahiry/Antigravity/Target Portfolio 2/demos", filename)
    out2 = os.path.join("/home/didar-lahiry/Antigravity/Target Portfolio 2/public/demos", filename)
    im.convert("RGB").save(out1, "WEBP", quality=95)
    im.convert("RGB").save(out2, "WEBP", quality=95)
    print(f"Generated perfect poster: {out1} & {out2}")

# 1. Kishan AI Platform - Soft Sage / Mint (#8fd3c1 -> (143, 211, 193))
make_perfect_poster(
    filename="kishan-poster.webp",
    app_name="Kishan Dashboard",
    url_bar="kishan.agro.bd/live-market",
    accent_color=(143, 211, 193), # Soft Mint / Sage (portfolio's --d-teal)
    hero_tag="National Agriculture Telemetry",
    hero_title=("Kishan AI Platform", "(কৃষাণ)"),
    hero_desc="Live DAM Market Price Intelligence, 7-Day Weather Forecasting & Bengali Voice Assistant",
    sidebar_items=[
        ("Market Telemetry", True),
        ("Weather Advisory", False),
        ("Bangla TTS Voice", False),
        ("Disaster Alert SMS", False),
        ("API Integrations", False)
    ],
    status_text="LIVE CONNECTED",
    ui_cards=[
        ("DAM Market Index", "64 Districts", ["Daily wholesale vs retail pricing", "Crop trend percentage tracking"], "FastAPI + Gemini AI"),
        ("Weather Forecast", "Open-Meteo", ["Hyper-local 7-day precipitation", "Crop-specific agronomic advice"], "Automated Cron"),
        ("Accessibility Audio", "Bangla TTS", ["Voice readouts of market rates", "One-tap audio bulletin player"], "Native Audio API"),
        ("Offline Storage", "SQLite DB", ["Full cache for rural connectivity", "Zero login guest access mode"], "Local Database")
    ]
)

# 2. Letter Portfolio - Soft Pastel Rose / Pink (#ff9ebb -> (255, 158, 187))
make_perfect_poster(
    filename="letter-portfolio-poster.webp",
    app_name="Letter Desktop",
    url_bar="portfolio.didarlahiry.com/desk",
    accent_color=(255, 158, 187), # Soft Pastel Pink (portfolio's signature --screen)
    hero_tag="Tactile Web Experience",
    hero_title=("Letter Portfolio Experience", ""),
    hero_desc="Interactive Envelope Metaphor, Tactile Stationery & 3D Desk Experience in Next.js",
    sidebar_items=[
        ("Stationery Desk", True),
        ("Story & Career", False),
        ("Tech Stack Folders", False),
        ("Direct Dispatch", False),
        ("Settings", False)
    ],
    status_text="60 FPS FLUID",
    ui_cards=[
        ("Envelope Metaphor", "Dynamic Tilt", ["Physics-based tilt & reactive drag", "Smooth tactile open animations"], "Framer Motion"),
        ("Modular Sections", "Instant Tabs", ["Personal story & project files", "Interactive skill stack cards"], "React + Tailwind"),
        ("High Performance", "100/100 Core", ["Zero-latency SSG static speed", "Sub-second load across mobile"], "Next.js App Router"),
        ("Visual Aesthetics", "Clean Studio", ["Modern typography and dark tones", "Seamless browser responsiveness"], "CSS Hardware Accel")
    ]
)

# 3. AI Sales Agent - Soft Warm Amber / Dusk Peach (#f0a35e -> (240, 163, 94))
make_perfect_poster(
    filename="sales-bot-poster.webp",
    app_name="Sales Concierge",
    url_bar="agent.sales.telegram/console",
    accent_color=(240, 163, 94), # Soft Dusk Amber (portfolio's --d-amber)
    hero_tag="Autonomous Telegram Concierge",
    hero_title=("E-Commerce AI Sales Agent", ""),
    hero_desc="Autonomous Telegram Sales Representative with Product Advice & 24/7 Checkout",
    sidebar_items=[
        ("Autonomous Agent", True),
        ("Catalog & Sizing", False),
        ("Cart & Orders", False),
        ("Supervisor Handoff", False),
        ("Conversion Stats", False)
    ],
    status_text="24/7 STANDBY",
    ui_cards=[
        ("Conversational Engine", "Gemini 2.5", ["Multi-turn natural buyer advice", "Product suggestions and size guide"], "Gemini API"),
        ("Order Dispatch", "SQLite DB", ["Automated cart & checkout logger", "Customer address & order receipt"], "Python AsyncIO"),
        ("Supervisor Takeover", "Admin Mode", ["Live human takeover console", "Instant alert on high-value orders"], "Telegram Webhooks"),
        ("Sales Metrics", "+350% Speed", ["Instant response with zero wait", "Automated FAQ resolution 24/7"], "Cloud Automated")
    ]
)

# 4. FB Automation - Soft Sky / Periwinkle (#93c5fd -> (147, 197, 253))
make_perfect_poster(
    filename="fb-automation-poster.webp",
    app_name="Cloud Automation",
    url_bar="meta.graph.automation/dashboard",
    accent_color=(147, 197, 253), # Soft Sky / Lavender
    hero_tag="Autonomous Social Manager",
    hero_title=("Facebook 24/7 AI Automation", ""),
    hero_desc="Autonomous 24/7 Facebook Manager: AI Content, Graphic Banners & Messenger Bot",
    sidebar_items=[
        ("Auto Publishing", True),
        ("Graphic Banners", False),
        ("Comment Engine", False),
        ("Messenger Concierge", False),
        ("Page Growth", False)
    ],
    status_text="SCHEDULE ACTIVE",
    ui_cards=[
        ("Scheduled Publishing", "3x Daily", ["AI trending tech post generation", "Scheduled automated cron release"], "APScheduler"),
        ("Dynamic Graphics", "Pillow", ["Topic-tailored banner rendering", "High-res branded typography"], "Python PIL"),
        ("Smart Auto-Replies", "Bangla NLP", ["Contextual polite comment replies", "Spam filtering & sentiment check"], "Gemini Flash"),
        ("Messenger Concierge", "24/7 Active", ["Instant private message response", "Portfolio & contact inquiry router"], "Graph Webhooks")
    ]
)
