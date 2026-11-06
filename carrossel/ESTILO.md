# Estilo de carrossel — Zanellato

Baseado exclusivamente na referência "Como eu construiria uma Marca Pessoal do zero".

## Regras fixas
1. **Slide 1 = CAPA com foto** (obrigatório). Foto cheia, título gigante empilhado em branco.
2. **Slides do meio** = conteúdo (texto, lista, imagem opcional) ou foto cheia com texto.
3. **Último slide = CTA** (obrigatório). Resumo em serifa + chamada com o @.
4. Formato 1080 × 1350 (4:5). Ideal: 6 a 9 slides.

O gerador avisa (e pede confirmação ao exportar) se a capa não tem foto ou se o CTA não está no final.

## Visual
| Elemento | Especificação |
|---|---|
| Fundo | Branco `#FFF` com grade fina na maioria; 1 ou 2 slides em verde Trives escuro `#10241D` flat com granulado leve (vintage), sem grade e sem gradiente |
| Texto | Preto `#111` no branco · branco no verde |
| Destaque | Discreto: verde escuro `#14291F` no branco · champanhe `#D9CFB8` no verde. Sem neon. Fotos sempre coloridas |
| Topo | Nada (sem logo e sem nome) |
| Rodapé | Nenhum (opcional por slide, só texto) |

## Tipografia
| Uso | Fonte |
|---|---|
| Títulos, subtítulos, corpo | **Poppins** (700 / 400) |
| Título da capa | **Archivo** 800, entrelinha bem apertada |
| Título do resumo/CTA | **Poppins** 700 |
| Chamada pequena | **Poppins** 600, caixa alta, espaçamento largo |

## Tipos de slide
- **capa**: `foto` (obrigatória), `recorte` (PNG da pessoa sem fundo, mesmo enquadramento da foto, para a pessoa ficar **na frente** do título como na referência), `pre` (texto pequeno), `linha1`, `linha2` (gigante), `pos`, `posicao` (topo/meio/base).
- **conteudo**: `numero` ("03"), `titulo`, `subtitulo`, `imagem` + `imagem2` (1 imagem única ou 2 lado a lado), `posicao_imagem`, `altura`, `legenda`, `texto`, `itens`, `texto_final`.
- **foto**: foto cheia com `kicker`, `titulo` e `texto` por cima.
- **cta**: `kicker` ("O resumo"), `titulo`, `texto`, `chamada` (use `{handle}`), `foto` redonda opcional.

### Listas (`itens`, uma por linha)
- `Educação | ensinar algo prático` → **Educação** · descrição em cinza
- `1. Sobre o que você fala? (3 a 5 temas)` → **1.** pergunta (parênteses em cinza)

### Formatação no texto
`**negrito**` · `*cor de destaque*` · `_serifa itálica_` · linha em branco = novo parágrafo.

## Escrita (copy)
- **Depois de dois-pontos, sempre letra maiúscula** (aplicado automaticamente em todo texto).
- Capa: promessa + "do zero" / "em X dias". Uma palavra gigante, poucas palavras ao redor.
- Cada slide de conteúdo: **um** ensinamento. Título no imperativo curto ("Documente, não performe"), subtítulo com a tensão, corpo de 2 a 4 frases curtas.
- Feche cada slide com uma frase de contraste ("Viral é acidente. Valor é intenção.").
- Máx. ~330 caracteres de corpo por slide.
- CTA: frase-resumo em 2 linhas curtas + "Salva esse post e segue @...".

## Prompt para gerar o roteiro com IA
> Escreva um carrossel no estilo Zanellato sobre **[TEMA]**, em JSON no formato de `exemplos/marca-pessoal.json`.
> Slide 1 tipo "capa" (pre / linha1 / linha2 gigante / pos). De 4 a 6 slides "conteudo" numerados 01, 02…, cada um com título imperativo curto, subtítulo com a tensão e corpo de até 330 caracteres (pode usar `itens`). Último slide tipo "cta" com kicker "O resumo", título em 2 linhas de contraste, texto de 1 frase e chamada "**Salva esse post e segue** {handle}". Português do Brasil, frases curtas, sem emoji.

## Capa (hook em destaque + recorte da pessoa)
Objetivo: parar o scroll sendo elegante. O hook é o herói.
- Camadas (`carrosseis/<nome>/capa/capa.html`): foto → título → **recorte só da pessoa** (`pessoa.png`) → selo.
  A pessoa (boné, mão) fica **na frente** da palavra gigante; árvores/fundo ficam atrás.
- Hierarquia por tamanho: chamada pequena espaçada (Poppins 500, caixa alta) → palavra média (Anton) → **palavra gigante** (Anton, largura total entre margens) com leve sobreposição.
- Selo em itálico (Poppins 500) branco sólido com texto escuro, levemente inclinado, encaixado entre as linhas.
- Tudo branco/neutro, sem neon. Margem de segurança de 80 px.
- Referências de tipografia: contraste de peso/estilo, escala extrema, palavras pequenas encaixadas nos vãos.
O slide 1 do roteiro usa `"tipo": "pronta"` apontando para `capa/capa.png`.

## Storyboard (curiosidade slide a slide)
- Todo slide de conteúdo termina com um **gancho** (`"gancho"`): uma frase em letra de mão (Caveat) + seta desenhada,
  que abre uma pergunta respondida só no slide seguinte. Uma linha, sem ponto final. Ex.: "E o maior vazamento nem está no anúncio".
- **Desenhos à mão** (`"desenho"` + `"rotulos"` separados por `|`), estilo rabisco (rough.js):
  `alvo` (lista riscada → alvo), `funil` (funil com furos), `bolhas` (pequeno vs grande), `grafico` (curva caindo), `pipeline` (3 etapas).
- **Exemplo concreto** (`"exemplo"`): nota em letra de mão numa moldura desenhada com fita, logo acima do gancho. Uma situação real, curta.
- Desenhos disponíveis: `alvo` (lista riscada → alvo com dardo), `funil` (leads entrando, furos pingando R$), `iceberg` (ponta = cliente novo, base submersa),
  `grafico` (curva caindo com marcadores quente/morno/frio — rótulos: eixo|tempos|anotação|marcadores), `pipeline` (rótulos `nome:número`, calcula a % entre etapas), `bolhas`.
- Marcações no texto: `[[palavra]]` = círculo à mão · `{{palavra}}` = sublinhado à mão.
- **Menos é mais:** cada slide = título + subtítulo (1 linha) + desenho simples + exemplo + gancho. Sem parágrafo extra.
- Desenhos limpos: traço pouco tremido, poucos rótulos, um único elemento na cor de destaque. Sem bonequinhos, hachuras ou enfeites.
- Um desenho por slide no máximo; ele ocupa o espaço livre entre o texto e o gancho, centralizado.
- **Margens:** 128 px nas laterais e 150 px em cima e embaixo. Tudo alinhado à mesma margem esquerda.
- **Gancho:** sempre na mesma posição (embaixo, alinhado à esquerda com o texto), letra de mão + seta curta; só o traço da seta varia levemente.
