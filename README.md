# Claudinho

## Carrossel Zanellato — `carrossel/`

Gerador de carrosséis para Instagram (1080 × 1350) no estilo da referência "Marca Pessoal do zero":
capa sempre com foto, slides de texto/imagem e CTA obrigatório no final.

**Motor (recomendado):** um comando gera capa + slides + prévia + relatório de problemas:

```bash
node carrossel/gerar.js carrossel/carrosseis/03-follow-up/roteiro.json
```

Foto de capa e recorte da pessoa: `python3 carrossel/recorte.py` (veja as instruções no topo do arquivo).
Modelo de roteiro: `carrossel/carrosseis/_modelo/roteiro.json`. Fluxo e regras: `.claude/skills/carrossel/SKILL.md`.

**Editor no navegador (opcional):** abra `carrossel/index.html` para ajustar à mão e baixar os PNGs.

Regras de estilo detalhadas: [`carrossel/ESTILO.md`](carrossel/ESTILO.md).
