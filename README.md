# Site HCsoftware

**No ar:** <https://condessa.github.io/hcsoftware/> · repositório: <https://github.com/condessa/hcsoftware>

Página única que reúne todos os programas gratuitos do HCsoftware, com descrição,
plataformas e botões de download direto para os instaladores publicados no GitHub.

- Sem servidor, sem base de dados, sem dependências: só HTML, CSS e um pouco de JavaScript.
- Identidade visual igual à da aplicação: fundo `#2b2b2b`, azul `#4a90d9` e o logótipo
  "HC" em âmbar (`#FFC46B → #C2761A`).
- Funciona em qualquer alojamento estático (GitHub Pages, Netlify, Cloudflare Pages…).

## Ficheiros

| Ficheiro | Para que serve |
|---|---|
| `index.html` | A página. É aqui que se edita o texto e se acrescentam programas. |
| `estilo.css` | Todas as cores, espaçamentos e o comportamento em telemóvel. |
| `app.js` | Filtros por categoria, pesquisa e atualização automática da versão do HC-Gestão Stocks. |
| `assets/` | Logótipo, captura do painel, favicon e imagem de partilha (`og-image.png`). |
| `tools/gerar_imagens.py` | Volta a gerar o favicon e a imagem de partilha a partir das imagens do projeto. |
| `robots.txt`, `sitemap.xml` | Ajudam os motores de busca a encontrar a página. |

## Ver localmente

```bash
cd hcsoftware-site
python3 -m http.server 8000
```

Depois abrir <http://localhost:8000>. (Abrir o `index.html` diretamente também funciona,
mas a atualização automática da versão pode ser bloqueada pelo browser.)

## Publicar no GitHub Pages (gratuito)

Já está publicado. Se um dia precisares de refazer a configuração:

1. Criar um repositório **público** chamado `hcsoftware` em <https://github.com/condessa>.
2. Enviar o conteúdo desta pasta para a raiz desse repositório (`index.html` na raiz).
3. No repositório: **Settings → Pages → Source: Deploy from a branch → `main` → `/ (root)` → Save**.
4. Ao fim de um ou dois minutos a página fica em <https://condessa.github.io/hcsoftware/>.

Se o repositório tiver outro nome (ou usares um domínio próprio), atualiza estes três sítios
em `index.html`: `<link rel="canonical">`, `og:url` e `og:image`; e o endereço em `sitemap.xml`.
No domínio próprio, basta adicionar um ficheiro `CNAME` com o domínio.

## Atualizar o catálogo

### Novo programa

Copiar um bloco `<article class="cartao" …>` dentro de `#lista-programas` e mudar:

- `data-categoria` — `gestao`, `iot`, `rede` ou `utilidades` (tem de existir um chip com o mesmo valor);
- `data-nome` — palavras-chave para a pesquisa;
- o monograma (`GS`, `AM`, …) e a cor (`m-ambar`, `m-azul`, `m-verde`, `m-roxo`);
- nome, versão, descrição, etiquetas e os links dos botões.

### Versão do HC-Gestão Stocks

Os botões e a versão atualizam-se sozinhos: o `app.js` lê o `versao.json` publicado em
`condessa/hc-gestao-stocks-releases` e substitui os links. O HTML tem sempre uma versão
de recurso, para o caso de não haver rede.

### Capturas

Para trocar a imagem de partilha e o favicon:

```bash
cd hcsoftware-site
python3 tools/gerar_imagens.py
```

O script lê o logótipo e as capturas de `../StockWin11/imagens` e `../StockWin11/tools/capturas`.

## Notas

- O telefone de apoio que aparece na aplicação **não** está no site (ficou só o e-mail),
  para não expor o número publicamente. Para o acrescentar, é na secção `#sobre`.
- O HC-Gestão Stocks é gratuito mas o código-fonte é privado; por isso não tem etiqueta
  "código aberto". O DeviceScan e o Tasmota Smart Hub têm licença MIT.
