#!/usr/bin/env python3
"""Gera os recursos visuais do site HCsoftware (logótipo, favicon, imagem OG)."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"
ORIGEM = RAIZ.parent / "StockWin11"

SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

AMBAR_1 = (255, 196, 107)
AMBAR_2 = (194, 118, 26)
TINTA = (58, 34, 5)
AZUL = (74, 144, 217)


def gradiente(tamanho: tuple[int, int], a: tuple[int, int, int], b: tuple[int, int, int]) -> Image.Image:
    largura, altura = tamanho
    base = Image.new("RGB", (1, altura))
    px = base.load()
    for y in range(altura):
        t = y / max(altura - 1, 1)
        px[0, y] = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
    return base.resize(tamanho, Image.Resampling.BICUBIC)


def com_cantos(imagem: Image.Image, raio: int) -> Image.Image:
    mascara = Image.new("L", imagem.size, 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, imagem.width - 1, imagem.height - 1), raio, fill=255)
    resultado = imagem.convert("RGBA")
    resultado.putalpha(mascara)
    return resultado


def favicon(lado: int) -> Image.Image:
    icone = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    fundo = com_cantos(gradiente((lado, lado), AMBAR_1, AMBAR_2), round(lado * 0.22))
    icone.alpha_composite(fundo)
    desenho = ImageDraw.Draw(icone)
    fonte = ImageFont.truetype(SERIF_BOLD, round(lado * 0.44))
    texto = "HC"
    caixa = desenho.textbbox((0, 0), texto, font=fonte)
    x = (lado - (caixa[2] - caixa[0])) / 2 - caixa[0]
    y = (lado - (caixa[3] - caixa[1])) / 2 - caixa[1] - lado * 0.015
    desenho.text((x, y), texto, font=fonte, fill=TINTA + (255,))
    return icone


def brilho(tamanho: tuple[int, int], centro: tuple[int, int], raio: int,
           cor: tuple[int, int, int], alpha: int) -> Image.Image:
    """Halo suave e sem bordas duras (máscara desfocada sobre cor sólida)."""
    margem = 300
    mascara = Image.new("L", (tamanho[0] + 2 * margem, tamanho[1] + 2 * margem), 0)
    cx, cy = centro[0] + margem, centro[1] + margem
    ImageDraw.Draw(mascara).ellipse((cx - raio, cy - raio, cx + raio, cy + raio), fill=alpha)
    mascara = mascara.filter(ImageFilter.GaussianBlur(raio * 0.55))
    mascara = mascara.crop((margem, margem, margem + tamanho[0], margem + tamanho[1]))
    camada = Image.new("RGBA", tamanho, cor + (255,))
    camada.putalpha(mascara)
    return camada


def malha(tamanho: tuple[int, int], passo: int = 44) -> Image.Image:
    camada = Image.new("RGBA", tamanho, (0, 0, 0, 0))
    desenho = ImageDraw.Draw(camada)
    for x in range(0, tamanho[0], passo):
        desenho.line([(x, 0), (x, tamanho[1])], fill=(255, 255, 255, 7), width=1)
    for y in range(0, tamanho[1], passo):
        desenho.line([(0, y), (tamanho[0], y)], fill=(255, 255, 255, 7), width=1)
    return camada


def imagem_og() -> Image.Image:
    largura, altura = 1200, 630
    base = Image.new("RGB", (largura, altura), (22, 22, 22)).convert("RGBA")
    base.alpha_composite(malha((largura, altura)))
    base.alpha_composite(brilho((largura, altura), (980, 90), 230, AZUL, 46))
    base.alpha_composite(brilho((largura, altura), (120, 420), 260, AMBAR_2, 34))

    desenho = ImageDraw.Draw(base)
    logo = Image.open(ORIGEM / "imagens" / "HCsoftware.png").convert("RGBA")
    escala = 46 / logo.height
    logo = logo.resize((round(logo.width * escala), 46), Image.Resampling.LANCZOS)
    base.alpha_composite(logo, (80, 56))

    titulo = ImageFont.truetype(SANS_BOLD, 64)
    desenho.multiline_text((80, 146), "Software gratuito,\npara todos.", font=titulo,
                           fill=(240, 240, 240, 255), spacing=6)

    subtitulo = ImageFont.truetype(SANS, 27)
    desenho.text((82, 312), "8 programas para Windows e Linux · HCsoftware",
                 font=subtitulo, fill=(165, 165, 165, 255))

    captura = Image.open(ORIGEM / "tools" / "capturas" / "escuro-painel.png").convert("RGBA")
    largura_captura = 1120
    altura_captura = round(captura.height * largura_captura / captura.width)
    captura = captura.resize((largura_captura, altura_captura), Image.Resampling.LANCZOS)
    captura = com_cantos(captura, 18)

    sombra = Image.new("RGBA", (largura_captura + 80, altura_captura + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((40, 40, 40 + largura_captura, 40 + altura_captura),
                                             20, fill=(0, 0, 0, 170))
    sombra = sombra.filter(ImageFilter.GaussianBlur(26))

    base.alpha_composite(sombra, (0, 356))
    base.alpha_composite(captura, (40, 376))
    ImageDraw.Draw(base).rounded_rectangle((40, 376, 40 + largura_captura, 376 + altura_captura),
                                           18, outline=(255, 255, 255, 30), width=1)

    return base.convert("RGB")


def principal() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(ORIGEM / "imagens" / "HCsoftware.png", ASSETS / "logo-hcsoftware.png")

    captura = Image.open(ORIGEM / "tools" / "capturas" / "escuro-painel.png").convert("RGB")
    captura = captura.resize((1280, round(captura.height * 1280 / captura.width)), Image.Resampling.LANCZOS)
    captura.save(ASSETS / "painel.webp", "WEBP", quality=86, method=6)

    favicon(64).save(ASSETS / "favicon.png")
    favicon(180).save(ASSETS / "apple-touch-icon.png")
    imagem_og().save(ASSETS / "og-image.png", optimize=True)

    for ficheiro in sorted(ASSETS.iterdir()):
        print(f"{ficheiro.name}: {ficheiro.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    principal()
