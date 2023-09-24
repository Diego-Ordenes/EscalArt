// var clicked = false;
// var clicked_3 = true;

// function mostrarComisiones() {
//     if (clicked) {
//         if (clicked_3) {
//             document.getElementById('es-comision').style.display = 'none';
//             clicked = false;
//         } else {
//             clicked_3 = true;
//         }

//     } else {
//         document.getElementById('gl-guardados').style.display = 'none';
//         document.getElementById('es-comision').style.display = 'flex';
//         clicked = true;
//         clicked_3 = false;
//     }

// }

// var clicked_guardados = false;
// var clicked_2 = true;

// function mostrarGuardados() {
//     if (clicked_guardados) {
//         if (clicked_2) {
//             document.getElementById('gl-guardados').style.display = 'none';
//             clicked_guardados = false;

//         } else {
//             clicked_2 = true
//         }
//     } else {
//         document.getElementById('es-comision').style.display = 'none';
//         document.getElementById('gl-guardados').style.display = 'flex';
//         clicked_guardados = true;
//         clicked_2 = false;
//     }

// }
function mostrarGuardados() {
    document.getElementById('es-comision').style.display = 'none';
    document.getElementById('gl-guardados').style.display = 'flex';
    document.getElementById('es-comisiontrabajo').style.display = 'none';

}

function mostrarComisiones() {
    document.getElementById('es-comision').style.display = 'flex';
    document.getElementById('gl-guardados').style.display = 'none';
    document.getElementById('es-comisiontrabajo').style.display = 'none';


}

function mostrarComisionesTrabajo() {
    // document.getElementById('tareas--').style.display = 'none';
    document.getElementById('gl-guardados').style.display = 'none';
    document.getElementById('es-comision').style.display = 'none';
    document.getElementById('es-comisiontrabajo').style.display = 'block';

}
// Alertas
function MostrarAlerta() {
    document.getElementById('AlertaOk').style.display = 'block';
}

function OcultarAlerta() {
    document.getElementById('AlertaOk').style.display = 'none';
}

function MostrarAlerta2() {
    document.getElementById('AlertaOk2').style.display = 'block';
}

function OcultarAlerta2() {
    document.getElementById('AlertaOk2').style.display = 'none';
}

// Fin alertas

// upload files
const realFileBtn2 = document.getElementById("real-file2");
const CustomBtn2 = document.getElementById("custom-button2");
CustomBtn2.addEventListener("click", function() {
    realFileBtn2.click();
});

const realFileBtn3 = document.getElementById("real-file3");
const CustomBtn3 = document.getElementById("custom-button3");
CustomBtn3.addEventListener("click", function() {
    realFileBtn3.click();
});

// fin upload files


/* perfil cliente Vista artista*/
function mostrarReferencias() {
    document.getElementById('es-comision').style.display = 'none';
    document.getElementById('gl-guardados').style.display = 'block';
    document.getElementById('tareas--').style.display = 'none';
}

function mostrarEsComision() {
    document.getElementById('es-comision').style.display = 'block';
    document.getElementById('gl-guardados').style.display = 'none';
    document.getElementById('tareas--').style.display = 'none';

}

function mostrarTareas() {
    document.getElementById('tareas--').style.display = 'block';
    document.getElementById('gl-guardados').style.display = 'none';
    document.getElementById('es-comision').style.display = 'none';

}

function ver_tareas() {
    if (clicked) {
        document.getElementById('crear-tarea').style.display = 'none';
        clicked = false;
    } else {
        document.getElementById('crear-tarea').style.display = 'block';
        clicked = true;
    }
}


// Info date
const dateNumber = document.getElementById('dateNumber');
const dateText = document.getElementById('dateText');
const dateMonth = document.getElementById('dateMonth');
const dateYear = document.getElementById('dateYear');

// Tasks Container
const tasksContainer = document.getElementById('tasksContainer');

const setDate = () => {
    const date = new Date();
    dateNumber.textContent = date.toLocaleString('es', { day: 'numeric' });
    dateText.textContent = date.toLocaleString('es', { weekday: 'long' });
    dateMonth.textContent = date.toLocaleString('es', { month: 'long' });
    dateYear.textContent = date.toLocaleString('es', { year: 'numeric' });
};

const addNewTask = event => {
    event.preventDefault();
    const { value } = event.target.taskText;
    if (!value) return;
    const task = document.createElement('div');
    task.classList.add('task', 'roundBorder');
    task.addEventListener('click', changeTaskState);
    task.textContent = value;

    tasksContainer.prepend(task);
    event.target.reset();
};

const changeTaskState = event => {
    event.target.classList.toggle('done');
};

const order = () => {
    const done = []; //Tareas echas
    const toDo = []; //Tareas por hacer
    tasksContainer.childNodes.forEach(el => {
        el.classList.contains('done') ? done.push(el) : toDo.push(el)
    })
    return [...toDo, ...done];
}

const renderOrderedTasks = () => {
    order().forEach(el => tasksContainer.appendChild(el))
}

setDate();