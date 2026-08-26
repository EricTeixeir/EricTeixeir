# Como usar isso no seu GitHub

Estes arquivos montam a versão "terminal" do seu perfil: heatmap de
commits animado no topo, e retrato ASCII + card de infos lado a lado
embaixo — tudo SVG, sem serviço de terceiros, sem token.

## 1. Crie o repositório especial do seu perfil

Se ainda não existe, crie um repositório **com exatamente o mesmo nome
do seu usuário**: `EricTeixeir/EricTeixeir` (público). O `README.md`
dele é o que aparece no topo do seu perfil.

## 2. Suba estes arquivos

Copie para a raiz do repo:

```
README.md
contrib-heatmap.svg
eric-ascii.svg
info-card.svg
scripts/
.github/workflows/update-profile-art.yml
```

```bash
git init
git remote add origin https://github.com/EricTeixeir/EricTeixeir.git
git add .
git commit -m "feat: perfil animado com heatmap + retrato ASCII"
git branch -M main
git push -u origin main
```

## 3. Ative o workflow

Vá em **Actions** no repo → você vai ver "Update profile art" →
clique em **Run workflow** uma vez manualmente pra confirmar que
funciona. Depois disso ele roda sozinho todo dia (~06:17 UTC) e
mantém `contrib-heatmap.svg` sempre atualizado com seus commits reais.

## 4. Se quiser trocar a foto do retrato depois

```bash
pip install -r scripts/requirements.txt
python scripts/prep_photo.py sua-nova-foto.jpg     # remove fundo + realça contraste
python scripts/make_ascii_svg.py source-prepped.png
mv avi-ascii.svg eric-ascii.svg
git add eric-ascii.svg && git commit -m "chore: atualizar retrato" && git push
```

## O que cada script faz

| Script | O que faz | Roda quando |
|---|---|---|
| `fetch_contributions.py` | baixa seu calendário de contribuições público (HTML, sem token) | diariamente via Actions |
| `render_heatmap_svg.py` | desenha o grid 53×7 animado a partir desses dados | diariamente via Actions |
| `prep_photo.py` | remove fundo da foto + realça contraste (preto e branco) | só quando você trocar a foto |
| `make_ascii_svg.py` | converte a foto tratada em ASCII art que "digita" sozinho | só quando você trocar a foto |
| `make_info_card.py` | gera o card estilo neofetch (edite os textos direto no script) | quando quiser mudar o texto |

## Detalhes técnicos que valem saber

- O GitHub remove `<script>` de READMEs e boa parte do CSS inline —
  por isso toda a animação vive dentro de cada SVG (SMIL / CSS
  keyframes), e o README só posiciona os arquivos.
- `<h1>`/`<h2>` desenham uma linha embaixo do texto; por isso os
  cabeçalhos "prompt de terminal" usam `<h3>`.
- Espaçamento vertical: `style="margin-top"` é ignorado pelo GitHub,
  use `<br>`.
- As larguras das imagens (`860`, `370`, `490`) são pensadas pra
  alinhar: `370 + 490 = 860`. Se mudar uma, ajuste a outra.
