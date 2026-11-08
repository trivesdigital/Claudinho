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
   - `python3 carrossel/recorte.py --pessoa .../capa "x,y x,y …" [--modo cor|pele|escuro|poligono] [--ate Y] [--manga Y]` → confira só `previa-recorte.jpg`.
     Modos: `cor` (céu/folhas atrás) · `pele` (mão/braço sobre tela/mesa; manga escura abaixo de --manga) · `escuro` (boné/cabelo preto sobre fundo cinza) · `poligono` (só o contorno).
   - P&B com pretos profundos (preferência do usuário para fotos de capa): `python3 carrossel/recorte.py --pb .../capa` depois do recorte. HEIC funciona (pillow-heif).
   - Várias opções de capa: um JSON por opção com `{"capa":{…,"saida":"capa-x/capa.png"},"slides":[]}` + `node carrossel/gerar.js arquivo.json --so-capa`.
   - A última linha do título deve ter `base` ~40–60 px **abaixo do topo da cabeça/boné** (a pessoa cobre só a base das letras).
4. `node carrossel/gerar.js carrossel/carrosseis/NN-tema/roteiro.json` → relatório no terminal. Corrija os avisos no JSON e rode de novo.
5. Confira **apenas** `previa.jpg` (1 imagem). Só abra um slide individual se a prévia mostrar problema.
6. Commit + push; envie ao usuário **o `.zip` da pasta** (todos os slides de uma vez) com `SendUserFile`, em vez dos PNGs um a um.

## Regras de estilo (aprovadas pelo usuário)
- Público AAA, minimalista e elegante. Fundo branco na maioria; **1–2 slides** com `"tema":"escuro"` (verde Trives escuro, flat com granulado). Sem neon, sem logo, sem nome no topo, sem rodapé.
- Fontes: Poppins (texto), Anton/Archivo (capa), Caveat (letra de mão). Margens 128 px laterais / 150 px vertical (automático).
- Capa: foto P&B com pretos profundos (preferência atual), **título grande**, pessoa recortada na frente da última linha. **Respiro:** margem 120 px nas laterais e 150 px no topo (`margem`, `margem_topo`); o título se ajusta à largura útil.
  Linhas encaixam sozinhas pela forma real das letras (acentos incluídos, sem encostar); se um acento bater, a linha de cima desliza até 90 px p/ a direita (`"encaixe": false` desliga).
  Legibilidade (**só em capas P&B**, com `"pb": true`): máscara preta em toda a foto (`mascara`, padrão 0.18) + fade preto do topo até abaixo do título (`fade_forca` 0.66, `fade_extra` 300 px; `"fade": false` desliga). O recorte recebe o mesmo escurecimento. Capas coloridas: só o sombreado leve do topo (`escurecer`, padrão 0.2). `escala` (padrão 1) reduz/aumenta o título inteiro.
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
| `baloes` | fala \| legenda \| pensamento \| legenda |
| `escada` | degrau 1 \| degrau 2 \| degrau 3 \| nota |
| `balanca` | lado leve \| lado pesado (vence) |
| `cartoes` | título A \| texto A (✗) \| título B \| texto B (✓) |
| `troca` | você dá \| valor \| você recebe \| valor |

**Estilos especiais do manifesto** (`"estilo"`): `versiculo` (Instrument Serif itálico + aspas grandes + referência em caixa alta; `linha1` texto, `linha2` referência) · `paralelo` (`a1`/`a2` e `b1`/`b2`: palavra gigante em Anton + frase, separados por traço à mão) · `cta` (sem ícone por padrão — `"icone": true` liga o aviãozinho; `linha1` pergunta, `linha2` pedido, `linha3` @ em etiqueta).

**Cores do manifesto:** monocromático (branco/preto + cinza) para o texto; **verde só no traço do destaque** (`{{palavra}}` mantém a cor do texto; só o sublinhado à mão é verde `#12965A`, no fundo preto `#3FD18A`). Slides escuros do manifesto usam o fundo verde (`"tema":"escuro"`); `"preto"` existe mas o usuário prefere o verde. Handle: **@caiozanellato**.

**Manifesto (trilha viral):** `{"tipo":"manifesto","linha1":"frase forte","linha2":"contraponto (mais leve)","linha3":"opcional pequeno","desenho":"…","citacao":true,"cta":true}` — **manifesto é só tipografia** (o usuário achou os desenhos abstratos/ruins): frase grande centralizada + `{{palavra-chave}}` sublinhada à mão. Não usar desenho de código no manifesto. **Ilustração externa** (traço preto grosso estilo vetor, fundo branco — o usuário gera no GPT): salve em `carrosseis/<pasta>/ilustracoes/*.png` e use `"ilustracao": "ilustracoes/x.png"` no slide (fica abaixo do texto, fundo branco some com multiply).
Prompt-base para o usuário: "Estilo: ilustração em linha preta grossa e uniforme, estilo vetor (line art), traço limpo e contínuo, sem sombreado, sem hachura, sem cor, sem texto. Fundo branco puro. Composição minimalista, objeto centralizado com bastante espaço em branco ao redor. Formato 4:3, alta resolução." 

**Ilustrações dos carrosséis de dicas:** ícones **flat** (biblioteca Phosphor, peso `fill`, `npm i @phosphor-icons/core@2.1.1` no scratchpad) compostos num SVG 800×560: cinza `#C9C9C9` para o que não importa, preto `#1B1B1B`, e **verde `#12965A` só na opção que importa** (em slide verde: branco / branco 35% / `#3FD18A`). Campo `"ilustracao": "ilustracoes/x.svg"` em `conteudo` ou `manifesto`.
**Formato de dicas aprovado:** o do carrossel 02 (número + título, subtítulo legível, frase com marcação, ilustração, "Na prática" em caixa tingida, gancho). A 2ª imagem (contracapa) também precisa funcionar como capa (Instagram testa A/B). Ganchos podem pedir uma ação pontual ("Abre sua última proposta…").

**Nunca repetir a ilustração de um carrossel anterior** (regra do usuário). Se nenhum desenho existente servir sem repetir, crie um novo tipo em `index.html` (função `drawAll`) e registre aqui.
Já usados: 02 → alvo, funil, bolhas, grafico, pipeline · 03 → grafico, bolhas, linha, alvo, pipeline · 04 → baloes, escada, balanca, cartoes, troca.
**Fácil de entender:** títulos curtos e do dia a dia; uma ideia por slide; "Na prática" como diálogo (**Cliente:** / **Você:**).

## Linha editorial Zanellato
Público: donos de empresas de **10 a 200 funcionários**, **multissegmento** (falar com dores comuns a qualquer setor).
**5 pilares, equilibrados** (vendas é só um deles): **Negócios · IA · Gestão · Vendas · Marketing**.
Hook no formato que funcionou: curto (≤ 6 palavras), virada **"não é X, é Y"** com palavra riscada + palavra gigante, ou "O que N anos/clientes me ensinaram sobre X".
Já publicados: marca pessoal (não repetir o tema), +1.200 clientes/crescer, follow-up, desconto/confiança.
