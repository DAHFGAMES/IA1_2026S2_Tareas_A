```python
md_content = """# Tarea 2: Enunciado y Análisis de Especificación
**Universidad San Carlos de Guatemala**  
**Facultad de Ingeniería — Escuela de Ingeniería en Ciencias y Sistemas**  
**Curso:** Inteligencia Artificial 1 (Sección A) — Segundo Semestre 2026  
**Tutores:** Roberto Miguel García Santizo | Jose Javier Bonilla Salazar  
**Ponderación:** 2 pts | **Tiempo estimado:** 4 hrs  

---

## 1. Marco Formativo

### 1.1 Valores
* **Honestidad:** Evitar el plagio de contenido, capturas de pantalla o proyectos que no hayan sido realizados por el estudiante.

### 1.2 Competencias
* **Competencia General:** Aplicar los fundamentos y funciones principales en el uso de listas en Prolog e integrarlos en una arquitectura cliente-servidor orientada a servicios (API REST).
* **Competencia Específica:** Implementación de las seis funciones principales de listas, uso de recursividad para mostrar los resultados, y construcción de un backend y frontend para la entrada y salida de datos dinámicos.

### 1.3 Objetivo
Desarrollar la lógica de manipulación de estructuras de datos dinámicas en Prolog, aplicando métodos nativos de listas (`append`, `length`, `member`, `reverse`, `sort`, `msort`) y algoritmos recursivos, para luego integrar este motor de inferencia lógico con un backend en Python y una interfaz gráfica (frontend) que permita la comunicación y gestión de inventarios para un videojuego RPG.

---

## 2. Material de Apoyo
* Diapositivas de la Sesión: *"Prolog Profundo: Listas, Unificación y Recursividad"*.
* Scripts desarrollados en clase (Ejemplos de iteración recursiva y uso de métodos nativos).
* Documentación oficial de SWI-Prolog.

---

## 3. Descripción de la Actividad

### Fase 1: Motor de Inferencia (Prolog)
1. **Definición de Hechos:**
   * Declara un hecho que contenga una lista de al menos 4 ítems (incluyendo al menos un ítem duplicado) para los ítems principales del aventurero.
   * Declara un hecho que contenga una lista de al menos 3 ítems distintos para los ítems secundarios del aventurero.
2. **Implementación de la Regla de Recorrido Recursivo:**
   * Crea un predicado recursivo para mostrar el inventario.
   * Debe contener el **Caso Base** (manejando la lista vacía `[]`) y el **Caso Recursivo** (desestructurando en `[H|T]` e imprimiendo el ítem).
3. **Regla Principal de Procesamiento:**
   * Crea una regla que reciba como entrada un `ItemBuscado` y devuelva mediante unificación las variables: `TotalItems`, `InventarioInvertido`, `InventarioUnico` e `InventarioOrdenado`.
   * Dentro de la regla, utiliza secuencialmente `append/3`, `length/2`, `member/2`, `reverse/2`, `sort/2` y `msort/2` para procesar el Inventario General.
   * Como última instrucción, llama a la regla recursiva pasándole el Inventario General para que imprima todos los ítems en la consola.

### Fase 2: Backend (Python + API REST)
1. Crea una API REST que exponga un endpoint `GET` (Framework/Librería a libre elección).
2. Configura **PySwip** para cargar el archivo `.pl` y ejecutar la consulta principal inyectando el parámetro ingresado.
3. Captura las variables unificadas devueltas por Prolog y formatéalas en una respuesta JSON.
4. Configura los middlewares de **CORS** para permitir peticiones desde el navegador.

### Fase 3: Frontend (HTML/JS)
1. Construye una interfaz web sencilla con un formulario de entrada de texto para buscar un ítem.
2. Utiliza JavaScript/TypeScript (`fetch` o `axios`) para enviar el dato ingresado al backend.
3. Captura la respuesta JSON y renderiza dinámicamente en pantalla el total de ítems, y las listas invertidas, con duplicados y sin duplicados.

---

## 4. Entregables
1. **Archivos de Código:** Código fuente completo (`.pl`, `.py`, archivos web) con comentarios técnicos que expliquen qué hace cada línea, la aridad de los métodos utilizados y la lógica del caso base/recursivo, así como la conexión del backend.
2. **Captura de Ejecución:** Una imagen clara de la interfaz Web mostrando los resultados de una consulta exitosa, y una captura paralela de la consola del servidor (Backend) evidenciando la impresión recursiva de los ítems lanzada por Prolog.

---

## 5. Cronograma

| Acción | Número de Semana | Fecha |
| :--- | :---: | :---: |
| **Asignación de tarea** | Semana 4 | 14/08/2026 |
| **Entrega de Tarea** | Semana 5 | 21/08/2026 |

---

## 6. Rúbrica de Calificación

### 6.1 Requisitos para optar a Calificación

| Tema | Descripción | Cumple (Sí/No) |
| :--- | :--- | :---: |
| **Compilación sin errores** | El archivo `.pl` y el script de Python deben compilar e iniciar sin lanzar ningún *Syntax Error* o *Traceback* fatal que impida levantar el servidor. | — |
| **Formato de entrega** | Se debe entregar en un repositorio llamado `IA1_2026S2_Tareas_A` dentro de una carpeta llamada `Tarea2`. | — |
| **Evidencia funcional** | Se debe incluir un archivo MD en el cual se detalle el funcionamiento del código, se describa el flujo y se documente de forma técnica su implementación, además de incluir capturas de pantalla de su funcionamiento y de las peticiones usadas. | — |
| **Comunicación Integral** | El backend debe permitir conexiones externas (CORS configurado) y el frontend debe consumir la API satisfactoriamente sin rechazos de red. | — |
| **Originalidad y Autoría** | El código no debe presentar plagio evidente ni copias idénticas a otros estudiantes. | — |

### 6.2 Detalle de la Calificación (100 pts)

#### 1. Habilidades (40 pts)
* **1.1 Calidad de código y comentarios (20 pts):** El código (`.pl`, `.py`, `.js`) está debidamente estructurado. Incluye comentarios técnicos claros que explican la aridad, lógica de unificación, rutas de la API y consumo en frontend.
* **1.2 Entregables y Capturas de Ejecución (20 pts):** Entrega todos los archivos requeridos y las capturas evidencian la ejecución del frontend (JSON renderizado) y la terminal del backend (impresión recursiva).

#### 2. Conocimientos (60 pts)
* **2.1 Lógica y Métodos Nativos (Prolog) (15 pts):** Define hechos y enlaza correctamente los 6 métodos solicitados (`append`, `length`, `member`, `reverse`, `sort`, `msort`) logrando unificación de variables.
* **2.2 Recursividad (Prolog) (15 pts):** El predicado implementa correctamente el caso base (`[]`) y el caso recursivo (`[H|T]`), iterando sin entrar en bucles infinitos.
* **2.3 Integración Backend (Python/API REST) (15 pts):** Expone correctamente la ruta API, ejecuta PySwip dinámicamente y serializa la respuesta unificada en un diccionario JSON sin errores de conversión.
* **2.4 Integración Frontend (Web) (15 pts):** El cliente captura el dato del formulario, consume la API de forma asíncrona (`fetch`) y plasma los datos dinámicamente en el DOM (HTML).

---

### 6.3 Penalizaciones

| Motivo de Penalización | Porcentaje | Justificación |
| :--- | :---: | :--- |
| **Error de sintaxis / No compila** | `-100%` | Si el archivo `.pl` lanza *Syntax Error* o el Backend no levanta (ej. puerto ocupado hardcodeado, falta de importaciones), el sistema no es evaluable. |
| **Hardcoding de variables** | `-40%` | El estudiante escribe a mano los valores esperados dentro de Prolog o ignora la respuesta del Backend y quema el JSON en el frontend. Destruye el propósito lógico. |
| **Omisión del Warning Singleton Variables** | `-10%` | Si al compilar, SWI-Prolog lanza advertencias de variables declaradas y no utilizadas. Falla de estándares técnicos. |
| **Error de CORS o Comunicación de API** | `-30%` | El frontend no puede renderizar la información debido a que no se manejaron las políticas CORS en el backend o la ruta Fetch está mal declarada. |
| **Entrega Tardía** | `-100%` | Penalización administrativa según los lineamientos de entrega de tareas prácticas. |
| **Plagio evidente o Copia de IA sin justificar** | `-100%` | Entregas con código idéntico entre estudiantes o estructuras avanzadas no cubiertas en clase sin capacidad de explicación técnica. |
"""

file_path = "Tarea2_Analisis_Especificacion.md"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"File generated: {file_path}")


```

