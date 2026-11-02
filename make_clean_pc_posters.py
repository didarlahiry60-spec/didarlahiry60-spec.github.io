import os
from PIL import Image, ImageDraw, ImageFont

def make_perfect_poster(filename, app_name, url_bar, accent_color, hero_tag, hero_title, hero_desc, ui_cards, sidebar_items, status_text):
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (13, 17, 26, 255))
    draw = ImageDraw.Draw(im)

    # Fonts
    font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_bengali = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"

    f_title_main = ImageFont.truetype(font_bold, 40)
    f_title_b = ImageFont.truetype(font_bengali, 38)
    f_h2 = ImageFont.truetype(font_bold, 24)
    f_card_title = ImageFont.truetype(font_bold, 24)
    f_body = ImageFont.truetype(font_bold, 20)
    f_desc = ImageFont.truetype(font_bold, 21)
    f_tag = ImageFont.truetype(font_bold, 18)
    f_pill = ImageFont.truetype(font_bold, 16)
    f_sm = ImageFont.truetype(font_bold, 16)
    f_nav = ImageFont.truetype(font_bold, 18)
    f_browser = ImageFont.truetype(font_bold, 17)

    # Outer Browser / OS Window Frame
    draw.rounded_rectangle([(25, 20), (1255, 700)], radius=16, fill=(17, 22, 34, 255), outline=(55, 68, 96, 255), width=2)

    # Top Window Bar
    draw.rounded_rectangle([(25, 20), (1255, 80)], radius=16, fill=(24, 31, 48, 255))
    draw.line([(25, 80), (1255, 80)], fill=(50, 62, 88, 255), width=1)

    # Window dots
    draw.ellipse([(50, 42), (66, 58)], fill=(255, 95, 87, 255))
    draw.ellipse([(76, 42), (92, 58)], fill=(254, 188, 46, 255))
    draw.ellipse([(102, 42), (118, 58)], fill=(40, 200, 64, 255))

    # Browser URL Address Bar
    draw.rounded_rectangle([(180, 35), (880, 67)], radius=8, fill=(13, 17, 26, 255), outline=(70, 85, 115, 255), width=1)
    draw.text((205, 41), f"🔒  https://{url_bar}", fill=(225, 235, 250), font=f_browser)

    # Window right status
    draw.text((940, 41), f"● {status_text}", fill=accent_color, font=f_nav)
    draw.text((1140, 41), "PROD v2.6", fill=(180, 195, 220), font=f_sm)

    # Left Sidebar (width: 250px)
    draw.rectangle([(25, 81), (275, 698)], fill=(15, 19, 30, 255))
    draw.line([(275, 81), (275, 698)], fill=(45, 56, 80, 255), width=1)

    # Sidebar Header
    draw.text((50, 110), app_name.upper(), fill=(255, 255, 255), font=f_h2)
    draw.line([(50, 150), (250, 150)], fill=(45, 56, 80, 255), width=1)

    # Sidebar Navigation items
    y_nav = 170
    for idx, (icon, label, is_active) in enumerate(sidebar_items):
        if is_active:
            draw.rounded_rectangle([(40, y_nav - 5), (260, y_nav + 34)], radius=8, fill=(accent_color[0], accent_color[1], accent_color[2], 50), outline=accent_color, width=1)
            draw.text((55, y_nav + 2), f"{icon}  {label}", fill=(255, 255, 255), font=f_nav)
        else:
            draw.text((55, y_nav + 2), f"{icon}  {label}", fill=(180, 195, 220), font=f_nav)
        y_nav += 48

    # Sidebar bottom system status
    draw.rounded_rectangle([(40, 585), (260, 665)], radius=10, fill=(22, 28, 44, 255), outline=(55, 68, 96, 255), width=1)
    draw.text((55, 600), "SYSTEM TELEMETRY", fill=(170, 185, 215), font=f_sm)
    draw.text((55, 628), "99.98% High Uptime", fill=(74, 222, 128), font=f_tag)

    # Main Workspace (width: 955px)
    draw.rounded_rectangle([(305, 110), (1225, 275)], radius=14, fill=(22, 28, 44, 255), outline=(accent_color[0], accent_color[1], accent_color[2], 180), width=2)
    
    # DYNAMIC PILL WIDTH: measure text length so pill completely encloses the tag!
    pill_text = f"★ {hero_tag.upper()}"
    bbox_pill = draw.textbbox((0, 0), pill_text, font=f_pill)
    text_w = bbox_pill[2] - bbox_pill[0]
    pill_x1 = 330
    pill_y1 = 130
    pill_x2 = pill_x1 + text_w + 32
    pill_y2 = pill_y1 + 36

    # Solid vibrant background matching theme
    draw.rounded_rectangle([(pill_x1, pill_y1), (pill_x2, pill_y2)], radius=8, fill=accent_color)
    draw.text((pill_x1 + 16, pill_y1 + 8), pill_text, fill=(10, 15, 25), font=f_pill)

    # Hero Title
    draw.text((330, 178), hero_title[0], fill=(255, 255, 255), font=f_title_main)
    if len(hero_title) > 1 and hero_title[1]:
        bbox = draw.textbbox((0, 0), hero_title[0], font=f_title_main)
        w_title = bbox[2] - bbox[0]
        draw.text((330 + w_title + 14, 180), hero_title[1], fill=accent_color, font=f_title_b)

    # Hero Subtitle
    draw.text((330, 232), hero_desc, fill=(255, 255, 255), font=f_desc)

    # 4 UI Content Dashboard Cards
    card_coords = [
        ((305, 305), (745, 475)),
        ((775, 305), (1225, 475)),
        ((305, 500), (745, 670)),
        ((775, 500), (1225, 670))
    ]

    for (c_tl, c_br), (c_title, c_badge, c_items, c_tag) in zip(card_coords, ui_cards):
        draw.rounded_rectangle([c_tl, c_br], radius=12, fill=(19, 25, 38, 255), outline=(60, 75, 105, 255), width=2)
        
        # Card header bar
        draw.rounded_rectangle([c_tl, (c_br[0], c_tl[1] + 44)], radius=12, fill=(26, 34, 52, 255))
        draw.line([(c_tl[0], c_tl[1] + 44), (c_br[0], c_tl[1] + 44)], fill=(55, 68, 96, 255), width=1)
        
        # Header text
        draw.text((c_tl[0] + 16, c_tl[1] + 10), c_title, fill=(255, 255, 255), font=f_card_title)
        draw.text((c_br[0] - 130, c_tl[1] + 13), c_badge, fill=accent_color, font=f_sm)

        # Content lines
        y_c = c_tl[1] + 56
        for line in c_items:
            draw.ellipse([(c_tl[0] + 16, y_c + 7), (c_tl[0] + 24, y_c + 15)], fill=accent_color)
            draw.text((c_tl[0] + 32, y_c), line, fill=(255, 255, 255), font=f_body)
            y_c += 28

        # Card bottom pill tag dynamically sized
        bbox_tag = draw.textbbox((0, 0), c_tag, font=f_sm)
        tag_w = bbox_tag[2] - bbox_tag[0]
        tag_x1 = c_tl[0] + 16
        tag_y1 = c_br[1] - 34
        tag_x2 = tag_x1 + tag_w + 24
        tag_y2 = tag_br_y = c_br[1] - 8
        draw.rounded_rectangle([(tag_x1, tag_y1), (tag_x2, tag_y2)], radius=6, fill=accent_color)
        draw.text((tag_x1 + 12, tag_y1 + 5), c_tag, fill=(10, 15, 25), font=f_sm)

    # Save outputs
    out1 = os.path.join("/home/didar-lahiry/Antigravity/Target Portfolio 2/demos", filename)
    out2 = os.path.join("/home/didar-lahiry/Antigravity/Target Portfolio 2/public/demos", filename)
    im.convert("RGB").save(out1, "WEBP", quality=95)
    im.convert("RGB").save(out2, "WEBP", quality=95)
    print(f"Generated perfect poster: {out1} & {out2}")

