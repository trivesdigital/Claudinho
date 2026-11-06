---
name: carrossel
description: Cria carrosséis do Zanellato (Instagram 1080×1350) com o motor do repositório. Use quando pedirem um carrossel novo, ajuste de carrossel, capa ou sugestão de tema.
---

# Carrossel Zanellato — motor de baixo custo

Objetivo: máxima qualidade com o mínimo de tokens. **Não leia** `index.html`, `capa-motor.html`, `gerar.js` nem `ESTILO.md` inteiros — tudo que é preciso está aqui.

## Fluxo (sempre nesta ordem)
1. **Aprovação antes de criar** (regra do usuário). Responda em texto, numa tabela curta: capa (layout + linhas), e por slide: título · desenho · Na prática · gancho; + CTA. Não gere nada antes do "ok".
2. Criar pasta `carrossel/carrosseis/NN-tema/` e escrever `roteiro.json` (copie o formato de `carrossel/carrosseis/_modelo/roteiro.json`).
3. Foto de capa (se houver):
   - `python3 carrossel/recorte.py FOTO carrossel/carrosseis/NN-tema/capa` → leia só `capa/grade.jpg` (coordenadas ×2).
   - `python3 carrossel/recorte.py --pessoa .../capa "x,y x,y …"` → polígono em volta de cabeça/boné/mão; confira só `previa-recorte.jpg`.
   - A última linha do título deve ter `base` ~40–60 px **abaixo do topo da cabeça/boné** (a pessoa cobre só a base das letras).
4. `node carrossel/gerar.js carrossel/carrosseis/NN-tema/roteiro.json` → relatório no terminal. Corrija os avisos no JSON e rode de novo.
5. Confira **apenas** `previa.jpg` (1 imagem). Só abra um slide individual se a prévia mostrar problema.
6. Commit + push; envie os PNGs ao usuário com `SendUserFile`.

## Regras de estilo (aprovadas pelo usuário)
- Público AAA, minimalista e elegante. Fundo branco na maioria; **1–2 slides** com `"tema":"escuro"` (verde Trives escuro, flat com granulado). Sem neon, sem logo, sem nome no topo, sem rodapé.
- Fontes: Poppins (texto), Anton/Archivo (capa), Caveat (letra de mão). Margens 128 px laterais / 150 px vertical (automático).
- Capa: foto colorida, **título grande**, pessoa recortada na frente da última linha, margem 80 px.
  Linhas encaixam sozinhas pela forma real das letras (acentos incluídos, sem encostar); se um acento bater, a linha de cima desliza até 90 px p/ a direita (`"encaixe": false` desliga).
  `espaco` (opcional, padrão 1) multiplica o espaço entre as linhas do título: 0.5 = mais junto, 1.5 = mais solto.
  Layouts: `riscado` (3 linhas: pequena · palavra riscada · gigante) · `padrao` (4: pequena espaçada · média · selo · gigante) · `dois-pesos` (3: pequena · fina · pesada) · `serifa` (3: pequena · itálico serifado · condensada).
- Slide de conteúdo = título + subtítulo (1 linha) + 1 frase curta com `[[círculo]]`/`{{sublinhado}}` + desenho + **Na prática** (`exemplo`, 1–2 linhas, situação real) + **gancho** (1 linha, sem ponto final, abre curiosidade p/ o próximo).
- Depois de dois-pontos: maiúscula (automático). Último slide sempre `cta` com palavra para comentar.
- Não invente dados como se fossem reais; números de exemplo devem soar ilustrativos.

## Desenhos (`desenho` + `rotulos` separados por `|`)
| desenho | rotulos |
|---|---|
| `alvo` | o que não funciona \| o que funciona |
| `funil` | topo \| furo 1 \| furo 2 \| furo 3 \| saída |
| `bolhas` | pequeno \| legenda \| grande \| legenda |
| `grafico` | eixo Y \| marca1, marca2, marca3 \| anotação |
| `pipeline` | etapa:número \| etapa:número \| etapa:número \| nota (número opcional; % é calculada) |
| `linha` | Dia 0:ação \| Dia 1:ação \| … (linha do tempo) |

## Linha editorial (base: Método Trives — dono para dono)
Comercial (follow-up, qualificação, reativação da base), gestão (CRM, números da semana, previsibilidade), visão de fundador (+1.200 clientes, 9 anos), tecnologia (IA de pré-vendas no WhatsApp), marketing × comercial integrados. **Não** usar "marca pessoal" como tema.
