# Escopo — Coleção TikZ

Repositório central para organizar, versionar e publicar as figuras TikZ
usadas (ou reaproveitáveis) nas diversas disciplinas/projetos de pesquisa
em `GitRTx` (CircuitosCA, ControleClássico, ControleDigital,
ControleEstados, MetodosNumericos, Identificação, Koopman, MPC-DMC, ...).

Hoje cada projeto guarda suas próprias figuras em
`Notas/imgs/tikz/*.tikz`, sem catálogo comum — o levantamento inicial
encontrou **43 arquivos `.tikz`** espalhados em 6 projetos, incluindo
variações de um mesmo tema redesenhadas em projetos diferentes (ex.:
`MassaMolaAmortecedor.tikz` existe em 3 projetos, com diferenças reais
entre elas — não são cópias idênticas). Este repositório resolve isso:
um lugar único, categorizado por tema, com preview e download em vários
formatos.

## Objetivos da v1

1. **Coleção organizada por categoria/tema de pesquisa** — cada figura é
   um arquivo `.tikz` (só o corpo `tikzpicture`, no mesmo formato já usado
   nos projetos) + um arquivo de metadados `.meta.yml` (título, descrição,
   tags).
2. **Pipeline de build automático**: cada `.tikz` vira um documento
   standalone compilável e é convertido para **PNG** (raster, alta
   densidade), **SVG** (vetor, para web) e **EPS** (vetor, para LaTeX/
   publicações), além do **PDF** intermediário.
3. **Site Quarto navegável por tema/categoria**, seguindo o mesmo padrão
   visual do [`TemplateNotas`](../TemplateNotas) (mesma `_quarto.yml` /
   SCSS), com uma página por categoria mostrando um grid de cards. Cada
   card tem: preview em PNG, título/descrição/tags, e links para baixar
   PNG / SVG / EPS / fonte `.tikz` / `.tex` standalone.
4. **Pasta de entrada (`banco/`)** para depositar figuras ainda não
   categorizadas — vindas do "banco de dados" pessoal ou extraídas de
   projetos existentes — para triagem futura sem travar o fluxo de
   trabalho atual.
5. Continua **dentro de `GitRTx/TikZ`**, sem tocar nos outros projetos.

## Fora de escopo da v1 (próximas iterações)

- Migração em massa dos 43 `.tikz` já existentes nos projetos (decisão
  editorial: qual variante manter, como renomear, como não duplicar).
  A v1 traz só 4 figuras de exemplo, uma por categoria, para validar o
  pipeline ponta a ponta.
- Busca textual / tags clicáveis no site (Quarto `listing` com filtro).
- Deduplicação automática de figuras semelhantes.
- Publicação automática via GitHub Pages (o workflow existe como modelo
  em `TemplateNotas/.github/workflows/publish.yml` e pode ser copiado
  quando o conteúdo estiver maduro).

## Estrutura de diretórios

```
TikZ/
├── SCOPE.md                     este documento
├── README.md                    guia de uso/contribuição
├── _quarto.yml                  site Quarto (mesmo padrão do TemplateNotas)
├── TemaModelo.scss              tema visual (copiado/adaptado do TemplateNotas)
├── index.qmd                    portal: introdução + cards de categorias
├── categorias/                  páginas .qmd geradas (uma por categoria) — NÃO editar à mão
│   └── <categoria>.qmd
├── figuras/                     coleção curada, organizada por categoria
│   └── <categoria>/
│       ├── NomeFigura.tikz       corpo tikzpicture (sem preâmbulo)
│       └── NomeFigura.meta.yml   título, descrição, tags, libs extras (opcional)
├── banco/                       entrada: depositar .tikz não categorizados
│   └── README.md
├── _build/                      artefatos gerados (git-ignored) — pdf/png/svg/eps + .tex standalone
│   └── <categoria>/<NomeFigura>/
├── scripts/
│   ├── build_figuras.py         .tikz -> standalone .tex -> pdf -> png/svg/eps
│   ├── generate_gallery.py      varre figuras/ + _build/ -> escreve categorias/*.qmd e index.qmd
│   └── rebuild.sh                atalho: roda os dois scripts + quarto render
└── .gitignore                   ignora _build/ e _site/
```