```text
File generated: Tarea2_Analisis_Especificacion.md


```

Your Markdown file is ready


---

# Tarea #2 — Análisis y Especificación del Proyecto

## Información General

* **Universidad:** Universidad San Carlos de Guatemala


* **Facultad:** Facultad de Ingeniería


* **Escuela:** Escuela de Ingeniería en Ciencias y Sistemas


* **Curso:** Laboratorio - Inteligencia Artificial 1 - Sección A


* **Periodo:** Segundo Semestre 2026


* **Tutores:** Roberto Miguel García Santizo (Tutor 1) | Jose Javier Bonilla Salazar (Tutor 2)


* **Ponderación:** 2 puntos


* **Tiempo estimado:** 4 horas



---

## 1. Marco Formativo

### 1.1 Valores

* **Honestidad:** Evitar el plagio de contenido, capturas de pantalla o proyectos que no hayan sido realizados por el estudiante.



### 1.2 Competencias

* **Competencia General:** Aplicar los fundamentos y funciones principales en el uso de listas en Prolog e integrarlos en una arquitectura cliente-servidor orientada a servicios (API REST).


* **Competencia Específica:** Implementación de las seis funciones principales de listas, uso de recursividad para mostrar los resultados, y construcción de un backend y frontend para la entrada y salida de datos dinámicos.



