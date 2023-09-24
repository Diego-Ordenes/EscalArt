// Opciones perfil artista
var toggle = false;

function MostrarOpciones() {
    if (toggle) {
        document.getElementById('settings-post').style.display = 'none';
        toggle = false;

    } else {
        document.getElementById('settings-post').style.display = 'flex';
        toggle = true;

    }
}

