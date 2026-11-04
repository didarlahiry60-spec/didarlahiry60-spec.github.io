import os
from PIL import Image, ImageDraw, ImageFont

def make_perfect_poster(filename, app_name, url_bar, accent_color, hero_tag, hero_title, hero_desc, ui_cards, sidebar_items, status_text):
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (14, 17, 26, 255))
    draw = ImageDraw.Draw(im)

    font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_bengali = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"

    # Upgraded, prominent, large & ultra-crisp fonts
    f_title_main = ImageFont.truetype(font_bold, 38)
    f_title_b = ImageFont.truetype(font_bengali, 36)
    f_h2 = ImageFont.truetype(font_bold, 22)
    f_card_title = ImageFont.truetype(font_bold, 22)
    f_body = ImageFont.truetype(font_bold, 18)
    f_desc = ImageFont.truetype(font_bold, 18)
    f_tag = ImageFont.truetype(font_bold, 17)
    f_pill = ImageFont.truetype(font_bold, 17)
    f_sm = ImageFont.truetype(font_bold, 17)
    f_nav = ImageFont.truetype(font_bold, 18)
    f_browser = ImageFont.truetype(font_bold, 17)

    # 100% Solid Deep Black for text inside all colorful pills/boxes
    box_text_black = (0, 0, 0)
    # 100% Crisp Pure White for text on dark backgrounds
    text_white = (255, 255, 255)
    # Bright high-contrast light text for secondary labels
    text_bright_light = (230, 240, 255)

    # Outer Browser / OS Window Frame
    draw.rounded_rectangle([(25, 20), (1255, 700)], radius=16, fill=(18, 22, 34, 255), outline=(60, 75, 105, 255), width=2)

    # Top Window Bar
    draw.rounded_rectangle([(25, 20), (1255, 82)], radius=16, fill=(26, 32, 50, 255))
    draw.line([(25, 82), (1255, 82)], fill=(55, 68, 96, 255), width=1)

    # Window dots
    draw.ellipse([(50, 42), (66, 58)], fill=(255, 95, 87, 255))
    draw.ellipse([(76, 42), (92, 58)], fill=(254, 188, 46, 255))
    draw.ellipse([(102, 42), (118, 58)], fill=(40, 200, 64, 255))

    # Browser URL Address Bar
    draw.rounded_rectangle([(180, 34), (880, 68)], radius=8, fill=(13, 16, 26, 255), outline=(70, 88, 125, 255), width=1)
    draw.text((205, 41), f"https://{url_bar}", fill=text_bright_light, font=f_browser)

    # Window right status
    draw.text((930, 41), f"● {status_text}", fill=accent_color, font=f_browser)
    draw.text((1135, 41), "PROD v2.6", fill=text_bright_light, font=f_sm)

    # Left Sidebar (width: 255px)
    draw.rectangle([(25, 83), (280, 698)], fill=(16, 20, 32, 255))
    draw.line([(280, 83), (280, 698)], fill=(50, 62, 88, 255), width=1)

    # Sidebar Header
    draw.text((45, 110), app_name.upper(), fill=text_white, font=f_h2)
    draw.line([(45, 146), (260, 146)], fill=(50, 62, 88, 255), width=1)

    # Sidebar Navigation items
    y_nav = 165
    for idx, (label, is_active) in enumerate(sidebar_items):
        if is_active:
            # Active sidebar item: Solid colorful box with BOLD BLACK TEXT
            draw.rounded_rectangle([(40, y_nav - 6), (265, y_nav + 36)], radius=8, fill=accent_color)
            draw.text((54, y_nav + 4), label, fill=box_text_black, font=f_nav)
        else:
            # Inactive items: Bright, crisp, clearly legible
            draw.text((54, y_nav + 4), label, fill=text_bright_light, font=f_nav)
        y_nav += 48

    # Sidebar bottom system status
    draw.rounded_rectangle([(38, 575), (268, 668)], radius=10, fill=(24, 30, 48, 255), outline=(60, 75, 105, 255), width=1)
    draw.text((50, 590), "SYSTEM TELEMETRY", fill=text_bright_light, font=f_sm)
    
    # Status Pill: Solid colorful box with BOLD BLACK TEXT
    draw.rounded_rectangle([(48, 618), (258, 658)], radius=7, fill=accent_color)
    draw.text((60, 626), "99.98% High Uptime", fill=box_text_black, font=f_pill)

    # Main Workspace Hero Card (width: 920px: 305 to 1225)
    hero_box_x1, hero_box_x2 = 305, 1225
    draw.rounded_rectangle([(hero_box_x1, 110), (hero_box_x2, 280)], radius=14, fill=(22, 28, 44, 255), outline=(accent_color[0], accent_color[1], accent_color[2], 140), width=1)
    
    # Top Tag Pill: Solid colorful box with BOLD BLACK TEXT
    pill_text = f"★ {hero_tag.upper()}"
    bbox_pill = draw.textbbox((0, 0), pill_text, font=f_pill)
    text_w = bbox_pill[2] - bbox_pill[0]
    pill_x1 = 330
    pill_y1 = 126
    pill_x2 = pill_x1 + text_w + 32
    pill_y2 = pill_y1 + 38

    draw.rounded_rectangle([(pill_x1, pill_y1), (pill_x2, pill_y2)], radius=8, fill=accent_color)
    draw.text((pill_x1 + 16, pill_y1 + 8), pill_text, fill=box_text_black, font=f_pill)

    # Hero Title (Crisp pure white)
    draw.text((330, 180), hero_title[0], fill=text_white, font=f_title_main)
    if len(hero_title) > 1 and hero_title[1]:
        bbox = draw.textbbox((0, 0), hero_title[0], font=f_title_main)
        w_title = bbox[2] - bbox[0]
        draw.text((330 + w_title + 14, 182), hero_title[1], fill=accent_color, font=f_title_b)

    # Hero Subtitle (Crisp pure white, large 18 bold)
    max_desc_w = hero_box_x2 - 330 - 24 # 871px available
    bbox_desc = draw.textbbox((0, 0), hero_desc, font=f_desc)
    desc_w = bbox_desc[2] - bbox_desc[0]
    safe_desc = hero_desc
    if desc_w > max_desc_w:
        while desc_w > max_desc_w and len(safe_desc) > 5:
            safe_desc = safe_desc[:-2]
            bbox_desc = draw.textbbox((0, 0), safe_desc + "...", font=f_desc)
            desc_w = bbox_desc[2] - bbox_desc[0]
        safe_desc = safe_desc + "..."

    draw.text((330, 238), safe_desc, fill=text_white, font=f_desc)

    # 4 UI Content Dashboard Cards
    card_coords = [
        ((305, 305), (745, 475)),
        ((775, 305), (1225, 475)),
        ((305, 500), (745, 670)),
        ((775, 500), (1225, 670))
    ]

    for (c_tl, c_br), (c_title, c_badge, c_items, c_tag) in zip(card_coords, ui_cards):
        draw.rounded_rectangle([c_tl, c_br], radius=12, fill=(20, 26, 40, 255), outline=(58, 72, 102, 255), width=1)
        
        # Card header bar
        draw.rounded_rectangle([c_tl, (c_br[0], c_tl[1] + 46)], radius=12, fill=(28, 36, 56, 255))
        draw.line([(c_tl[0], c_tl[1] + 46), (c_br[0], c_tl[1] + 46)], fill=(58, 72, 102, 255), width=1)
        
        # Header text: Crisp Pure White Bold
        draw.text((c_tl[0] + 16, c_tl[1] + 10), c_title, fill=text_white, font=f_card_title)
        
        # Header right badge: Bold Accent Color
        bbox_b = draw.textbbox((0, 0), c_badge, font=f_sm)
        badge_w = bbox_b[2] - bbox_b[0]
        draw.text((c_br[0] - badge_w - 18, c_tl[1] + 13), c_badge, fill=accent_color, font=f_sm)

        # Content lines: Crisp Pure White Bold
        y_c = c_tl[1] + 58
        max_line_w = (c_br[0] - c_tl[0]) - 50
        for line in c_items:
            # Bullet dot
            draw.ellipse([(c_tl[0] + 16, y_c + 7), (c_tl[0] + 25, y_c + 16)], fill=accent_color)
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
            draw.text((c_tl[0] + 34, y_c), safe_line, fill=text_white, font=f_body)
            y_c += 30

        # Card bottom pill tag: Solid Colorful Box with BOLD BLACK TEXT
        bbox_tag = draw.textbbox((0, 0), c_tag, font=f_tag)
        tag_w = bbox_tag[2] - bbox_tag[0]
        tag_x1 = c_tl[0] + 16
        tag_y1 = c_br[1] - 40
        tag_x2 = min(tag_x1 + tag_w + 32, c_br[0] - 16)
        tag_y2 = tag_y1 + 32
        draw.rounded_rectangle([(tag_x1, tag_y1), (tag_x2, tag_y2)], radius=7, fill=accent_color)
        draw.text((tag_x1 + 16, tag_y1 + 6), c_tag, fill=box_text_black, font=f_tag)

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
    accent_color=(143, 211, 193),
    hero_tag="National Agriculture Telemetry",
    hero_title=("Kishan AI Platform", "(কৃষাণ)"),
    hero_desc="Live DAM Market Price Intelligence, 7-Day Weather Forecasts & Bengali Voice Assistant",
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
    accent_color=(255, 158, 187),
    hero_tag="Tactile Web Experience",
    hero_title=("Letter Portfolio Experience", ""),
    hero_desc="Interactive Envelope Metaphor, Tactile Stationery & 3D Desk in Next.js",
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
        ("Visual Aesthetics", "Clean Studio", ["Modern typography & dark tones", "Seamless browser responsiveness"], "CSS Hardware Accel")
    ]
)

# 3. AI Sales Agent - Soft Warm Amber / Dusk Peach (#f0a35e -> (240, 163, 94))
make_perfect_poster(
    filename="sales-bot-poster.webp",
    app_name="Sales Concierge",
    url_bar="agent.sales.telegram/console",
    accent_color=(240, 163, 94),
    hero_tag="Autonomous Telegram Concierge",
    hero_title=("E-Commerce AI Sales Agent", ""),
    hero_desc="Autonomous Telegram Sales Representative with Live Product Advice & Checkout",
    sidebar_items=[
        ("Autonomous Agent", True),
        ("Catalog & Sizing", False),
        ("Cart & Orders", False),
        ("Supervisor Handoff", False),
        ("Conversion Stats", False)
    ],
    status_text="24/7 STANDBY",
    ui_cards=[
        ("Conversational Engine", "Gemini 2.5", ["Multi-turn natural buyer advice", "Product suggestions & size guide"], "Gemini API"),
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
    accent_color=(147, 197, 253),
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
