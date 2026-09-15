# Especificación: búsqueda de regens

## Contexto y objetivo

Los jugadores retirados del Modo Carrera pueden reaparecer como nuevos jugadores
con la misma fecha de nacimiento y nacionalidad. Esta funcionalidad permitirá
mantener un catálogo de jugadores en activo, actualizado una vez al año, para
que un usuario pueda comprobar si el jugador que considera un posible regen
coincide con los datos del jugador en la BBDD. La posición servirá como indicio
adicional, pero no será obligatoria para realizar la consulta.

## Usuarios

- Jugadores de EA FC que buscan identificar regens en su partida.
- Personas que mantienen o actualizan una base de datos de jugadores.

## Historias de usuario

- Como responsable del catálogo, quiero actualizar anualmente los datos de los
  jugadores en activo para mantener sus medias y demás atributos al día.
- Como jugador, quiero introducir la fecha de nacimiento, nacionalidad del
  jugador encontrado para comprobar si un jugador de la BBDD puede ser su regen.
- Como jugador, quiero añadir la posición como dato opcional para reforzar o
  debilitar la posible coincidencia.

## Requisitos funcionales

### RF-1. Actualizar anualmente el catálogo de jugadores activos

El sistema deberá permitir actualizar el catálogo de jugadores en activo con
los datos disponibles para una nueva temporada. La actualización de un jugador
se determinará por su ID; un ID existente actualizará sus datos y un ID nuevo
añadirá un jugador.

**Criterios de aceptación (EARS):**

- Cuando se cargue una actualización anual válida, el sistema deberá incorporar
  los jugadores nuevos y actualizar los jugadores con el mismo ID.
- Cuando una colección incluya un ID repetido dentro de la propia carga, el
  sistema deberá rechazar la carga completa e informar del duplicado.
- Cuando una actualización sea válida, el sistema no deberá conservar una
  versión anterior de un jugador cuyo ID haya sido actualizado.

### RF-2. Validar los datos de los jugadores

Cada jugador deberá tener ID, nombre, fecha de nacimiento válida, nacionalidad
no vacía, media numérica entre 0 y 100 y edad no negativa.

**Criterios de aceptación (EARS):**

- Si falta un dato obligatorio o su valor no es válido, el sistema deberá
  rechazar la carga completa y mostrar un mensaje claro en español.
- Si todos los jugadores contienen datos válidos, el sistema deberá aceptar la
  colección para su incorporación o actualización.

### RF-3. Comprobar un posible regen

El sistema deberá permitir consultar un jugador activo proporcionando la fecha
de nacimiento y la nacionalidad del jugador retirado que el usuario considera
su posible origen. El jugador activo será una posible coincidencia únicamente
cuando ambos valores coincidan exactamente.

**Criterios de aceptación (EARS):**

- Cuando la fecha y la nacionalidad sean válidas, el sistema deberá considerar
  únicamente jugadores activos que coincidan exactamente con ambos valores.
- Cuando la fecha de nacimiento o la nacionalidad de la búsqueda sean
  inválidas, el sistema deberá rechazar la búsqueda y mostrar un mensaje claro
  en español.
- Cuando un jugador activo coincida solo en uno de los dos valores, el sistema
  deberá indicar que no es una coincidencia válida.

### RF-4. Considerar la posición como criterio opcional

El sistema deberá permitir indicar la posición del jugador retirado como dato
opcional. Si se proporciona, deberá mostrar si la posición del jugador activo
coincide, sin invalidar la consulta cuando no se proporcione o no coincida.

**Criterios de aceptación (EARS):**

- Cuando se indique una posición, el sistema deberá informar de si coincide
  con la posición del jugador activo.
- Cuando no se indique una posición, el sistema deberá resolver la consulta
  usando la fecha de nacimiento y la nacionalidad.
- Cuando la posición no coincida, el sistema deberá conservar la coincidencia
  por fecha y nacionalidad, pero señalar la discrepancia de posición.

### RF-5. Filtrar por media mínima

El filtro de media mínima se aplicará a cada candidato concreto. Los
resultados deberán incluir únicamente jugadores cuya media sea igual o
superior a 85; un candidato con media inferior a 85 no se mostrará.

