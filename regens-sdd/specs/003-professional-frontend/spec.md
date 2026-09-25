# Especificación: frontend profesional para búsqueda de regens

## Contexto y objetivo

El frontend actual sirve como prueba funcional del MVP, pero presenta una única
forma centrada y una lista básica de resultados. Esta fase lo convertirá en una
experiencia de scouting más clara, densa y reutilizable para jugadores de EA FC:
permitirá configurar una búsqueda, interpretar rápidamente las coincidencias y
repetir consultas con menos fricción.

La referencia de producto será la organización de herramientas de datos como
FUTBIN: navegación persistente, búsqueda y filtros destacados, resultados
comparables y una interfaz responsive orientada a explorar información. La
aplicación tendrá identidad, textos, componentes y recursos propios; no copiará
marca, código, imágenes, iconos propietarios ni diseño exacto de FUTBIN.

## Alcance

La fase cubre únicamente la aplicación Angular en `FRONTEND/`. Mantendrá el
contrato de `GET /api/v1/regens` y las reglas de negocio del MVP y de la
integración del catálogo. No requiere endpoints nuevos, cambios de JSON ni
modificaciones del backend.

El resultado será una vista principal de búsqueda de regens con shell de
producto, formulario de filtros, resumen de consulta, resultados ricos y estados
completos de carga, error, vacío y validación. La interfaz no debe simular
capacidades que la API no ofrece.

## Usuarios

- Jugadores de EA FC que consultan posibles regens durante una partida.
- Usuarios que necesitan comparar varias coincidencias sin perder los criterios
  de la búsqueda.

## Historias de usuario

- Como jugador, quiero reconocer de inmediato qué hace la aplicación y acceder
  a la búsqueda desde una navegación clara.
- Como jugador, quiero introducir los datos del jugador retirado en un panel de
  filtros comprensible y ejecutar la búsqueda sin pasos innecesarios.
- Como jugador, quiero ver cada posible regen con su media, edad, posición,
  nacionalidad y señales de coincidencia para comparar candidatos rápidamente.
- Como jugador, quiero conservar el contexto de mi consulta mientras reviso los
  resultados y poder limpiar los filtros para empezar otra búsqueda.
- Como usuario móvil, quiero usar la misma funcionalidad en una pantalla pequeña
  sin que la tabla, los botones o los mensajes se desborden.
- Como usuario con teclado o lector de pantalla, quiero identificar los campos,
  estados y resultados sin depender únicamente del color o del ratón.

## Requisitos funcionales

### PF-1. Proporcionar un shell de producto reconocible

La aplicación deberá mostrar una estructura consistente con:

- cabecera con nombre propio de la herramienta y acceso a la búsqueda;
- navegación secundaria o lateral preparada para la vista activa, sin enlaces
  falsos a funciones no implementadas;
- contenido principal con título, descripción breve y área de trabajo;
- pie o información secundaria solo cuando aporte contexto real, sin desplazar
  la búsqueda innecesariamente.

La vista activa deberá poder identificarse visualmente y mediante atributos
accesibles. El shell no deberá mostrar la marca FUTBIN ni presentar la aplicación
como afiliada a EA o FUTBIN.

### PF-2. Ofrecer un panel de búsqueda orientado a filtros

El formulario deberá conservar `birth_date`, `nationality` y `position` del
contrato actual y deberá:

- presentar fecha de nacimiento como control de fecha con validación de fecha de
  calendario;
- presentar nacionalidad como campo obligatorio con etiqueta visible y ayuda
  contextual; no se asumirá un catálogo de países que la API no proporciona;
- presentar posición como filtro opcional mediante controles fáciles de escanear,
  manteniendo la posibilidad de introducir el valor aceptado por el backend;
- incluir acciones de buscar y limpiar, con estados disabled/loading claros;
- mostrar los errores junto al campo y un resumen accesible cuando el formulario
  no se pueda enviar;
- conservar los valores mientras se muestran resultados o un error recuperable.

La interfaz no añadirá filtros de media mínima, potencial, liga, club u otros
criterios que no formen parte del contrato actual. La media mínima de 85 seguirá
siendo una regla del backend, no una configuración visual engañosa.

### PF-3. Presentar resultados para comparar candidatos

Cuando la API devuelva coincidencias, la vista deberá mostrar:

- un resumen con los criterios consultados y el número de coincidencias;
- tarjetas o filas compactas por jugador, con nombre, media, edad, posición,
  nacionalidad, fecha de nacimiento y temporada cuando estén disponibles;
- una señal explícita y comprensible para cada coincidencia de fecha,
  nacionalidad y posición, distinguiendo posición coincidente, no coincidente y
  no informada;
- el mensaje de posible regen devuelto por la API sin ocultar el detalle de la
  comparación;
- una jerarquía visual que destaque la media y el nombre, pero que no dependa
  solo del color;
- el orden recibido de la API, que ya representa el criterio determinista del
  dominio.

La interfaz no modificará, reordenará ni filtrará silenciosamente la colección
recibida. Si se incorpora una vista alternativa de tabla, deberá representar los
mismos datos y conservar la accesibilidad de las tarjetas.

