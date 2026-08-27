# Como usar isso no seu GitHub

Estes arquivos montam a versão "terminal" do seu perfil: heatmap de
commits animado e, logo abaixo, um card estilo terminal com sua
identidade, bio e contato — tudo SVG, sem serviço de terceiros, sem
token.

## 1. Crie o repositório especial do seu perfil

Se ainda não existe, crie um repositório **com exatamente o mesmo nome
do seu usuário**: `EricTeixeir/EricTeixeir` (público). O `README.md`
dele é o que aparece no topo do seu perfil.

## 2. Suba estes arquivos

Copie para a raiz do repo:

```
README.md
contrib-heatmap.svg
info-card.svg
scripts/
.github/workflows/update-profile-art.yml
```

```bash
git init
git remote add origin https://github.com/EricTeixeir/EricTeixeir.git
git add .
git commit -m "feat: perfil animado com heatmap + card de infos"
git branch -M main
git push -u origin main
```

## 3. Ative o workflow

Vá em **Actions** no repo → você vai ver "Update profile art" →
clique em **Run workflow** uma vez manualmente pra confirmar que
funciona. Depois disso ele roda sozinho todo dia (~06:17 UTC) e
mantém `contrib-heatmap.svg` sempre atualizado com seus commits reais.

## 4. Se quiser mudar o texto do card

Edite `NAME`, `TITLE`, `INFO` ou `CONTACT` no topo de
`scripts/make_info_card.py`, depois rode:

```bash
python3 scripts/make_info_card.py
git add info-card.svg && git commit -m "chore: atualizar card de infos" && git push
```

## O que cada script faz

| Script | O que faz | Roda quando |
|---|---|---|
| `fetch_contributions.py` | baixa seu calendário de contribuições público (HTML, sem token) | diariamente via Actions |
| `render_heatmap_svg.py` | desenha o grid 53×7 animado a partir desses dados | diariamente via Actions |
| `make_info_card.py` | gera o card estilo neofetch (edite os textos direto no script) | quando quiser mudar o texto |

## Detalhes técnicos que valem saber

- O GitHub remove `<script>` de READMEs e boa parte do CSS inline —
  por isso toda a animação vive dentro de cada SVG (SMIL / CSS
  keyframes), e o README só posiciona os arquivos.
- `<h1>`/`<h2>` desenham uma linha embaixo do texto; por isso os
  cabeçalhos "prompt de terminal" usam `<h3>`.
- Espaçamento vertical: `style="margin-top"` é ignorado pelo GitHub,
  use `<br>`.
- Todo SVG embutido via `<img>` precisa ter `width`/`height`
  explícitos além do `viewBox`, ou alguns visualizadores de markdown
  falham em renderizar ("Invalid image source"). Os dois arquivos já
  saem assim dos scripts.
