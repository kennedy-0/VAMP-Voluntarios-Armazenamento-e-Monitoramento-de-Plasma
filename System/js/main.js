const API = "http://localhost:5001/api";
const ORDEM_TIPOS = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"];
const MESES = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
let doacoes = [], estoque = [], graficos = {};
const filtros = { ano: new Set(), cidade: new Set(), tipo: new Set() };

// Cria os botões de filtro de um grupo (ano, cidade ou tipo)
function montarFiltro(chave, valores) {
    const grupo = document.getElementById("f-" + chave);
    valores.forEach(v => {
        const label = document.createElement("label");
        label.innerHTML = `<input type="checkbox" value="${v}"> ${v}`;
        label.querySelector("input").addEventListener("change", e => {
            e.target.checked ? filtros[chave].add(v) : filtros[chave].delete(v);
            atualizar();
        });
        grupo.appendChild(label);
    });
}

// Filtro vazio = não filtra nada
const passa = (conj, valor) => conj.size === 0 || conj.has(valor);

// Conta (ou soma) itens agrupando por uma chave
function agrupar(lista, chave, valor = () => 1) {
    const r = {};
    lista.forEach(i => { const k = chave(i); r[k] = (r[k] || 0) + valor(i); });
    return r;
}

function desenhar(id, tipo, labels, series) {
    if (graficos[id]) graficos[id].destroy();
    graficos[id] = new Chart(document.getElementById(id), {
        type: tipo,
        data: { labels, datasets: series },
        options: { responsive: true, maintainAspectRatio: false,
                   scales: { y: { beginAtZero: true } },
                   plugins: { legend: { display: series.length > 1 } } }
    });
}

function atualizar() {
    const f = doacoes.filter(d =>
        passa(filtros.ano, d.data.slice(0, 4)) &&
        passa(filtros.cidade, d.cidade) &&
        passa(filtros.tipo, d.tipo));

    document.getElementById("k-doacoes").textContent = f.length;
    document.getElementById("k-litros").textContent =
        (f.reduce((s, d) => s + d.quantidade_ml, 0) / 1000).toFixed(1);

    // Por mês (ano-mês em ordem cronológica)
    const mes = agrupar(f, d => d.data.slice(0, 7));
    const chavesMes = Object.keys(mes).sort();
    desenhar("g-mes", "bar",
        chavesMes.map(k => MESES[+k.slice(5) - 1] + "/" + k.slice(2, 4)),
        [{ label: "Doações", data: chavesMes.map(k => mes[k]), backgroundColor: "#d90e0e" }]);

    // Por cidade (maior para menor)
    const cid = agrupar(f, d => d.cidade);
    const chavesCid = Object.keys(cid).sort((a, b) => cid[b] - cid[a]);
    desenhar("g-cidade", "bar", chavesCid,
        [{ label: "Doações", data: chavesCid.map(k => cid[k]), backgroundColor: "#8b0000" }]);

    // Por tipo: doações no período vs estoque atual (filtra cidade e tipo)
    const est = agrupar(estoque.filter(e => passa(filtros.cidade, e.cidade) && passa(filtros.tipo, e.tipo)),
                        e => e.tipo, e => e.quantidade);
    const doa = agrupar(f, d => d.tipo);
    const tipos = ORDEM_TIPOS.filter(t => passa(filtros.tipo, t));
    desenhar("g-tipo", "bar", tipos, [
        { label: "Doações", data: tipos.map(t => doa[t] || 0), backgroundColor: "#d90e0e" },
        { label: "Bolsas em estoque", data: tipos.map(t => est[t] || 0), backgroundColor: "#555" }]);
}

document.getElementById("limpar").addEventListener("click", () => {
    Object.values(filtros).forEach(s => s.clear());
    document.querySelectorAll(".filtro input").forEach(i => i.checked = false);
    atualizar();
});

// Busca os dados na API e monta a tela
Promise.all([fetch(API + "/doacoes"), fetch(API + "/estoque")])
    .then(rs => Promise.all(rs.map(r => r.json())))
    .then(([d, e]) => {
        doacoes = d; estoque = e;
        montarFiltro("ano", [...new Set(d.map(x => x.data.slice(0, 4)))].sort());
        montarFiltro("cidade", [...new Set(d.map(x => x.cidade))].sort());
        montarFiltro("tipo", ORDEM_TIPOS);
        atualizar();
    })
    .catch(() => document.getElementById("aviso").hidden = false);
