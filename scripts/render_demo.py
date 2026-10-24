#!/usr/bin/env python3
"""Narasi2Video - contoh jalur render yang sudah teruji (PIL + ffmpeg, tanpa internet).

Memperagakan: latar, judul masuk, benda bergerak, Tingang pemandu, watermark
menyatu pada objek, footer tipis, subtitle, dan penutup 2 detik.
Pakai:  python3 render_demo.py keluaran.mp4 [audio.wav]
Ubah SCENES dan CLOSING untuk video sungguhan; logika gerak dipakai ulang.
"""
import math, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 24
HERE = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(HERE, "..", "assets", "tingang.svg")
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
if not os.path.exists(FONT):
    FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(sz): return ImageFont.truetype(FONT, sz)
def ease_out(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def ease_io(t): t = min(max(t, 0), 1); return 3 * t * t - 2 * t ** 3

# Satu scene = satu dict. Durasi nyata 9-10 detik; demo dipendekkan agar cepat.
SCENES = [
    dict(dur=4.0, judul="Apa itu\nProklamasi?", sub="Pernyataan kemerdekaan bangsa Indonesia",
         bg=("#1f8a48", "#0b3f24"), gaya="infografis"),
]
CLOSING = dict(dur=2.0, akun=["Instagram  @toto_gutomo", "TikTok  @toto.gutomo", "YouTube  TotoGutomo"])
WATERMARK = "totogutomo.com"

def tingang_png(path="/tmp/n2v_tingang.png", w=460):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", SVG,
                    "-vf", f"scale={w}:-1", "-pix_fmt", "rgba", "-frames:v", "1", path], check=True)
    return Image.open(path).convert("RGBA")

def gradient(c1, c2):
    a = Image.new("RGB", (1, H)); px = a.load()
    r1, g1, b1 = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    r2, g2, b2 = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    for y in range(H):
        k = y / (H - 1)
        px[0, y] = (int(r1 + (r2 - r1) * k), int(g1 + (g2 - g1) * k), int(b1 + (b2 - b1) * k))
    return a.resize((W, H))

def center_text(d, text, y, sz, fill, alpha=255, anchor_x=W // 2):
    f = font(sz)
    for i, line in enumerate(text.split("\n")):
        d.text((anchor_x, y + i * int(sz * 1.2)), line, font=f, fill=fill[:3] + (alpha,), anchor="mm")

def scene_frame(sc, t, bg, tg):
    img = bg.copy().convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    dur = sc["dur"]
    # Beat 1 (0-2 dtk) masuk | Beat 2 aksi | Beat 3 (dtk terakhir) keluar
    fade_out = 1 - ease_io((t - (dur - 0.5)) / 0.5) if t > dur - 0.5 else 1
    # Judul: geser masuk dari kiri dengan percepatan halus
    k = ease_out(t / 0.8)
    center_text(d, sc["judul"], 360, 120, (255, 255, 255, 255),
                alpha=int(255 * k * fade_out), anchor_x=int(W // 2 - (1 - k) * 500))
    # Objek "rumah" (papan) tempat watermark menyatu
    hx, hy = 220, 900
    pop = ease_out((t - 0.6) / 0.6)
    s = 0.6 + 0.4 * pop
    bw, bh = int(640 * s), int(380 * s)
    cx, cy = W // 2, hy + 190
    d.rounded_rectangle((cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2), 36,
                        fill=(255, 241, 200, int(255 * pop * fade_out)))
    d.polygon([(cx - bw // 2 - 30, cy - bh // 2), (cx, cy - bh // 2 - int(170 * s)), (cx + bw // 2 + 30, cy - bh // 2)],
              fill=(214, 58, 30, int(255 * pop * fade_out)))
    # Watermark menyatu: putih tipis di dinding objek (satu scene satu watermark)
    d.text((cx, cy + bh // 2 - 50), WATERMARK, font=font(34), fill=(255, 255, 255, int(110 * pop * fade_out)), anchor="mm")
    # Benda bergerak: bola menelusuri garis waktu (kiri ke kanan = waktu maju)
    mt = ease_io((t - 1.2) / 2.0)
    bx = 160 + mt * (W - 320); by = 1400
    d.line((160, by, W - 160, by), fill=(255, 255, 255, 120), width=8)
    d.ellipse((bx - 34, by - 34, bx + 34, by + 34), fill=(242, 183, 5, int(255 * fade_out)))
    # Tingang pemandu: melayang halus + bayangan alas (efek pseudo-3D)
    bob = math.sin(t * 3.2) * 14
    tx, ty = 150, 1470 - int(tg.size[1] * 0.45)
    sh = 1 - 0.08 * math.sin(t * 3.2)
    d.ellipse((tx + 30, 1532, tx + 30 + int(230 * sh), 1572), fill=(0, 0, 0, 80))
    img.alpha_composite(tg.resize((int(tg.size[0] * 0.62), int(tg.size[1] * 0.62))), (tx, int(ty + bob + 40)))
    # Subtitle: kata kunci aman layar, kontras jelas
    d.rounded_rectangle((90, 1660, W - 90, 1780), 28, fill=(0, 0, 0, int(140 * fade_out)))
    d.text((W // 2, 1720), sc["sub"], font=font(40), fill=(255, 255, 255, int(255 * fade_out)), anchor="mm")
    d.text((W // 2, 1870), WATERMARK, font=font(28), fill=(255, 255, 255, 120), anchor="mm")  # footer tipis
    return img.convert("RGB")

def closing_frame(c, t):
    img = gradient("#0b3f24", "#10122a").convert("RGBA"); d = ImageDraw.Draw(img, "RGBA")
    k = ease_out(t / 0.4)
    for i, a in enumerate(c["akun"]):
        d.text((W // 2, 800 + i * 150 + int((1 - k) * 60)), a, font=font(58), fill=(255, 255, 255, int(255 * k)), anchor="mm")
    d.text((W // 2, 1300), "Guru SMA Negeri 3 Maliku", font=font(40), fill=(242, 183, 5, int(255 * k)), anchor="mm")
    d.text((W // 2, 1870), WATERMARK, font=font(28), fill=(255, 255, 255, 120), anchor="mm")
    return img.convert("RGB")

def main(out, audio=None):
    tg = tingang_png()
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio: cmd += ["-i", audio, "-c:a", "aac", "-b:a", "128k", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for sc in SCENES:
        bg = gradient(*sc["bg"])
        for f in range(int(sc["dur"] * FPS)):
            p.stdin.write(scene_frame(sc, f / FPS, bg, tg).tobytes())
    for f in range(int(CLOSING["dur"] * FPS)):
        p.stdin.write(closing_frame(CLOSING, f / FPS).tobytes())
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