### 1.3 Objetivo

Desarrollar la lógica de manipulación de estructuras de datos dinámicas en Prolog, aplicando métodos nativos de listas (`append`, `length`, `member`, `reverse`, `sort`, `msort`) y algoritmos recursivos, para luego integrar este motor de inferencia lógico con un backend en Python y una interfaz gráfica (frontend) que permita la comunicación y gestión de inventarios para un videojuego RPG.

---

## 2. Material de Apoyo

* Diapositivas de la Sesión: *"Prolog Profundo: Listas, Unificación y Recursividad"*.


* Scripts desarrollados en clase (Ejemplos de iteración recursiva y uso de métodos nativos).


* Documentación oficial de SWI-Prolog.



---

## 3. Descripción de las Actividades

### **Fase 1: Motor de Inferencia (Prolog)**

1. **Definición de Hechos:**
* Declara un hecho con una lista de al menos 4 ítems (debe incluir al menos un ítem duplicado) para los ítems principales del aventurero.


* Declara un hecho con una lista de al menos 3 ítems distintos para los ítems secundarios del aventurero.




2. **Implementación de la Regla de Recorrido Recursivo:**
* Crea un predicado recursivo para mostrar el inventario.


* Debe incluir el **Caso Base** (manejando la lista vacía `[]`) y el **Caso Recursivo** (desestructurando en `[H|T]` e imprimiendo el ítem).




3. **Regla Principal de Procesamiento:**
* Crea una regla que reciba como entrada un `ItemBuscado` y devuelva mediante unificación las variables: `TotalItems`, `InventarioInvertido`, `InventarioUnico` e `InventarioOrdenado`.


* Utiliza secuencialmente los predicados nativos `append/3`, `length/2`, `member/2`, `reverse/2`, `sort/2` y `msort/2` para procesar el Inventario General.


* Como última instrucción, invoca la regla recursiva pasándole el Inventario General para imprimir todos los ítems en consola.





### **Fase 2: Backend (Python + API REST)**

1. Crea una API REST que exponga un endpoint `GET` (Framework o librería a libre elección).


2. Configura **PySwip** para cargar el archivo `.pl` y ejecutar la consulta principal inyectando el parámetro ingresado.


3. Captura las variables unificadas devueltas por Prolog y formatéalas en una respuesta en formato JSON.


4. Configura los middlewares de **CORS** para permitir peticiones externas desde el navegador.



### **Fase 3: Frontend (HTML/JS)**

1. Construye una interfaz web sencilla con un formulario de entrada de texto para buscar un ítem.


