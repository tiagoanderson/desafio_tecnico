// =============================================================================
// static/js/script.js
// -----------------------------------------------------------------------------
// CAMADA: View (Frontend)
//
// JavaScript simples do lado do cliente (roda no navegador do usuário).
// Única responsabilidade: pedir confirmação antes de excluir um registro,
// evitando exclusões acidentais de setor ou patrimônio.
// =============================================================================

document.addEventListener("DOMContentLoaded", function () {
    // Seleciona todos os formulários marcados com o atributo
    // data-confirmar="mensagem" (ver botões de excluir nos templates).
    const formulariosDeExclusao = document.querySelectorAll("form[data-confirmar]");

    formulariosDeExclusao.forEach(function (formulario) {
        formulario.addEventListener("submit", function (evento) {
            const mensagem = formulario.getAttribute("data-confirmar");
            const confirmado = window.confirm(mensagem);

            if (!confirmado) {
                evento.preventDefault(); // cancela o envio do formulário
            }
        });
    });

    // Fecha automaticamente os alertas (mensagens flash) após 4 segundos.
    const alertas = document.querySelectorAll(".alert");
    alertas.forEach(function (alerta) {
        setTimeout(function () {
            alerta.classList.remove("show");
            alerta.classList.add("fade");
        }, 4000);
    });
});
