// Mostrar input para responder a un comentario
function responderComentario(parent_id) {

    const row = document.getElementById(parent_id);
    if (row.classList.contains('d-none')) {
        row.classList.remove('d-none');
    } else {
        row.classList.add('d-none');
    }

}

function mostrarRespuestas(children) {

    const row = document.getElementById(children);
    if (row.classList.contains('d-none')) {
        row.classList.remove('d-none');
    } else {
        row.classList.add('d-none');
    }
}