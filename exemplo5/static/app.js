const apiBase = `${window.location.origin}/produtos`;

const productsTableBody = document.getElementById("productsTableBody");
const productsCardList = document.getElementById("productsCardList");
const productCount = document.getElementById("productCount");
const openCreateButton = document.getElementById("openCreateButton");

const modalOverlay = document.getElementById("modalOverlay");
const modalKicker = document.getElementById("modalKicker");
const modalTitle = document.getElementById("modalTitle");
const closeModalButton = document.getElementById("closeModalButton");
const productForm = document.getElementById("productForm");
const viewContent = document.getElementById("viewContent");
const deleteContent = document.getElementById("deleteContent");
const saveProductButton = document.getElementById("saveProductButton");
const confirmDeleteButton = document.getElementById("confirmDeleteButton");

const productIdField = document.getElementById("productId");
const productNomeField = document.getElementById("productNome");
const productPrecoField = document.getElementById("productPreco");
const productQuantidadeField = document.getElementById("productQuantidade");

let currentModalMode = null;
let selectedProduct = null;

function formatCurrency(value) {
    return Number(value).toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
    });
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function resetModalSections() {
    viewContent.classList.add("hidden");
    productForm.classList.add("hidden");
    deleteContent.classList.add("hidden");
}

function openModal(mode, product = null) {
    currentModalMode = mode;
    selectedProduct = product;
    resetModalSections();
    modalOverlay.classList.remove("hidden");
    document.body.classList.add("modal-open");

    if (mode === "create") {
        modalKicker.textContent = "Novo cadastro";
        modalTitle.textContent = "Adicionar produto";
        productForm.reset();
        productIdField.value = "";
        productNomeField.required = true;
        productPrecoField.required = true;
        productQuantidadeField.required = true;
        saveProductButton.setAttribute("aria-label", "Cadastrar produto");
        saveProductButton.setAttribute("title", "Cadastrar produto");
        saveProductButton.innerHTML = '<i class="bi bi-plus-lg" aria-hidden="true"></i>';
        productForm.classList.remove("hidden");
    }

    if (mode === "edit" && product) {
        modalKicker.textContent = "Edicao";
        modalTitle.textContent = `Editar produto #${product.id}`;
        productIdField.value = product.id;
        productNomeField.value = product.nome;
        productPrecoField.value = product.preco;
        productQuantidadeField.value = product.quantidade;
        productNomeField.required = true;
        productPrecoField.required = true;
        productQuantidadeField.required = true;
        saveProductButton.setAttribute("aria-label", "Salvar alteracoes");
        saveProductButton.setAttribute("title", "Salvar alteracoes");
        saveProductButton.innerHTML = '<i class="bi bi-floppy" aria-hidden="true"></i>';
        productForm.classList.remove("hidden");
    }

    if (mode === "view" && product) {
        modalKicker.textContent = "Visualizacao";
        modalTitle.textContent = `Produto #${product.id}`;
        document.getElementById("viewId").textContent = product.id;
        document.getElementById("viewNome").textContent = product.nome;
        document.getElementById("viewPreco").textContent = formatCurrency(product.preco);
        document.getElementById("viewQuantidade").textContent = product.quantidade;
        viewContent.classList.remove("hidden");
    }

    if (mode === "delete" && product) {
        modalKicker.textContent = "Remocao";
        modalTitle.textContent = `Excluir produto #${product.id}`;
        document.getElementById("deleteId").textContent = product.id;
        document.getElementById("deleteNome").textContent = product.nome;
        deleteContent.classList.remove("hidden");
    }
}

function closeModal() {
    modalOverlay.classList.add("hidden");
    document.body.classList.remove("modal-open");
    currentModalMode = null;
    selectedProduct = null;
    productForm.reset();
}