## Esquema de metadados (`NomeFigura.meta.yml`)

```yaml
title: "Bloco PID em malha fechada"        # opcional; padrão = nome do arquivo
description: "Diagrama de blocos do controlador PID com realimentação unitária."
tags: [pid, diagrama-de-blocos, malha-fechada]
libraries: [arrows.meta, positioning, calc, fit]   # libs TikZ extras além do conjunto padrão
dpi: 300                                            # opcional; densidade do PNG (padrão 300)
fonte: "ControleClassico/Notas/imgs/tikz/PIDBloco.tikz"  # proveniência, opcional
```

Sem `.meta.yml`, a figura ainda entra na galeria: título derivado do nome
do arquivo, descrição vazia, tag = nome da categoria.

## Pipeline de conversão

Bibliotecas TikZ carregadas por padrão no preâmbulo standalone (levantadas
a partir do uso real nos 43 arquivos existentes):
`arrows.meta, positioning, calc, decorations.pathmorphing, patterns, fit,
shapes.geometric`. Libs adicionais por figura entram via `libraries:` no
`.meta.yml`.

Para cada `figuras/<categoria>/<nome>.tikz`:

1. Gera `_build/<categoria>/<nome>/<nome>.tex` (classe `standalone`,
   preâmbulo comum + libs extras do `.meta.yml`, `\input` do `.tikz`).
2. `pdflatex` → `<nome>.pdf` (recorte automático da classe `standalone`).
3. `pdftoppm -r <dpi> -png` → `<nome>.png` (raster, densidade configurável,
   padrão 300 dpi — "boa densidade" para uso em slides/documentos).
4. `pdf2svg` → `<nome>.svg` (vetor, para a web).
5. `pdftops -eps` → `<nome>.eps` (vetor — fidelidade exata, não há perda
   de "densidade" porque não é raster; é o formato correto para inclusão
   em LaTeX clássico/publicações).
6. Copia o `.tikz` fonte e o `.tex` standalone para a mesma pasta de
   build, para virarem link de download direto na galeria.

Build incremental: um arquivo só é recompilado se o `.tikz` ou o
`.meta.yml` forem mais novos que o `.pdf` já gerado (ou com `--force`).

## Página de categoria (gerada)

Grid responsivo de cards. Cada card:

- **Preview**: `<nome>.png` (thumbnail, `loading="lazy"`).
- **Título** + descrição curta + tags (badges).
- **Downloads**: `PNG` · `SVG` · `EPS` · `.tikz` · `.tex` (standalone).
- **Ver código**: expande o conteúdo do `.tikz` inline (`<details>`).

O `index.qmd` lista as categorias com contagem de figuras e um link para
cada página de categoria.

## Fluxo de trabalho (contribuir com uma figura nova)

1. Depositar o `.tikz` em `banco/` (se ainda não sabe a categoria) ou
   direto em `figuras/<categoria>/` (categoria existente ou nova pasta).
2. Opcional: criar `NomeFigura.meta.yml` ao lado.
3. Rodar `scripts/rebuild.sh` — compila o pendente, regenera as páginas e
   roda `quarto render`.
4. Conferir em `_site/index.html` (ou `quarto preview`).

## Categorias iniciais (v1)

Baseadas nos temas já identificados nos projetos de `GitRTx`:
`controle-classico`, `controle-estados`, `controle-digital`,
`circuitos-ca`, `metodos-numericos`, `identificacao`, `koopman`,
`mpc-dmc`. A v1 semeia 4 delas com uma figura de exemplo cada; as demais
podem ser criadas sob demanda (basta criar a pasta em `figuras/`).