2. Utiliza JavaScript/TypeScript (`fetch` o `axios`) para enviar el dato ingresado al backend de forma asíncrona.


3. Captura la respuesta JSON y renderiza dinámicamente en el DOM el total de ítems y las listas invertidas, con duplicados y sin duplicados.



---

## 4. Entregables

1. **Archivos de Código:** Código fuente completo (`.pl`, `.py`, archivos web) con comentarios técnicos detallados explicando cada línea, la aridad de los métodos utilizados, la lógica del caso base/recursivo y la conexión del backend.


2. **Captura de Ejecución:**
* Una captura clara de la interfaz Web mostrando los resultados de una consulta exitosa.


* Una captura paralela de la consola del servidor (Backend) evidenciando la impresión recursiva de los ítems realizada por Prolog.





---

## 5. Cronograma

| Acción | Número de Semana | Fecha |
| --- | --- | --- |
| **Asignación de tarea** | Semana 4 | 14/08/2026

 |
| **Entrega de Tarea** | Semana 5 | 21/08/2026

 |

---

## 6. Rúbrica de Calificación

### 6.1 Requisitos para Optar a Calificación

| Tema | Descripción |
| --- | --- |
| **Compilación sin errores** | El archivo `.pl` y el script de Python deben compilar e iniciar sin lanzar ningún *Syntax Error* o *Traceback* fatal que impida levantar el servidor.

 |
| **Formato de entrega** | Debe entregarse en el repositorio `IA1_2026S2_Tareas_A` dentro de la carpeta `Tarea2`.

 |
| **Evidencia funcional** | Incluir un archivo `README.md` (o `.md`) con la documentación técnica del código, flujo de datos, capturas de funcionamiento y capturas de las peticiones usadas.

 |
| **Comunicación Integral** | Backend con CORS configurado correctamente para permitir consumo sin errores de red en el frontend.

 |
| **Originalidad y Autoría** | Código sin plagio evidente ni copias idénticas.

 |

---

### 6.2 Detalle de la Calificación (Total: 100 pts)

#### 1. Habilidades (40 pts)

* **1.1 Calidad de código y comentarios (20 pts):** Código estructurado (`.pl`, `.py`, `.js`) con comentarios técnicos que expliquen la aridad, lógica de unificación, rutas API y consumo en frontend.


* **1.2 Entregables y Capturas de Ejecución (20 pts):** Entrega de todos los archivos solicitados y capturas que demuestren el renderizado JSON en frontend y la salida en terminal del backend.



#### 2. Conocimientos (60 pts)

* **2.1 Lógica y Métodos Nativos en Prolog (15 pts):** Declaración correcta de hechos y uso de los 6 métodos solicitados (`append`, `length`, `member`, `reverse`, `sort`, `msort`) logrando unificación de variables.


* **2.2 Recursividad en Prolog (15 pts):** Implementación del caso base (`[]`) y caso recursivo (`[H|T]`) evitando bucles infinitos.


* **2.3 Integración Backend Python / API REST (15 pts):** Configuración adecuada de la API REST, integración con PySwip y serialización limpia a JSON.


* **2.4 Integración Frontend Web (15 pts):** Captura de datos, consumo asíncrono con `fetch` y actualización dinámica del DOM.



---

### 6.3 Penalizaciones

| Motivo de Penalización | Porcentaje | Justificación |
| --- | --- | --- |
| **Error de sintaxis / No compila** | `-100%` | El archivo `.pl` genera *Syntax Error* o el Backend no inicia (puerto ocupado, faltan dependencias).

 |
| **Hardcoding de variables** | `-40%` | Quemar datos requeridos dentro de Prolog o ignorar la respuesta de la API en el frontend.

 |
| **Omisión del Warning Singleton Variables** | `-10%` | Presencia de advertencias por variables declaradas y no utilizadas en SWI-Prolog.

 |
| **Error de CORS o Comunicación de API** | `-30%` | Fallo de comunicación entre frontend y backend por políticas de CORS o rutas mal declaradas.

 |
| **Entrega Tardía** | `-100%` | Incumplimiento de la fecha límite fijada en el cronograma.

 |
| **Plagio o copia no justificada de IA** | `-100%` | Código idéntico entre estudiantes o uso de estructuras avanzadas no explicadas.

 |