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
- **LaTeX** (`pdflatex`) — ex. TeX Live ou MacTeX.
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

## Sobre publicar no GitHub Pages

`_build/` e `_site/` estão no `.gitignore` — cada máquina recompila
localmente. Para publicar via CI (como em `TemplateNotas/.github/workflows/publish.yml`),
o workflow precisa instalar TeX Live + poppler + pdf2svg e rodar
`scripts/build_figuras.py` e `scripts/generate_gallery.py` antes de
`quarto render`. Alternativa mais simples: parar de ignorar `_build/` e
versionar os artefatos já compilados. Nenhuma das duas está feita ainda
— fica para quando o conteúdo estiver maduro (ver `SCOPE.md`).