**Criterios de aceptación (EARS):**

- Cuando existan coincidencias, el sistema deberá excluir las que tengan una
  media inferior a 85.
- Cuando una coincidencia tenga una media exactamente igual a 85, el sistema
  deberá incluirla.

### RF-6. Resolver varias posibles coincidencias

Si existen varios jugadores activos que coinciden con la fecha de nacimiento y
la nacionalidad, el sistema deberá ordenar las posibles coincidencias por
media descendente. Si dos o más jugadores tienen la misma media, deberá
mostrar primero al de mayor edad. Si también coinciden la media y la edad, se
ordenarán por `id` ascendente para resolver el empate de forma determinista.

**Criterios de aceptación (EARS):**

- Cuando haya varias posibles coincidencias válidas, el sistema deberá devolverlas
  ordenadas de mayor a menor media.
- Cuando varias coincidencias tengan la misma media, el sistema deberá ordenar
  primero al jugador de mayor edad.
- Cuando solo exista una posible coincidencia válida, el sistema deberá
  devolverla como resultado principal.

### RF-7. Informar de la ausencia de coincidencias

El sistema deberá comunicar claramente cuando no existan jugadores activos que
cumplan la fecha, la nacionalidad y la media mínima solicitadas.

**Criterios de aceptación (EARS):**

- Cuando no existan posibles coincidencias válidas, el sistema deberá devolver
  una lista vacía y mostrar un mensaje informativo en español.

## Requisitos no funcionales

- Las reglas de coincidencia, filtrado, posición y ordenación deberán producir el mismo
  resultado ante los mismos datos de entrada.
- Los errores de validación deberán identificar de forma comprensible el
  problema detectado.
- Las operaciones deberán preservar la integridad de la base de jugadores y no
  dejar actualizaciones parciales tras un error de validación.
- Los mensajes visibles para el usuario y la documentación funcional deberán
  estar escritos en español.

## Casos límite

- El catálogo inicial está vacío.
- La carga contiene jugadores duplicados por ID.
- La carga contiene un jugador sin ID, nombre, fecha, nacionalidad, media o edad.
- La carga contiene una fecha imposible, una media fuera del rango permitido o
  una edad negativa.
- La consulta usa una fecha imposible o una nacionalidad vacía.
- La consulta no incluye posición.
- La posición indicada no coincide con la del jugador activo.
- Hay varios jugadores con la misma fecha, nacionalidad y media.
- No hay coincidencias con media igual o superior a 85.
- Existe una coincidencia con media exactamente igual a 85.
- Una actualización reemplaza los datos de un jugador existente por su ID.

## Fuera de alcance

- Identificar regens mediante atributos distintos de fecha de nacimiento,
  nacionalidad, posición, media y edad.
- Confirmar que un jugador es un regen con información distinta a la
  coincidencia de atributos definida.
- Editar manualmente los datos de un jugador fuera de la actualización anual.
- Gestionar varias fuentes de datos simultáneas.
- Incluir estadísticas históricas, potencial, posiciones secundarias o evolución
  temporal.
- Definir decisiones técnicas o de arquitectura.

## Criterios de finalización

- Se puede actualizar anualmente el catálogo de jugadores activos y actualizar
  registros existentes por ID.
- Se rechazan cargas inválidas de forma completa, sin actualizaciones parciales.
- Se comprueba un posible regen por fecha de nacimiento y nacionalidad exactas.
- La posición puede usarse como criterio adicional sin ser obligatoria.
- Solo se muestran coincidencias con media igual o superior a 85.
- Las posibles coincidencias se ordenan por media y edad según lo especificado.
- Las entradas inválidas y las búsquedas sin resultados generan mensajes claros.
- Todos los requisitos funcionales tienen pruebas automatizadas asociadas.

## Decisiones de T1

- La media mínima de 85 se aplica a cada candidato concreto de la consulta.
  Los candidatos con `overall < 85` se excluyen y los candidatos con
  `overall = 85` se incluyen.
- Un empate completo de media y edad se resuelve por `id` ascendente.