# 1. Kishan
make_perfect_poster(
    filename="kishan-poster.webp",
    app_name="Kishan Dashboard",
    url_bar="kishan.agro.bd/live-market",
    accent_color=(74, 222, 128), # Bright Emerald
    hero_tag="National Agriculture Telemetry",
    hero_title=("Kishan AI Platform", "(কৃষাণ)"),
    hero_desc="Live DAM Market Price Intelligence, 7-Day Weather Forecasting & Bengali Voice Assistant.",
    sidebar_items=[
        ("📊", "Market Telemetry", True),
        ("🌦️", "Weather Advisory", False),
        ("🗣️", "Bangla TTS Voice", False),
        ("🚨", "Disaster Alert SMS", False),
        ("⚙️", "API Integrations", False)
    ],
    status_text="LIVE CONNECTED",
    ui_cards=[
        ("DAM Market Index", "64 Districts", ["Daily wholesale vs retail pricing", "Crop trend percentage tracking"], "FastAPI + Gemini AI"),
        ("Weather Forecast", "Open-Meteo", ["Hyper-local 7-day precipitation", "Crop-specific agronomic advice"], "Automated Cron"),
        ("Accessibility Audio", "Bangla TTS", ["Voice readouts of market rates", "One-tap audio bulletin player"], "Native Audio API"),
        ("Offline Storage", "SQLite DB", ["Full cache for rural connectivity", "Zero login guest access mode"], "Local Database")
    ]
)

