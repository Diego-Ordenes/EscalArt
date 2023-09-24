var clicked = false;
window.addEventListener("scroll", function() {
        var nav = document.querySelector(".nav");
        var config = document.querySelector("#Configuracion");
        nav.classList.toggle("active", window.scrollY > 0);
        config.classList.toggle("active", window.scrollY > 0);
    })
    //----------------------Perfil--------------------------//
function mostrarConfig_dt() {
    if (clicked) {
        document.getElementById('Configuracion').style.right = '0';
        clicked = false;
    } else {
        document.getElementById('Configuracion').style.right = '-250px';
        clicked = true;
    }

}

function ocultarConfig() {
    document.getElementById('Configuracion').style.display = 'none';
}