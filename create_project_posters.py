import os
from PIL import Image, ImageDraw, ImageFont

def make_poster(filename, title, category, subtitle, features, tech_stack, accent_color, bg_gradient_colors, icon_symbol="⚡"):
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (11, 14, 23, 255))
    draw = ImageDraw.Draw(im)

    # Background gradient
    c1, c2 = bg_gradient_colors
    for y in range(h):
        r = int(c1[0] + (c2[0] - c1[0]) * (y / h))
        g = int(c1[1] + (c2[1] - c1[1]) * (y / h))
        b = int(c1[2] + (c2[2] - c1[2]) * (y / h))
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Grid lines
    grid_color = (255, 255, 255, 12)
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=grid_color, width=1)

    # Glowing decorative orb top-right
    orb = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    orb_draw = ImageDraw.Draw(orb)
    for radius in range(350, 0, -10):
        alpha = int(35 * (1 - radius / 350))
        orb_draw.ellipse(
            [(950 - radius, 220 - radius), (950 + radius, 220 + radius)],
            fill=(accent_color[0], accent_color[1], accent_color[2], alpha)
        )
    im = Image.alpha_composite(im, orb)
    draw = ImageDraw.Draw(im)

    # Fonts
    font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_sans = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
    font_bengali = "/usr/share/fonts/truetype/noto/NotoSansBengali-Bold.ttf"

    title_font = ImageFont.truetype(font_bengali if any(ord(c) > 2000 for c in title) else font_bold, 52)
    cat_font = ImageFont.truetype(font_bold, 18)
    sub_font = ImageFont.truetype(font_sans, 24)
    feat_font = ImageFont.truetype(font_sans, 20)
    tag_font = ImageFont.truetype(font_bold, 17)
    code_font = ImageFont.truetype(font_bold, 16)

    # Left Container Card
    draw.rounded_rectangle([(60, 60), (1220, 660)], radius=24, outline=(255, 255, 255, 30), width=2)
    # Header bar
    draw.rounded_rectangle([(60, 60), (1220, 125)], radius=24, fill=(15, 20, 32, 220))
    draw.line([(60, 125), (1220, 125)], fill=(255, 255, 255, 25), width=2)

    # Window dots
    draw.ellipse([(90, 85), (106, 101)], fill=(255, 95, 87, 255))
    draw.ellipse([(118, 85), (134, 101)], fill=(254, 188, 46, 255))
    draw.ellipse([(146, 85), (162, 101)], fill=(40, 200, 64, 255))

    # Header title
    draw.text((180, 80), f"didarlahiry / {filename.replace('-poster.webp', '')}", fill=(180, 190, 210), font=code_font)
    draw.text((1020, 80), "LIVE SHOWCASE", fill=accent_color, font=code_font)

    # Category Pill
    pill_w = 260
    draw.rounded_rectangle([(90, 160), (90 + pill_w, 200)], radius=12, fill=(accent_color[0], accent_color[1], accent_color[2], 40), outline=accent_color, width=2)
    draw.text((115, 169), f"● {category.upper()}", fill=accent_color, font=cat_font)

    # Main Title
    draw.text((90, 220), title, fill=(255, 255, 255), font=title_font)

    # Subtitle
    draw.text((90, 290), subtitle, fill=(180, 190, 210), font=sub_font)

    # Features
    y_pos = 350
    for feat in features:
        draw.ellipse([(92, y_pos + 6), (104, y_pos + 18)], fill=accent_color)
        draw.text((120, y_pos), feat, fill=(230, 235, 245), font=feat_font)
        y_pos += 42

    # Tech Stack Tags (Bottom Left)
    x_tag = 90
    y_tag = 580
    for tag in tech_stack:
        bbox = draw.textbbox((0, 0), tag, font=tag_font)
        tw = bbox[2] - bbox[0]
        draw.rounded_rectangle([(x_tag, y_tag), (x_tag + tw + 28, y_tag + 40)], radius=8, fill=(255, 255, 255, 18), outline=(255, 255, 255, 40), width=1)
        draw.text((x_tag + 14, y_tag + 9), tag, fill=(240, 245, 255), font=tag_font)
        x_tag += tw + 40

    # Right Side Graphic Frame (Mockup window)
    draw.rounded_rectangle([(770, 160), (1190, 620)], radius=18, fill=(13, 17, 28, 240), outline=(255, 255, 255, 35), width=2)
    # Graphic Header
    draw.rounded_rectangle([(770, 160), (1190, 210)], radius=18, fill=(20, 26, 42, 255))
    draw.line([(770, 210), (1190, 210)], fill=(255, 255, 255, 20), width=1)
    draw.text((800, 174), f"SYSTEM PREVIEW // {category.upper()}", fill=(160, 175, 200), font=code_font)

    # Inner preview area with glow
    draw.rounded_rectangle([(795, 230), (1165, 595)], radius=14, fill=(18, 24, 38, 255), outline=(accent_color[0], accent_color[1], accent_color[2], 100), width=2)
    
    # Graphic lines inside preview
    draw.text((820, 255), f"Status: ACTIVE [2026]", fill=(74, 222, 128), font=code_font)
    draw.text((820, 290), f"Orchestrator: Autonomous Agent", fill=(200, 210, 230), font=code_font)
    draw.line([(820, 325), (1140, 325)], fill=(255, 255, 255, 20), width=1)

    # Visual data points
    draw.rounded_rectangle([(820, 350), (1140, 420)], radius=10, fill=(accent_color[0], accent_color[1], accent_color[2], 25))
    draw.text((838, 365), f"CORE: {tech_stack[0]} + {tech_stack[1]}", fill=accent_color, font=tag_font)
    draw.text((838, 392), f"RELIABILITY: 99.9% UPTIME", fill=(190, 205, 225), font=code_font)

    draw.rounded_rectangle([(820, 440), (1140, 510)], radius=10, fill=(255, 255, 255, 10))
    draw.text((838, 455), f"PIPELINE: Real-time Execution", fill=(255, 255, 255), font=tag_font)
    draw.text((838, 482), f"SECURITY: Verified & Sandboxed", fill=(160, 175, 200), font=code_font)

    # Save
    out_path = os.path.join("/home/didar-lahiry/Antigravity/Target Portfolio 2/demos", filename)
    im.convert("RGB").save(out_path, "WEBP", quality=90)
    print(f"Generated {out_path}")

