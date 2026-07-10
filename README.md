# Coleção TikZ

Coleção organizada, por tema, das figuras TikZ usadas nas disciplinas e
projetos de pesquisa de `GitRTx`. Cada figura vira automaticamente PNG,
SVG, EPS e PDF, e entra em um site Quarto navegável por categoria — com
preview da imagem, código-fonte e links de download.

Veja **[`SCOPE.md`](SCOPE.md)** para o desenho completo (estrutura,
esquema de metadados, pipeline de conversão). Este arquivo é só o guia
rápido de uso.

## Adicionar uma figura

1. Coloque o `.tikz` (só o corpo `tikzpicture`, sem preâmbulo — mesmo
   formato já usado nos outros projetos) em `figuras/<categoria>/`. Se
   não souber a categoria ainda, deposite em `banco/` (veja
   [`banco/README.md`](banco/README.md)) e categorize depois.
2. Opcional: crie `figuras/<categoria>/NomeFigura.meta.yml` com título,
   descrição e tags (esquema em `SCOPE.md`). Sem isso, a figura ainda
   aparece na galeria com metadados mínimos.
3. Rode:
   ```bash
   ./scripts/rebuild.sh
   ```
   Isso compila as figuras pendentes (`build_figuras.py`), regenera as
   páginas de categoria e o `index.qmd` (`generate_gallery.py`), e
   renderiza o site (`quarto render`).
4. Confira em `_site/index.html`, ou rode `quarto preview` para navegar
   com recarregamento automático.

Para recompilar tudo do zero (ex.: depois de mudar o preâmbulo padrão em
`scripts/build_figuras.py`): `./scripts/rebuild.sh --force`.

Para compilar só uma categoria ou uma figura específica:
```bash
python3 scripts/build_figuras.py --only controle-classico
python3 scripts/build_figuras.py --only controle-classico/PIDBloco
```

## Pré-requisitos

- **Quarto**.
- **LaTeX** (`pdflatex`) — ex. TeX Live ou MacTeX, com os pacotes
  `circuitikz` e `pgfplots` (usados por algumas figuras de circuitos e
  gráficos de sinais — veja `packages:` no `.meta.yml`).
- **Poppler** (`pdftoppm`, `pdftops`) e **pdf2svg** — no macOS:
  `brew install poppler pdf2svg`.
- **Python 3** com **PyYAML** (`pip install pyyaml`).

## Estrutura

```
figuras/<categoria>/*.tikz + *.meta.yml   fontes curadas, por tema
banco/                                     entrada de figuras não categorizadas
_build/                                    saída gerada (pdf/png/svg/eps) — não versionado
categorias/*.qmd                           páginas geradas — não editar à mão
scripts/                                   pipeline de build e geração da galeria
```

## Publicação no GitHub Pages

`_build/` e `_site/` estão no `.gitignore` — cada máquina recompila
localmente, e o site publicado é gerado do zero a cada push para `main`
pelo workflow `.github/workflows/publish.yml`. O pipeline no CI:
instala TinyTeX (`standalone`, `pgf`, `pgfplots`, `xcolor`,
`circuitikz` e dependências) + Poppler + pdf2svg, roda
`scripts/build_figuras.py` e `scripts/generate_gallery.py`, e então
`quarto render`, publicando `_site/` via GitHub Pages (Actions).

Passo único necessário no GitHub: em **Settings → Pages → Build and
deployment → Source**, selecionar **GitHub Actions**. Depois disso, todo
push em `main` publica automaticamente em
`https://raphateixeira.github.io/TikZ/`.
