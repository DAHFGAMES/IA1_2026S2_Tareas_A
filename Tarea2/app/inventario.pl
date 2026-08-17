/*
*-*-*-*-*-*-*-*-*
ARCHIVO: inventario.pl
FASE 1 - MOTOR DE INFERENCIA (PROLOG)

Este archivo es el "cerebro" del proyecto. No sabe nada de Python ni de la web:
solo guarda datos (hechos) y sabe razonar sobre ellos (reglas).

Se compone de 3 bloques:
  1) HECHOS            -> las dos listas de items del aventurero.
  2) REGLA RECURSIVA   -> recorre e imprime la lista item por item.
  3) REGLA PRINCIPAL   -> usa los 6 metodos nativos pedidos y devuelve resultados.

RECORDATORIO DE NOTACION PROLOG:
  nombre/N  -> "N" es la ARIDAD = cuantos argumentos recibe el predicado.
               Ej: append/3 significa que append recibe 3 argumentos.
  Mayuscula -> es una VARIABLE (un hueco que Prolog debe rellenar).
  minuscula -> es un ATOMO (un valor constante, como el texto "espada").
  [C|R]     -> patron de lista: C es la Cabeza (1er elemento) y R el Resto.
*-*-*-*-*-*-*-*-*
*/


/*
*-*-*-*-*-*-*-*-*
BLOQUE 1: HECHOS
Un HECHO es algo que Prolog acepta como verdadero sin tener que demostrarlo.
Aqui cada hecho guarda UNA lista completa dentro de UN solo argumento.
*-*-*-*-*-*-*-*-*
*/

% <-- items_principales/1: hecho con la lista principal (4 items, 'pocion' esta DUPLICADO a proposito).
% <-- El duplicado es necesario para que despues se note la diferencia entre sort/2 y msort/2.
items_principales([espada, pocion, escudo, pocion]).

% <-- items_secundarios/1: hecho con la lista secundaria (3 items, todos distintos).
items_secundarios([antorcha, cuerda, mapa]).


/*
*-*-*-*-*-*-*-*-*
BLOQUE 2: REGLA RECURSIVA (mostrar_inventario/1)

RECURSIVIDAD = un predicado que se llama a si mismo con un problema mas pequeno,
hasta llegar a un caso tan simple que ya no necesita llamarse otra vez.

Necesita SIEMPRE dos clausulas:
  - CASO BASE     -> la lista vacia []. Aqui la recursion PARA. Sin el, seria infinita.
  - CASO RECURSIVO-> parte la lista en [Cabeza|Cola], imprime la Cabeza y vuelve
                     a llamarse con la Cola (que tiene 1 elemento menos).

Como la Cola siempre es mas corta que la lista original, tarde o temprano queda []
y entra el caso base: por eso NUNCA se cicla.
*-*-*-*-*-*-*-*-*
*/

% <-- CASO BASE: si la lista que llega es exactamente la lista vacia, ya no hay nada que imprimir.
mostrar_inventario([]) :-
    writeln('--- Fin del recorrido recursivo ---'),  % <-- writeln/1: escribe el texto y salta de linea.
    flush_output.                                    % <-- flush_output/0: obliga a que el texto salga YA en la consola.

% <-- CASO RECURSIVO: la lista trae al menos un elemento, se parte en Cabeza y Cola.
mostrar_inventario([Cabeza|Cola]) :-
    write('  -> Item encontrado en la mochila: '),   % <-- write/1: escribe SIN saltar de linea.
    writeln(Cabeza),                                 % <-- imprime el elemento actual y salta de linea.
    mostrar_inventario(Cola).                        % <-- LLAMADA RECURSIVA: repite el proceso con el resto.


/*
*-*-*-*-*-*-*-*-*
BLOQUE 3: REGLA PRINCIPAL (analizar_inventario/6)

Es la unica regla que llama el backend de Python.

ENTRADA (el backend la manda ya rellena):
  ItemBuscado          -> el item que el usuario escribio en la pagina web.

SALIDAS (llegan como variables vacias y Prolog las rellena por UNIFICACION):
  TotalItems           -> cuantos items hay en total.
  Encontrado           -> 'si' o 'no', segun si el ItemBuscado esta en el inventario.
  InventarioInvertido  -> el inventario al reves.
  InventarioUnico      -> ordenado y SIN duplicados.
  InventarioOrdenado   -> ordenado y CON duplicados.

UNIFICACION = el mecanismo por el que Prolog "amarra" un valor a una variable
vacia para que ambos lados de la comparacion queden iguales.
*-*-*-*-*-*-*-*-*
*/

analizar_inventario(ItemBuscado, TotalItems, Encontrado, InventarioInvertido, InventarioUnico, InventarioOrdenado) :-

    % <-- Se traen las dos listas desde los hechos del BLOQUE 1 (Principales y Secundarios se unifican con ellas).
    items_principales(Principales),
    items_secundarios(Secundarios),

    % <-- METODO 1 - append/3: pega la lista 1 con la lista 2 y deja el resultado en la 3ra variable.
    % <-- Resultado: el "Inventario General" con el que se trabaja de aqui en adelante.
    append(Principales, Secundarios, InventarioGeneral),

    % <-- METODO 2 - length/2: cuenta cuantos elementos tiene la lista y unifica ese numero con TotalItems.
    length(InventarioGeneral, TotalItems),

    % <-- METODO 3 - member/2: verifica si un elemento pertenece a la lista.
    % <-- Se envuelve en un if-then-else ( Condicion -> Entonces ; Si_no ) porque member/2 FALLA
    % <-- cuando el item no existe, y esa falla tumbaria toda la regla dejando al backend sin respuesta.
    % <-- Asi la regla siempre tiene exito y solo cambia el valor de Encontrado.
    (   member(ItemBuscado, InventarioGeneral)
    ->  Encontrado = si
    ;   Encontrado = no
    ),

    % <-- METODO 4 - reverse/2: da vuelta la lista (el ultimo pasa a ser el primero).
    reverse(InventarioGeneral, InventarioInvertido),

    % <-- METODO 5 - sort/2: ordena alfabeticamente Y ELIMINA los duplicados.
    sort(InventarioGeneral, InventarioUnico),

    % <-- METODO 6 - msort/2: ordena alfabeticamente pero CONSERVA los duplicados.
    % <-- Comparar InventarioUnico contra InventarioOrdenado deja ver que hacia cada uno.
    msort(InventarioGeneral, InventarioOrdenado),

    % <-- ULTIMA INSTRUCCION (como pide el enunciado): se llama a la regla recursiva del BLOQUE 2.
    % <-- Esto es lo que imprime item por item en la CONSOLA DEL SERVIDOR de Python.
    nl,                                              % <-- nl/0: una linea en blanco para separar la salida.
    writeln('--- Recorrido recursivo del Inventario General ---'),
    mostrar_inventario(InventarioGeneral).
