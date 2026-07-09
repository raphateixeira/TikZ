# Banco (entrada de figuras não categorizadas)

Deposite aqui `.tikz` que você ainda não sabe em qual categoria colocar —
vindos do seu banco de dados pessoal de figuras ou extraídos de um
projeto existente. Nada nesta pasta entra no site automaticamente: é só
uma fila de espera.

## Triagem

1. Abra o arquivo e decida a categoria (uma pasta em `../figuras/`; crie
   uma nova se nenhuma existente servir).
2. Mova o `.tikz` para `../figuras/<categoria>/`.
3. Opcional: crie `NomeFigura.meta.yml` ao lado (veja o esquema em
   `../SCOPE.md`).
4. Rode `../scripts/rebuild.sh` para compilar e publicar.

Um `.tikz` aqui é só o corpo `\begin{tikzpicture}...\end{tikzpicture}`
(ou um trecho que possa ser envolvido por esse ambiente), sem preâmbulo —
mesmo formato usado nos outros projetos de `GitRTx`.
