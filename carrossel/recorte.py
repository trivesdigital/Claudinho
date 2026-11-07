#!/usr/bin/env python3
"""
RECORTE PARA CAPA — prepara a foto e o recorte da pessoa (que fica na frente do título).

Passo 1 · enquadrar e gerar a grade de coordenadas:
  python3 carrossel/recorte.py FOTO PASTA_CAPA [--y0 N]
    → PASTA_CAPA/foto.jpg  (1080×1350, corte 4:5; --y0 = linha do topo no original, padrão: centro)
    → PASTA_CAPA/grade.jpg (foto reduzida com grade de 100 px — use para ler as coordenadas)

Passo 2 · recortar a pessoa com um polígono (coordenadas da grade, em volta de cabeça/boné/mão):
  python3 carrossel/recorte.py --pessoa PASTA_CAPA "x,y x,y x,y ..." [--ate Y]
    → PASTA_CAPA/pessoa.png e PASTA_CAPA/previa-recorte.jpg (pessoa sobre magenta, para conferir)
    Dentro do polígono remove céu, folhas, telhado verde e neblina clara acima de --ate (padrão 800).
    Só importa a área onde o título passa; abaixo dela o recorte é igual à foto.
    --modo cor (padrão) · poligono (só o contorno) · pele (mão/braço: pele + manga escura abaixo de --manga Y) · escuro (boné/cabelo preto; fecha furos de logos)

Alternativa · tudo que não é céu fica na frente (bandeira, morro…):
  python3 carrossel/recorte.py --ceu PASTA_CAPA

Preto e branco com pretos profundos (rode DEPOIS do recorte; converte foto.jpg e pessoa.png):
  python3 carrossel/recorte.py --pb PASTA_CAPA

Aceita .heic (iPhone) se `pillow-heif` estiver instalado (pip install pillow-heif).
"""
import sys, json, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
try:
    import pillow_heif; pillow_heif.register_heif_opener()
except Exception:
    pass

def hsv(im):
    a = np.asarray(im.convert("HSV")).astype(float)
    return a[..., 0] * 360 / 255, a[..., 1] / 255, a[..., 2] / 255

def enquadrar(foto, pasta, y0=None):
    src = ImageOps.exif_transpose(Image.open(foto)).convert("RGB"); W, H = src.size
    pasta = Path(pasta); pasta.mkdir(parents=True, exist_ok=True)
    h = round(W * 1.25)
    if h <= H:
        y0 = (H - h) // 2 if y0 is None else max(0, min(H - h, y0)); box = (0, y0, W, y0 + h)
    else:
        w = round(H * .8); x0 = (W - w) // 2; box = (x0, 0, x0 + w, H)
    im = src.crop(box).resize((1080, 1350), Image.LANCZOS); im.save(pasta / "foto.jpg", quality=93)
    (pasta / "meta.json").write_text(json.dumps({"orig": str(Path(foto).resolve()), "box": list(box)}))
    g = im.copy(); d = ImageDraw.Draw(g)
    for x in range(0, 1080, 100): d.line([(x, 0), (x, 1350)], fill=(255, 0, 0), width=2); d.text((x + 4, 4), str(x), fill=(255, 0, 0))
    for y in range(0, 1350, 100): d.line([(0, y), (1080, y)], fill=(255, 0, 0), width=2); d.text((4, y + 4), str(y), fill=(255, 0, 0))
    g.resize((540, 675)).save(pasta / "grade.jpg", quality=80)
    print(f"ok → {pasta}/foto.jpg e {pasta}/grade.jpg (grade reduzida pela metade: multiplique as leituras por 2)")

