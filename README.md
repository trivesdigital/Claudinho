# Claudinho

## Carrossel Zanellato — `carrossel/`

Gerador de carrosséis para Instagram (1080 × 1350) no estilo da referência "Marca Pessoal do zero":
capa sempre com foto, slides de texto/imagem e CTA obrigatório no final.

**Usar no navegador:** abra `carrossel/index.html`, edite os slides à esquerda, envie as fotos e clique em **Baixar PNGs (.zip)**.

**Exportar pela linha de comando** (precisa de `npm i playwright`):

```bash
node carrossel/exportar.js carrossel/exemplos/marca-pessoal.json
```

As imagens saem em `carrossel/saida/<nome>/01.png, 02.png…`. Fotos locais ficam em `carrossel/fotos/` (não vão para o git).

Regras de estilo, fontes e prompt de copy: [`carrossel/ESTILO.md`](carrossel/ESTILO.md).