### PF-4. Resolver todos los estados de la consulta

La aplicación deberá representar de forma diferenciada:

- estado inicial, explicando qué datos hacen falta para comenzar;
- carga, con feedback visible y sin permitir envíos duplicados;
- éxito con resultados;
- éxito sin resultados, conservando una acción clara para ajustar o limpiar la
  consulta;
- error de validación del formulario;
- error de red, servidor o catálogo, con un mensaje en español y una acción para
  reintentar sin perder los criterios.

Los estados dinámicos deberán anunciarse de forma compatible con lectores de
pantalla mediante `role="status"`, `role="alert"` u otro mecanismo equivalente
cuando corresponda.

### PF-5. Ser usable en escritorio y móvil

La experiencia deberá adaptarse como mínimo a anchos de 320 px, 768 px y
1440 px sin scroll horizontal accidental. En escritorio podrá usar una
composición de panel de filtros y resultados; en móvil deberá priorizar el
contenido, apilar los campos y convertir la navegación o filtros secundarios en
un patrón accesible de expansión.

Los controles táctiles tendrán un tamaño utilizable, el texto se podrá leer sin
zoom y ningún nombre, etiqueta, mensaje o botón podrá quedar cortado u ocultar
otro contenido. El foco de teclado deberá ser visible en todos los controles
interactivos.

### PF-6. Aplicar una identidad visual propia y consistente

El frontend deberá definir un lenguaje visual coherente para una herramienta de
scouting: tipografía con jerarquía clara, colores con contraste suficiente,
escalas de espaciado, estados de interacción y componentes reutilizables. Podrá
usar una atmósfera deportiva y de datos, pero no replicará la identidad ni los
recursos de FUTBIN.

La composición deberá priorizar densidad útil, lectura rápida y comparación. No
se añadirán gráficos decorativos, métricas ficticias, publicidad, noticias,
monedas, mercado, squad builder ni contenido editorial que no tenga soporte en
el dominio.

### PF-7. Mantener el contrato y la calidad del frontend

El frontend deberá consumir el servicio existente sin cambiar sus nombres de
campos ni su semántica. Los textos visibles y mensajes de error estarán en
español; los identificadores de código seguirán en inglés.

Cada requisito de esta fase deberá tener pruebas automatizadas de componente o
integración. Las pruebas deberán verificar al menos el envío válido, validación,
estados de carga/error/vacío, representación de una coincidencia con posición
coincidente y no coincidente, acción de limpiar y comportamiento responsive
mediante una estrategia adecuada al entorno de tests.

## Requisitos no funcionales

- No se añadirán dependencias frontend salvo justificación explícita y
  actualización de esta spec.
- Se mantendrá `ChangeDetectionStrategy.OnPush` y la separación actual entre
  componentes de presentación y el servicio de API cuando siga siendo adecuada.
- La interfaz deberá funcionar con teclado, foco visible, etiquetas asociadas y
  contraste suficiente según WCAG 2.2 AA en los flujos principales.
- Los errores de API no expondrán detalles técnicos al usuario, aunque podrán
  registrarse de forma segura para depuración.
- La carga inicial no deberá depender de imágenes externas ni de servicios de
  terceros para mostrar la búsqueda.
- Los recursos visuales, si se incorporan, deberán tener licencia compatible y
  quedar documentados; no se reutilizarán assets de FUTBIN.

## Casos límite

- El usuario envía el formulario sin fecha o nacionalidad.
- La fecha tiene formato correcto pero no existe en el calendario.
- La posición se omite.
- La API devuelve cero coincidencias.
- La API devuelve varias coincidencias con posición coincidente, no coincidente
  o no informada.
- La API tarda o falla después de que el usuario haya completado el formulario.
- El usuario pulsa buscar varias veces durante la carga.
- El usuario limpia el formulario después de una respuesta.
- La pantalla tiene 320 px de ancho y un nombre o mensaje largo.
- El usuario navega el flujo completo únicamente con teclado.

## Fuera de alcance

- Cambiar las reglas de detección, ordenación o media mínima del backend.
- Crear endpoints de catálogo, autenticación, favoritos, perfiles o sincronización
  con una cuenta de EA.
- Implementar mercado, precios, SBC, noticias, plantillas, comparador avanzado,
  estadísticas históricas o potencial si no existe antes un contrato aprobado.
- Copiar la marca, assets, textos o diseño exacto de FUTBIN.
- Añadir analítica, publicidad o seguimiento de usuarios.

## Criterios de finalización

- La vista ya no es un formulario aislado: presenta un shell reconocible y una
  experiencia completa de búsqueda.
- Una búsqueda válida usa el contrato actual y muestra resultados comparables sin
  alterar el orden ni los datos del backend.
- Validación, carga, error, vacío y limpieza tienen representación y pruebas.
- La experiencia es utilizable a 320 px, 768 px y 1440 px, con teclado y lector
  de pantalla en el flujo principal.
- La identidad visual es propia, consistente y orientada a datos.
- No se han añadido dependencias ni capacidades fuera de alcance sin actualizar
  la spec.
- Todos los requisitos PF tienen pruebas automatizadas asociadas.
