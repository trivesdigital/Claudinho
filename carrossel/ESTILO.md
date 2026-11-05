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
- Capa: promessa + "do zero" / "em X dias". Uma palavra gigante, poucas palavras ao redor.
- Cada slide de conteúdo: **um** ensinamento. Título no imperativo curto ("Documente, não performe"), subtítulo com a tensão, corpo de 2 a 4 frases curtas.
- Feche cada slide com uma frase de contraste ("Viral é acidente. Valor é intenção.").
- Máx. ~330 caracteres de corpo por slide.
- CTA: frase-resumo em 2 linhas curtas + "Salva esse post e segue @...".

## Prompt para gerar o roteiro com IA
> Escreva um carrossel no estilo Zanellato sobre **[TEMA]**, em JSON no formato de `exemplos/marca-pessoal.json`.
> Slide 1 tipo "capa" (pre / linha1 / linha2 gigante / pos). De 4 a 6 slides "conteudo" numerados 01, 02…, cada um com título imperativo curto, subtítulo com a tensão e corpo de até 330 caracteres (pode usar `itens`). Último slide tipo "cta" com kicker "O resumo", título em 2 linhas de contraste, texto de 1 frase e chamada "**Salva esse post e segue** {handle}". Português do Brasil, frases curtas, sem emoji.

## Capa (recorte, minimalista)
Perfil chique, público AAA: menos é mais. Composição em camadas (`carrosseis/<nome>/capa/capa.html`):
foto → texto → recorte da foto (tudo que não é céu), então o texto fica **atrás** da bandeira/mastro/morro.
- Chamada em caixa alta pequena (Poppins 400, 19 px, espaçamento .46em)
- Título em Poppins 200 + palavra-chave em Poppins 300 itálico, centralizado, ~800 px de largura
- Complemento ("— DO ZERO") pequeno, alinhado ao fim do título, em área limpa
- Tudo branco. Sem selos, sem neon, sem pesos pesados
- Margem de segurança de 80 px em todos os lados
O slide 1 do roteiro usa `"tipo": "pronta"` apontando para `capa/capa.png`.