def pessoa(pasta, pontos, ate=800, modo="cor"):
    """Recorte em alta resolução (foto original) e reduzido no fim → bordas nítidas."""
    pasta = Path(pasta); im = Image.open(pasta / "foto.jpg").convert("RGB")
    k, hi = 1.0, im
    meta = pasta / "meta.json"
    if meta.exists():
        m_ = json.loads(meta.read_text())
        try:
            hi = ImageOps.exif_transpose(Image.open(m_["orig"])).convert("RGB").crop(tuple(m_["box"])); k = hi.size[0] / 1080
        except Exception:
            hi, k = im, 1.0
    poly = [tuple(float(c) * k for c in p.split(",")) for p in pontos.split()]
    P = Image.new("L", hi.size, 0); ImageDraw.Draw(P).polygon(poly, fill=255); P = np.asarray(P) > 0
    h, s, v = hsv(hi); yy = np.arange(hi.size[1])[:, None] * np.ones((1, hi.size[0])); A = ate * k
    def fechar(b, r=21):
        r = int(r * k) | 1
        x = Image.fromarray((b * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(r)).filter(ImageFilter.MinFilter(r))
        return np.asarray(x) > 127
    def abrir(b, r=3):
        r = int(r * k) | 1
        x = Image.fromarray((b * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(r)).filter(ImageFilter.MaxFilter(r))
        return np.asarray(x) > 127
    ceu = (h > 195) & (h < 235) & (s > .35)
    if modo == "poligono": m = P
    elif modo == "escuro": m = P & (fechar(v < .42, 45) | (yy >= A))
    elif modo == "pele":
        manga = globals().get("MANGA_Y") or ate
        pele = ((h < 50) & (s > .15) & (v > .42)) | ((v < .30) & (yy >= manga * k))
        m = P & (fechar(abrir(pele, 3), 5) | (yy >= A))
    else:
        folha = (h > 55) & (h < 125) & (s > .45) & (v > .42); telhado = (h > 100) & (h < 170) & (s > .25)
        neblina = (v > .60) & (s < .42) & (yy < A)
        m = P & ~ceu & ~((folha | telhado | neblina) & (yy < A))
    mi = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(int(3 * k) | 1))
    mi = mi.filter(ImageFilter.GaussianBlur(.6 * k)).resize(im.size, Image.LANCZOS)   # borda nítida e suave
    rgba = im.convert("RGBA"); rgba.putalpha(mi); rgba.save(pasta / "pessoa.png")
    xs = [p[0] / k for p in poly]; ys = [p[1] / k for p in poly]
    box = (max(0, int(min(xs)) - 30), max(0, int(min(ys)) - 30), min(1080, int(max(xs)) + 30), min(int(ate) + 40, 1350))
    bg = Image.new("RGBA", im.size, (255, 0, 200, 255)); bg.alpha_composite(rgba)
    prev = bg.convert("RGB").crop(box); prev.thumbnail((500, 500)); prev.save(pasta / "previa-recorte.jpg", quality=85)
    print(f"ok → {pasta}/pessoa.png  (confira {pasta}/previa-recorte.jpg)")

def ceu(pasta):
    pasta = Path(pasta); im = Image.open(pasta / "foto.jpg").convert("RGB")
    h, s, v = hsv(im); sky = (h > 195) & (h < 235) & (s > .35) & (v > .45)
    m = Image.fromarray(np.where(sky, 0, 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
    ImageDraw.floodfill(m, (540, 5), 128)
    m = Image.fromarray(np.where(np.asarray(m) == 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8))
    rgba = im.convert("RGBA"); rgba.putalpha(m); rgba.save(pasta / "pessoa.png")
    print(f"ok → {pasta}/pessoa.png (tudo que não é céu)")

def pb(pasta):
    """P&B editorial: pretos profundos, meios-tons suaves, altas luzes limpas."""
    pasta = Path(pasta)
    lut = []
    for i in range(256):
        x = max(0.0, min(1.0, (i - 22) / (242 - 22)))      # ponto de preto/branco
        x = x ** 1.18                                         # meios-tons mais densos
        x = x * x * (3 - 2 * x) * .55 + x * .45               # curva em S suave
        lut.append(int(round(x * 255)))
    def conv(im):
        g = ImageOps.grayscale(im.convert("RGB")).point(lut)
        return g.convert("RGB")
    f = pasta / "foto.jpg"; conv(Image.open(f)).save(f, quality=94)
    p = pasta / "pessoa.png"
    if p.exists():
        im = Image.open(p).convert("RGBA"); a = im.getchannel("A"); out = conv(im).convert("RGBA"); out.putalpha(a); out.save(p)
    print(f"ok → {pasta} em P&B")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(1)
    if a[0] == "--pessoa":
        ate = int(a[a.index("--ate") + 1]) if "--ate" in a else 800
        modo = a[a.index("--modo") + 1] if "--modo" in a else "cor"
        if "--manga" in a: globals()["MANGA_Y"] = int(a[a.index("--manga") + 1])
        pessoa(a[1], a[2], ate, modo)
    elif a[0] == "--pb":
        pb(a[1])
    elif a[0] == "--ceu":
        ceu(a[1])
    else:
        y0 = int(a[a.index("--y0") + 1]) if "--y0" in a else None
        enquadrar(a[0], a[1], y0)