# 2. Letter Portfolio
make_perfect_poster(
    filename="letter-portfolio-poster.webp",
    app_name="Letter Desktop",
    url_bar="portfolio.didarlahiry.com/desk",
    accent_color=(56, 189, 248), # Bright Sky Cyan
    hero_tag="Tactile Web Experience",
    hero_title=("Letter Portfolio Experience", ""),
    hero_desc="Physical envelope, paper stationery & tactile desk metaphor built in Next.js App Router.",
    sidebar_items=[
        ("✉️", "Stationery Desk", True),
        ("📂", "Story & Career", False),
        ("🛠️", "Tech Stack Folders", False),
        ("📬", "Direct Dispatch", False),
        ("⚙️", "Settings", False)
    ],
    status_text="60 FPS FLUID",
    ui_cards=[
        ("Envelope Metaphor", "Dynamic Tilt", ["Physics-based tilt & reactive drag", "Smooth tactile open animations"], "Framer Motion"),
        ("Modular Sections", "Instant Tabs", ["Personal story & project files", "Interactive skill stack cards"], "React + Tailwind"),
        ("High Performance", "100/100 Core", ["Zero-latency SSG static speed", "Sub-second load across mobile"], "Next.js App Router"),
        ("Visual Aesthetics", "Clean Studio", ["Modern typography and dark tones", "Seamless browser responsiveness"], "CSS Hardware Accel")
    ]
)

# 3. AI Sales Agent
make_perfect_poster(
    filename="sales-bot-poster.webp",
    app_name="Sales Concierge",
    url_bar="agent.sales.telegram/console",
    accent_color=(251, 113, 133), # Bright Coral Rose
    hero_tag="Autonomous Telegram Concierge",
    hero_title=("E-Commerce AI Sales Agent", ""),
    hero_desc="24/7 autonomous Telegram representative managing products, customer advice & live checkout.",
    sidebar_items=[
        ("🤖", "Autonomous Agent", True),
        ("🛍️", "Catalog & Sizing", False),
        ("📦", "Cart & Orders", False),
        ("👥", "Supervisor Handoff", False),
        ("📊", "Conversion Stats", False)
    ],
    status_text="24/7 STANDBY",
    ui_cards=[
        ("Conversational Engine", "Gemini 2.5", ["Multi-turn natural buyer advice", "Product suggestions and size guide"], "Gemini API"),
        ("Order Dispatch", "SQLite DB", ["Automated cart & checkout logger", "Customer address & order receipt"], "Python AsyncIO"),
        ("Supervisor Takeover", "Admin Mode", ["Live human takeover console", "Instant alert on high-value orders"], "Telegram Webhooks"),
        ("Sales Metrics", "+350% Speed", ["Instant response with zero wait", "Automated FAQ resolution 24/7"], "Cloud Automated")
    ]
)

# 4. FB Automation
make_perfect_poster(
    filename="fb-automation-poster.webp",
    app_name="Cloud Automation",
    url_bar="meta.graph.automation/dashboard",
    accent_color=(96, 165, 250), # Bright Electric Blue
    hero_tag="Autonomous Social Manager",
    hero_title=("Facebook 24/7 AI Automation", ""),
    hero_desc="Fully automated Facebook page manager: 3x daily AI posts, Pillow visual banners & Messenger chatbot.",
    sidebar_items=[
        ("⚡", "Auto Publishing", True),
        ("🎨", "Graphic Banners", False),
        ("💬", "Comment Engine", False),
        ("📩", "Messenger Concierge", False),
        ("📈", "Page Growth", False)
    ],
    status_text="SCHEDULE ACTIVE",
    ui_cards=[
        ("Scheduled Publishing", "3x Daily", ["AI trending tech post generation", "Scheduled automated cron release"], "APScheduler"),
        ("Dynamic Graphics", "Pillow", ["Topic-tailored banner rendering", "High-res branded typography"], "Python PIL"),
        ("Smart Auto-Replies", "Bangla NLP", ["Contextual polite comment replies", "Spam filtering & sentiment check"], "Gemini Flash"),
        ("Messenger Concierge", "24/7 Active", ["Instant private message response", "Portfolio & contact inquiry router"], "Graph Webhooks")
    ]
)
