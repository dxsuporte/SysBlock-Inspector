#!/usr/bin/env python3
from PIL import Image, ImageDraw

def generate_sysblock_inspector_icon():
    size = 512
    # Cria uma imagem transparente (RGBA)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # Cores no padrão RGBA (Ciano do monitor, Grafite de fundo, Verde OK)
    color_accent = (156, 220, 254, 255) # Ciano Técnico
    color_bg = (45, 45, 45, 255)        # Cinza Grafite
    color_ok = (76, 189, 90, 255)        # Verde de Status OK
    color_grid = (55, 55, 55, 255)      # Linhas da Grade

    # 1. Escudo de Fundo Circular (Cinza Grafite Premium)
    draw.ellipse([cx - 230, cy - 230, cx + 230, cy + 230], fill=color_bg, outline=color_accent, width=12)

    # 2. Grade de Blocos de Sistema no Fundo (Representando "SysBlock")
    for i in range(-160, 161, 80):
        draw.line([cx + i, cy - 160, cx + i, cy + 160], fill=color_grid, width=3)
        draw.line([cx - 160, cy + i, cx + 160, cy + i], fill=color_grid, width=3)

    # 3. Trilhas de Circuito / Pinos de Conexão do Processador
    pins = [-180, -140, 140, 180]
    for p in pins:
        draw.line([cx + p, cy - 80, cx + p, cy + 80], fill=color_accent, width=6)
        draw.line([cx - 80, cy + p, cx + 80, cy + p], fill=color_accent, width=6)

    # 4. Encapsulamento Central do Chip de Silício
    s = 100
    draw.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(32, 32, 32, 255), outline=(255, 255, 255, 255), width=4)

    # 5. Nós de Auditoria Internos (Verde Alerta OK e Ciano)
    draw.ellipse([cx - 49, cy - 49, cx - 21, cy - 21], fill=color_ok)
    draw.ellipse([cx + 21, cy + 21, cx + 49, cy + 49], fill=color_ok)
    draw.ellipse([cx + 21, cy - 49, cx + 49, cy - 21], fill=color_accent)
    draw.ellipse([cx - 49, cy + 21, cx - 21, cy + 49], fill=color_accent)

    # 6. Retículo da Lente do Inspetor (Alvo de Varredura Sênior)
    draw.ellipse([cx - 155, cy - 155, cx + 155, cy + 155], fill=None, outline=color_accent, width=4)

    # Grava por cima do icon.png antigo de forma instantânea
    img.save("icon.png", "PNG")
    print("🎉 Ícone tecnológico premium gerado com sucesso instantâneo!")

if __name__ == "__main__":
    generate_sysblock_inspector_icon()
