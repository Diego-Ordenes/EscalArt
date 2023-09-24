//-----------------------------------------------------------Publicaciones/Imagenes----------------------------------------//

//Variables
// const btnCierra = document.querySelector('#btn-cierra');

// const btnAdelanta = document.querySelector('#btn-adelanta');
// const btnRetrocede = document.querySelector('#btn-retrocede');
// const imagenes = document.querySelectorAll('#galeria img');
// const lightbox = document.querySelector('#contenedor-principal')

// const imagenActiva = document.querySelector('#img-activa');
// let indiceImagen = 0;

// //Abrir el lightbox

// const abreLightbox = (event) => {
//     imagenActiva.src = event.target.src;
//     lightbox.style.display = 'flex';
//     indiceImagen = Array.from(imagenes).indexOf(event.target);
// }
// imagenes.forEach((imagen) => {
//     imagen.addEventListener('click', abreLightbox);
// });

// //Cerrar el lightbox
btnCierra.addEventListener('click', () => {
    lightbox.style.display = 'none';
})

function OcultarPubli() {
    document.getElementById('contenedor-principal').style.display = 'none';
}

function AbrirPubli() {
    document.getElementById('contenedor-principal').style.display = 'flex';
}

//Adelantar imagen
const adelantaImagen = () => {
    if (indiceImagen === imagenes.length - 1) {
        indiceImagen = -1;
    }
    imagenActiva.src = imagenes[indiceImagen + 1].src;
    indiceImagen++;
};

btnAdelanta.addEventListener('click', adelantaImagen);

//Retrocede la imagen

const retrocedeImagen = () => {
    if (indiceImagen === 0) {
        indiceImagen = imagenes.length;
    }
    imagenActiva.src = imagenes[indiceImagen - 1].src;
    indiceImagen--;
};

btnRetrocede.addEventListener('click', retrocedeImagen);




//--------------------------------Calificacion------------------------------------------//
function mostrar() {
    document.getElementById('testimonials').style.display = 'flex';
}

function ocultar() {
    document.getElementById('testimonials').style.display = 'none';
}
//----------------------Perfil--------------------------//
function mostrarConfig() {
    document.getElementById('Configuracion').style.display = 'flex';
}

function ocultarConfig() {
    document.getElementById('Configuracion').style.display = 'none';
}
//----------------------Publicacion-----------------------//
function MostrarPublicacion() {
    document.getElementById('section-publicacion').style.display = 'flex';
}

function OcultarPublicacion() {
    document.getElementById('section-publicacion').style.display = 'none';
}
//-----------------------Configurar-Bio------------------------//
function MostrarConfi_bio() {
    document.getElementById('config-fondo').style.display = 'flex';
}

function OcultarConfi_bio() {
    document.getElementById('config-fondo').style.display = 'none';
}

// Opciones perfil artista
var toggle = false;

function MostrarOpciones() {
    if (toggle) {
        document.getElementById('settings-artista').style.display = 'none';
        toggle = false;

    } else {
        document.getElementById('settings-artista').style.display = 'flex';
        toggle = true;

    }
}