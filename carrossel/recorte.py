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

Alternativa · tudo que não é céu fica na frente (bandeira, morro…):
  python3 carrossel/recorte.py --ceu PASTA_CAPA
"""
import sys, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

def hsv(im):
    a = np.asarray(im.convert("HSV")).astype(float)
    return a[..., 0] * 360 / 255, a[..., 1] / 255, a[..., 2] / 255

def enquadrar(foto, pasta, y0=None):
    src = Image.open(foto).convert("RGB"); W, H = src.size
    pasta = Path(pasta); pasta.mkdir(parents=True, exist_ok=True)
    h = round(W * 1.25)
    if h <= H:
        y0 = (H - h) // 2 if y0 is None else max(0, min(H - h, y0)); box = (0, y0, W, y0 + h)
    else:
        w = round(H * .8); x0 = (W - w) // 2; box = (x0, 0, x0 + w, H)
    im = src.crop(box).resize((1080, 1350), Image.LANCZOS); im.save(pasta / "foto.jpg", quality=93)
    g = im.copy(); d = ImageDraw.Draw(g)
    for x in range(0, 1080, 100): d.line([(x, 0), (x, 1350)], fill=(255, 0, 0), width=2); d.text((x + 4, 4), str(x), fill=(255, 0, 0))
    for y in range(0, 1350, 100): d.line([(0, y), (1080, y)], fill=(255, 0, 0), width=2); d.text((4, y + 4), str(y), fill=(255, 0, 0))
    g.resize((540, 675)).save(pasta / "grade.jpg", quality=80)
    print(f"ok → {pasta}/foto.jpg e {pasta}/grade.jpg (grade reduzida pela metade: multiplique as leituras por 2)")

def pessoa(pasta, pontos, ate=800):
    pasta = Path(pasta); im = Image.open(pasta / "foto.jpg").convert("RGB")
    poly = [tuple(map(float, p.split(","))) for p in pontos.split()]
    P = Image.new("L", im.size, 0); ImageDraw.Draw(P).polygon(poly, fill=255); P = np.asarray(P) > 0
    h, s, v = hsv(im); yy = np.arange(im.size[1])[:, None] * np.ones((1, im.size[0]))
    ceu = (h > 195) & (h < 235) & (s > .35)
    folha = (h > 55) & (h < 125) & (s > .45) & (v > .42)
    telhado = (h > 100) & (h < 170) & (s > .25)
    neblina = (v > .60) & (s < .42) & (yy < ate)
    m = P & ~ceu & ~((folha | telhado | neblina) & (yy < ate))
    mi = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
    mi = mi.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
    rgba = im.convert("RGBA"); rgba.putalpha(mi); rgba.save(pasta / "pessoa.png")
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    box = (max(0, int(min(xs)) - 30), max(0, int(min(ys)) - 30), min(1080, int(max(xs)) + 30), min(int(ate) + 40, 1350))
    bg = Image.new("RGBA", im.size, (255, 0, 200, 255)); bg.alpha_composite(rgba)
    prev = bg.convert("RGB").crop(box); prev.thumbnail((500, 500)); prev.save(pasta / "previa-recorte.jpg", quality=80)
    print(f"ok → {pasta}/pessoa.png  (confira {pasta}/previa-recorte.jpg)")

def ceu(pasta):
    pasta = Path(pasta); im = Image.open(pasta / "foto.jpg").convert("RGB")
    h, s, v = hsv(im); sky = (h > 195) & (h < 235) & (s > .35) & (v > .45)
    m = Image.fromarray(np.where(sky, 0, 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
    ImageDraw.floodfill(m, (540, 5), 128)
    m = Image.fromarray(np.where(np.asarray(m) == 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8))
    rgba = im.convert("RGBA"); rgba.putalpha(m); rgba.save(pasta / "pessoa.png")
    print(f"ok → {pasta}/pessoa.png (tudo que não é céu)")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(1)
    if a[0] == "--pessoa":
        ate = int(a[a.index("--ate") + 1]) if "--ate" in a else 800
        pessoa(a[1], a[2], ate)
    elif a[0] == "--ceu":
        ceu(a[1])
    else:
        y0 = int(a[a.index("--y0") + 1]) if "--y0" in a else None
        enquadrar(a[0], a[1], y0)