function renderProducts(products) {
    productCount.textContent = `${products.length} ${products.length === 1 ? "item" : "itens"}`;

    if (!products.length) {
        productsTableBody.innerHTML = `
            <tr>
                <td colspan="5" class="empty-row">Nenhum produto cadastrado no momento.</td>
            </tr>
        `;
        productsCardList.innerHTML = `
            <article class="product-card product-card-empty">
                <p>Nenhum produto cadastrado no momento.</p>
            </article>
        `;
        return;
    }

    productsTableBody.innerHTML = products.map((product) => `
        <tr>
            <td>${product.id}</td>
            <td>${escapeHtml(product.nome)}</td>
            <td>${formatCurrency(product.preco)}</td>
            <td>${product.quantidade}</td>
            <td>
                <div class="action-group">
                    <button class="table-action action-view icon-only-button" type="button" data-action="view" data-id="${product.id}" aria-label="Visualizar produto ${escapeHtml(product.nome)}" title="Visualizar">
                        <i class="bi bi-eye" aria-hidden="true"></i>
                    </button>
                    <button class="table-action action-edit icon-only-button" type="button" data-action="edit" data-id="${product.id}" aria-label="Editar produto ${escapeHtml(product.nome)}" title="Editar">
                        <i class="bi bi-pencil-square" aria-hidden="true"></i>
                    </button>
                    <button class="table-action action-delete icon-only-button" type="button" data-action="delete" data-id="${product.id}" aria-label="Remover produto ${escapeHtml(product.nome)}" title="Remover">
                        <i class="bi bi-trash3" aria-hidden="true"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join("");

    productsCardList.innerHTML = products.map((product) => `
        <article class="product-card">
            <div class="product-card-top">
                <span class="product-card-id">#${product.id}</span>
                <strong class="product-card-name">${escapeHtml(product.nome)}</strong>
            </div>
            <div class="product-card-body">
                <div class="product-card-field">
                    <span>Preco</span>
                    <strong>${formatCurrency(product.preco)}</strong>
                </div>
                <div class="product-card-field">
                    <span>Quantidade</span>
                    <strong>${product.quantidade}</strong>
                </div>
            </div>
            <div class="action-group">
                <button class="table-action action-view icon-only-button" type="button" data-action="view" data-id="${product.id}" aria-label="Visualizar produto ${escapeHtml(product.nome)}" title="Visualizar">
                    <i class="bi bi-eye" aria-hidden="true"></i>
                </button>
                <button class="table-action action-edit icon-only-button" type="button" data-action="edit" data-id="${product.id}" aria-label="Editar produto ${escapeHtml(product.nome)}" title="Editar">
                    <i class="bi bi-pencil-square" aria-hidden="true"></i>
                </button>
                <button class="table-action action-delete icon-only-button" type="button" data-action="delete" data-id="${product.id}" aria-label="Remover produto ${escapeHtml(product.nome)}" title="Remover">
                    <i class="bi bi-trash3" aria-hidden="true"></i>
                </button>
            </div>
        </article>
    `).join("");
}

async function requestJson(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        },
        ...options,
    });

    const text = await response.text();
    const data = text ? JSON.parse(text) : {};

    if (!response.ok) {
        throw { status: response.status, data };
    }

    return data;
}

async function loadProducts() {
    try {
        const products = await requestJson(apiBase, { method: "GET" });
        renderProducts(products);
    } catch (error) {
        renderProducts([]);
        console.error("Erro ao listar produtos.", error);
    }
}

async function loadProductById(id) {
    return requestJson(`${apiBase}/${id}`, { method: "GET" });
}

productForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        nome: productNomeField.value.trim(),
        preco: Number(productPrecoField.value),
        quantidade: Number(productQuantidadeField.value),
    };

    try {
        if (currentModalMode === "create") {
            await requestJson(apiBase, {
                method: "POST",
                body: JSON.stringify(payload),
            });
        } else if (currentModalMode === "edit") {
            await requestJson(`${apiBase}/${productIdField.value}`, {
                method: "PUT",
                body: JSON.stringify(payload),
            });
        }

        closeModal();
        await loadProducts();
    } catch (error) {
        console.error("Erro ao salvar produto.", error);
    }
});

confirmDeleteButton.addEventListener("click", async () => {
    if (!selectedProduct) {
        return;
    }

    try {
        await requestJson(`${apiBase}/${selectedProduct.id}`, { method: "DELETE" });
        closeModal();
        await loadProducts();
    } catch (error) {
        console.error(`Erro ao excluir o produto ${selectedProduct.id}.`, error);
    }
});

async function handleProductAction(event) {
    const button = event.target.closest("[data-action]");
    if (!button) {
        return;
    }

    const { action, id } = button.dataset;

    try {
        const product = await loadProductById(id);

        if (action === "view") {
            openModal("view", product);
        }

        if (action === "edit") {
            openModal("edit", product);
        }

        if (action === "delete") {
            openModal("delete", product);
        }
    } catch (error) {
        console.error(`Erro ao carregar o produto ${id}.`, error);
    }
}

productsTableBody.addEventListener("click", handleProductAction);
productsCardList.addEventListener("click", handleProductAction);

openCreateButton.addEventListener("click", () => openModal("create"));
closeModalButton.addEventListener("click", closeModal);
modalOverlay.addEventListener("click", (event) => {
    if (event.target === modalOverlay) {
        closeModal();
    }
});

document.querySelectorAll("[data-close-modal]").forEach((button) => {
    button.addEventListener("click", closeModal);
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !modalOverlay.classList.contains("hidden")) {
        closeModal();
    }
});

loadProducts();