# Generate the 4 project posters
make_poster(
    filename="kishan-poster.webp",
    title="Kishan (কৃষাণ) AI Platform",
    category="AI Agro-Intelligence",
    subtitle="National DAM market prices, hyper-local weather & Bangla voice assistant.",
    features=[
        "Live DAM wholesale vs retail daily crop prices & trend intelligence",
        "Hyper-local 7-day weather forecasting & crop-specific agronomic advisory",
        "Bengali Text-to-Speech (TTS) voice accessibility for audio broadcast",
        "Automated disaster SMS alerts & offline-first cross-platform caching"
    ],
    tech_stack=["Flutter", "Python", "FastAPI", "Gemini AI", "Open-Meteo"],
    accent_color=(34, 197, 94), # Emerald
    bg_gradient_colors=((10, 25, 20), (12, 16, 26))
)

make_poster(
    filename="letter-portfolio-poster.webp",
    title="Letter Portfolio Experience",
    category="Interactive Web App",
    subtitle="Physical envelope & folder desk metaphor with fluid reactive animation.",
    features=[
        "Tactile stationary aesthetic: interactive envelopes, pull-out tabs & stickers",
        "Dynamic physics-based tilt and gesture interactions across desktop & mobile",
        "Modular reactive sections: personal story, tech stack, and instant contact",
        "Zero-latency Static Generation (SSG) built for ultra-fast load speed"
    ],
    tech_stack=["Next.js", "TypeScript", "React", "Tailwind CSS", "Framer Motion"],
    accent_color=(6, 182, 212), # Cyan
    bg_gradient_colors=((12, 25, 35), (10, 14, 24))
)

make_poster(
    filename="sales-bot-poster.webp",
    title="E-Commerce AI Sales Agent",
    category="Autonomous Agent",
    subtitle="24/7 intelligent Telegram sales representative & customer support bot.",
    features=[
        "Autonomous product advisory, customer inquiry handling & size consulting",
        "Multi-turn conversational sales engine powered by Google Gemini 2.5 Flash",
        "Automated customer order capture, cart tracking & relational SQLite logging",
        "Live supervisor monitoring dashboard with seamless manual agent takeover"
    ],
    tech_stack=["Python", "Gemini 2.5 Flash", "Telegram Bot API", "SQLite", "AsyncIO"],
    accent_color=(236, 72, 153), # Pink/Rose
    bg_gradient_colors=((30, 12, 24), (12, 14, 25))
)

make_poster(
    filename="fb-automation-poster.webp",
    title="Facebook 24/7 AI Automation",
    category="Autonomous Cloud Worker",
    subtitle="Automated Facebook page manager: 3x daily AI posts, banners & chatbot.",
    features=[
        "Autonomous 3x daily post publisher with scheduled AI trending tech updates",
        "Automated visual graphic banner generation tailored per topic via Pillow",
        "Contextual AI comment auto-responder in warm, professional Bengali",
        "24/7 direct Messenger AI customer concierge with zero human intervention"
    ],
    tech_stack=["Python", "Facebook API", "Gemini AI", "Pillow", "APScheduler"],
    accent_color=(59, 130, 246), # Electric Blue
    bg_gradient_colors=((15, 20, 38), (11, 14, 23))
)
