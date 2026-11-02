/* HCsoftware — filtros do catálogo e sincronização da versão mais recente. */

(function () {
  "use strict";

  /* ---------- filtros e pesquisa ---------- */

  const chips = Array.prototype.slice.call(document.querySelectorAll("[data-filtro]"));
  const cartoes = Array.prototype.slice.call(document.querySelectorAll(".cartao"));
  const pesquisa = document.getElementById("pesquisa");
  const vazio = document.getElementById("vazio");
  const resultado = document.getElementById("resultado");
  const limpar = document.getElementById("limpar-filtros");

  let categoria = "todos";
  let termo = "";

  function normalizar(texto) {
    return texto
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
  }

  function aplicarFiltros() {
    const alvo = normalizar(termo.trim());
    let visiveis = 0;

    cartoes.forEach(function (cartao) {
      const daCategoria = categoria === "todos" || cartao.dataset.categoria === categoria;
      const conteudo = normalizar(cartao.dataset.nome + " " + cartao.textContent);
      const corresponde = !alvo || conteudo.indexOf(alvo) !== -1;
      const mostrar = daCategoria && corresponde;

      cartao.hidden = !mostrar;
      if (mostrar) visiveis += 1;
    });

    vazio.hidden = visiveis > 0;
    resultado.textContent =
      visiveis === 1 ? "1 programa visível" : visiveis + " programas visíveis";
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (outro) {
        outro.classList.toggle("ativo", outro === chip);
        outro.setAttribute("aria-pressed", outro === chip ? "true" : "false");
      });
      categoria = chip.dataset.filtro;
      aplicarFiltros();
    });
  });

  if (pesquisa) {
    pesquisa.addEventListener("input", function () {
      termo = pesquisa.value;
      aplicarFiltros();
    });
  }

  if (limpar) {
    limpar.addEventListener("click", function () {
      termo = "";
      if (pesquisa) pesquisa.value = "";
      categoria = "todos";
      chips.forEach(function (chip) {
        const ativo = chip.dataset.filtro === "todos";
        chip.classList.toggle("ativo", ativo);
        chip.setAttribute("aria-pressed", ativo ? "true" : "false");
      });
      aplicarFiltros();
    });
  }

  /* ---------- versão mais recente do HC-Gestão Stocks ---------- */

  const URL_VERSAO =
    "https://raw.githubusercontent.com/condessa/hc-gestao-stocks-releases/main/versao.json";

  function tamanho(bytes) {
    if (!bytes || typeof bytes !== "number") return "";
    const mb = bytes / (1024 * 1024);
    if (mb >= 1) return (mb >= 10 ? Math.round(mb) : mb.toFixed(1).replace(".", ",")) + " MB";
    return Math.max(1, Math.round(bytes / 1024)) + " KB";
  }

  function aplicarVersao(dados) {
    if (!dados || !dados.versao || !dados.ficheiros) return;

    document.querySelectorAll("[data-versao-stocks]").forEach(function (el) {
      el.textContent = "v" + dados.versao;
    });

    document.querySelectorAll("[data-legenda-stocks]").forEach(function (el) {
      el.textContent = "HC-Gestão Stocks · v" + dados.versao;
    });

    [
      ["windows", "Windows", ".exe"],
      ["debian", "Linux", ".deb"]
    ].forEach(function (par) {
      const chave = par[0];
      const ficheiro = dados.ficheiros[chave];
      if (!ficheiro || !ficheiro.url) return;

      document.querySelectorAll('[data-download="' + chave + '"]').forEach(function (link) {
        link.href = ficheiro.url;
        const etiqueta = link.querySelector("small");
        if (etiqueta) {
          const tamanhoTexto = tamanho(ficheiro.tamanho);
          etiqueta.textContent = par[2] + (tamanhoTexto ? " · " + tamanhoTexto : "");
        }
      });
    });
  }

  if ("fetch" in window) {
    fetch(URL_VERSAO, { cache: "no-store" })
      .then(function (resposta) {
        return resposta.ok ? resposta.json() : null;
      })
      .then(aplicarVersao)
      .catch(function () {
        /* Sem rede: ficam os valores escritos no HTML. */
      });
  }

  /* ---------- ano no rodapé ---------- */

  const ano = document.getElementById("ano");
  if (ano) ano.textContent = String(new Date().getFullYear());

  /* Estado inicial dos chips (acessibilidade). */
  chips.forEach(function (chip) {
    chip.setAttribute("aria-pressed", chip.classList.contains("ativo") ? "true" : "false");
  });
})();
