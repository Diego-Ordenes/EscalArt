function chat(solicitud) {
    document.querySelector(`#${solicitud}-input`).focus();
    document.querySelector(`#${solicitud}-input`).onkeyup = function(e) {
        if (e.keyCode === 13) { // enter, return
            document.querySelector(`#${solicitud}-submit`).click();
        }
    };

    document.querySelector(`#${solicitud}-submit`).onclick = function(e) {
        var roomName = document.querySelector(`#${solicitud}-input`).value;
        window.location.pathname = '/chat/' + roomName + '/';
    };
}