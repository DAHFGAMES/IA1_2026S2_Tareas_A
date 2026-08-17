/*
*-*-*-*-*-*-*-*-*
ARCHIVO: script.js
FASE 3 - FRONTEND (LOGICA)

Este archivo hace 3 cosas, siempre en el mismo orden:

  1) ESCUCHA  -> espera a que el usuario envie el formulario.
  2) PIDE     -> llama a la API del backend con fetch() de forma ASINCRONA.
  3) PINTA    -> toma el JSON que regreso y lo escribe dentro del HTML (el DOM).

ASINCRONO significa que la pagina NO se congela mientras espera la respuesta:
se manda la peticion, el navegador sigue vivo, y cuando la respuesta llega
se ejecuta el resto del codigo. Eso es lo que hacen async/await.

DOM = el arbol de elementos HTML tal como el navegador lo tiene en memoria.
Modificar el DOM es lo que cambia lo que se ve en pantalla.
*-*-*-*-*-*-*-*-*
*/


/*
*-*-*-*-*-*-*-*-*
BLOQUE 1: CONFIGURACION Y REFERENCIAS AL HTML
*-*-*-*-*-*-*-*-*
*/

// <-- Direccion del endpoint del backend. Es la MISMA ruta declarada en servidor.py.
// <-- Si el backend corre en otro puerto o maquina, solo se cambia esta linea.
const URL_API = "http://localhost:5000/api/inventario";

// <-- document.getElementById busca en el HTML el elemento que tenga ese id y lo guarda en una variable.
const formulario = document.getElementById("formulario");
const entradaItem = document.getElementById("entradaItem");
const mensaje = document.getElementById("mensaje");
const resultados = document.getElementById("resultados");

// <-- Referencias a los "huecos" que se van a rellenar con los datos del JSON.
const totalItems = document.getElementById("totalItems");
const encontrado = document.getElementById("encontrado");
const listaInvertida = document.getElementById("listaInvertida");
const listaOrdenada = document.getElementById("listaOrdenada");
const listaUnica = document.getElementById("listaUnica");


/*
*-*-*-*-*-*-*-*-*
BLOQUE 2: FUNCION QUE PINTA UNA LISTA EN EL DOM

Recibe un <ul> vacio y un arreglo de textos, y crea un <li> por cada elemento.
Se usa la misma funcion para las tres listas, asi no se repite codigo.
*-*-*-*-*-*-*-*-*
*/

function pintarLista(contenedor, elementos) {

    contenedor.innerHTML = "";                  // <-- borra lo que hubiera de una consulta anterior.

    elementos.forEach(function (elemento) {     // <-- forEach recorre el arreglo elemento por elemento.
        const li = document.createElement("li");  // <-- crea un nuevo <li> en memoria.
        li.textContent = elemento;                // <-- textContent escribe el texto (no interpreta HTML, evita inyeccion).
        contenedor.appendChild(li);               // <-- appendChild lo cuelga dentro del <ul>: ahi es cuando aparece en pantalla.
    });
}


/*
*-*-*-*-*-*-*-*-*
BLOQUE 3: CONSULTA ASINCRONA AL BACKEND

Flujo: item escrito -> URL -> fetch -> respuesta -> JSON -> pintar en el DOM.
*-*-*-*-*-*-*-*-*
*/

async function consultarInventario(item) {

    // <-- encodeURIComponent escapa espacios y simbolos para que la URL sea valida.
    // <-- URL final de ejemplo:  http://localhost:5000/api/inventario?item=pocion
    const url = URL_API + "?item=" + encodeURIComponent(item);

    // <-- fetch() manda la peticion GET. Devuelve una promesa, por eso se usa await:
    // <-- el codigo se detiene AQUI hasta que el servidor conteste, sin bloquear la pagina.
    const respuesta = await fetch(url);

    // <-- .json() lee el cuerpo de la respuesta y lo convierte de texto JSON a objeto de JavaScript.
    const datos = await respuesta.json();

    // <-- respuesta.ok es false cuando el servidor contesto con un codigo de error (400, 500...).
    if (!respuesta.ok || !datos.ok) {
        throw new Error(datos.error || "El servidor respondio con un error.");
    }

    return datos;                               // <-- se devuelve el objeto ya listo para pintarse.
}


/*
*-*-*-*-*-*-*-*-*
BLOQUE 4: EVENTO DEL FORMULARIO

addEventListener("submit", ...) = "cuando se envie el formulario, ejecuta esto".
Se dispara tanto al hacer clic en el boton como al presionar Enter.
*-*-*-*-*-*-*-*-*
*/

formulario.addEventListener("submit", async function (evento) {

    evento.preventDefault();                    // <-- evita el comportamiento por defecto (recargar la pagina), que borraria todo.

    const item = entradaItem.value.trim();      // <-- .value es lo que el usuario escribio; .trim() quita espacios sobrantes.

    if (item === "") {                          // <-- validacion basica antes de gastar una peticion.
        mensaje.textContent = "Escriba un item para buscar.";
        return;
    }

    mensaje.textContent = "Consultando al motor Prolog...";   // <-- aviso mientras se espera la respuesta.
    resultados.classList.add("oculto");                       // <-- se esconde el resultado viejo.

    // <-- try/catch: si algo falla (servidor apagado, CORS, error de Prolog) se atrapa
    // <-- el error y se avisa en pantalla en vez de dejar la pagina en silencio.
    try {

        const datos = await consultarInventario(item);        // <-- se espera el JSON del backend.

        // <-- A partir de aqui TODO lo que se pinta sale del objeto 'datos', o sea, de Prolog.
        totalItems.textContent = datos.totalItems;            // <-- numero calculado por length/2.

        // <-- El booleano de member/2 se traduce a un texto entendible para el usuario.
        encontrado.textContent = datos.encontrado
            ? "El item '" + datos.itemBuscado + "' SI esta en el inventario."
            : "El item '" + datos.itemBuscado + "' NO esta en el inventario.";

        // <-- Se cambia el color segun el resultado (clase CSS distinta).
        encontrado.className = datos.encontrado ? "si" : "no";

        pintarLista(listaInvertida, datos.inventarioInvertido);  // <-- resultado de reverse/2.
        pintarLista(listaOrdenada, datos.inventarioOrdenado);    // <-- resultado de msort/2 (con duplicados).
        pintarLista(listaUnica, datos.inventarioUnico);          // <-- resultado de sort/2 (sin duplicados).

        resultados.classList.remove("oculto");                // <-- ya con todo lleno, se muestra la seccion.
        mensaje.textContent = "";                             // <-- se limpia el aviso de "Consultando...".

    } catch (error) {

        mensaje.textContent = "Error: " + error.message;      // <-- se informa el problema al usuario.
        console.error(error);                                 // <-- y se deja el detalle completo en la consola del navegador.
    }
});
