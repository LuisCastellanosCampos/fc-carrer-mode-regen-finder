# Tareas: frontend profesional para búsqueda de regens

Estas tareas pertenecen a una fase posterior al MVP. No deben comenzar hasta
aprobarse la especificación y el plan de esta carpeta.

## Aprobación y dirección visual

- [ ] **P1. Aprobar el alcance del frontend**
  - **PF:** PF-1 a PF-7
  - **Hecho cuando:** Se confirma que la fase solo modifica Angular, conserva
    `GET /api/v1/regens`, no añade funciones de FUTBIN fuera de alcance y define
    los anchos responsive y criterios de accesibilidad.

- [ ] **P2. Fijar identidad y composición**
  - **PF:** PF-1, PF-5, PF-6
  - **Hecho cuando:** Se documentan nombre, paleta, tipografía, jerarquía visual,
    shell, navegación activa y decisión entre tarjetas, tabla o ambas sin usar
    marca ni assets de terceros no autorizados.

## Shell y búsqueda

- [ ] **P3. Implementar el shell de producto**
  - **PF:** PF-1, PF-6
  - **Hecho cuando:** La aplicación tiene cabecera, navegación real, landmarks,
    título de página y vista de búsqueda activa en escritorio y móvil.

- [ ] **P4. Rediseñar el panel de filtros**
  - **PF:** PF-2, PF-4, PF-5
  - **Hecho cuando:** Fecha, nacionalidad y posición conservan el payload actual,
    tienen labels y estados claros, existen buscar y limpiar, y el panel se
    adapta sin overflow desde 320 px.

- [ ] **P5. Cubrir la interacción del formulario**
  - **PF:** PF-2, PF-4, PF-7
  - **Hecho cuando:** Las validaciones aparecen junto a los campos, los envíos
    duplicados quedan bloqueados durante la carga, los criterios se conservan en
    éxito/error y limpiar devuelve el estado inicial.

## Resultados y estados

- [ ] **P6. Implementar la presentación de resultados**
  - **PF:** PF-3, PF-6
  - **Hecho cuando:** Cada `RegenMatch` muestra nombre, media, edad, posición,
    nacionalidad, fecha, temporada y señales explícitas de coincidencia, sin
    cambiar el orden ni filtrar la respuesta.

- [ ] **P7. Implementar estados de consulta**
  - **PF:** PF-4, PF-5
  - **Hecho cuando:** Existen estados inicial, carga, resultados, vacío, error de
    validación y error recuperable, con mensajes en español, roles accesibles y
    acción de reintento cuando proceda.

## Responsive, accesibilidad y pruebas

- [ ] **P8. Aplicar tokens y estilos responsive**
  - **PF:** PF-5, PF-6
  - **Hecho cuando:** El layout funciona a 320 px, 768 px y 1440 px, mantiene
    foco visible, evita solapamientos y usa una identidad visual propia orientada
    a datos.

- [ ] **P9. Añadir pruebas del feature**
  - **PF:** PF-2, PF-3, PF-4, PF-7
  - **Hecho cuando:** Hay tests para validación, payload, carga, error, vacío,
    limpieza, coincidencias con posición coincidente/no coincidente y reintento.

- [ ] **P10. Verificar accesibilidad y contrato**
  - **PF:** PF-1, PF-3, PF-5, PF-7
  - **Hecho cuando:** Se comprueban labels, landmarks, roles, foco y teclado, y
    una prueba confirma que el servicio conserva los nombres y valores del
    contrato `GET /api/v1/regens`.

- [ ] **P11. Validar build y regresión**
  - **PF:** PF-1 a PF-7
  - **Hecho cuando:** `npm test` y `npm run build` pasan, las pruebas existentes
    siguen verdes y no se ha modificado el backend ni el formato JSON.
