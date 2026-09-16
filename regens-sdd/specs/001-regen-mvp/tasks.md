# Tareas de implementación: Regen Finder MVP

Cada tarea está estimada para un máximo de 20-30 minutos. Deben ejecutarse en
el orden indicado y marcarse únicamente cuando se cumpla su criterio verificable.

## Decisiones y base del dominio

- [x] **T1. Resolver las dudas abiertas de la spec**
  - **RF:** RF-5, RF-6
  - **Hecho cuando:** La spec indica si la media mínima de 85 se aplica al candidato concreto y define el desempate completo posterior a media y edad.

- [x] **T2. Preparar la estructura del monorepo**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** Existen las áreas separadas para dominio, aplicación, adaptadores, API, frontend y tests, sin dependencias del dominio hacia la interfaz o la persistencia.

- [x] **T3. Definir el modelo de jugador activo**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** El modelo contempla `id`, `name`, `birth_date`, `nationality`, `position`, `overall`, `age` y `season`, con sus restricciones documentadas.

- [x] **T4. Definir el modelo de resultado de coincidencia**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** El resultado representa el jugador activo, los estados de coincidencia de fecha, nacionalidad y posición, el estado de posible regen y el mensaje en español.

- [x] **T5. Definir errores y puertos de aplicación**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** Existen contratos para actualizar el catálogo, consultar jugadores y comunicar errores sin importar FastAPI, Angular ni la persistencia.

## Catálogo anual

- [x] **T6. Implementar la validación de jugadores**
  - **RF:** RF-2
  - **Hecho cuando:** Se rechazan ID, nombre, fecha, nacionalidad, media o edad ausentes o inválidos, y los errores identifican el campo en español.

- [x] **T7. Implementar la validación de colecciones**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Se rechazan colecciones con IDs duplicados y se valida toda la colección antes de modificar el catálogo.

- [x] **T8. Implementar el adaptador de persistencia del catálogo**
  - **RF:** RF-1, RF-2, RF-7
  - **Hecho cuando:** El catálogo puede leerse y reemplazarse mediante el puerto definido, sin exponer detalles de persistencia al dominio.

- [x] **T9. Implementar la actualización anual mediante upsert**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Los IDs nuevos se insertan, los existentes se actualizan y una colección inválida no deja ningún cambio aplicado.

- [x] **T10. Probar la actualización anual del catálogo**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** Los tests cubren carga inicial, inserción, actualización por ID, duplicados, datos inválidos y atomicidad ante errores.

## Detección de posibles regens

- [ ] **T11. Implementar la normalización de datos de consulta**
  - **RF:** RF-3, RF-4
  - **Hecho cuando:** Las fechas se validan como fechas exactas, la nacionalidad y la posición se normalizan para comparar, y los valores vacíos se rechazan.

- [ ] **T12. Implementar el cruce exacto por fecha y nacionalidad**
  - **RF:** RF-3
  - **Hecho cuando:** Solo se consideran posibles coincidencias los jugadores activos que coinciden en ambos datos; las coincidencias parciales quedan excluidas.

- [ ] **T13. Implementar la posición opcional**
  - **RF:** RF-4
  - **Hecho cuando:** La consulta funciona sin posición, informa de coincidencia cuando se proporciona y conserva el resultado aunque la posición difiera.

- [ ] **T14. Implementar el filtro de media mínima**
  - **RF:** RF-5
  - **Hecho cuando:** Los resultados con media inferior a 85 se excluyen y un jugador con media exactamente 85 se incluye, conforme a la decisión de T1.

- [ ] **T15. Implementar la ordenación de coincidencias**
  - **RF:** RF-6
  - **Hecho cuando:** Las coincidencias se ordenan por media descendente, edad descendente y el criterio final aprobado en T1.

- [ ] **T16. Implementar el caso sin coincidencias**
  - **RF:** RF-7
  - **Hecho cuando:** Una consulta sin resultados devuelve una lista vacía y un mensaje informativo en español.

- [ ] **T17. Probar las reglas de detección**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** Los tests cubren coincidencia exacta, coincidencia parcial, posición ausente o discrepante, umbral 85, ordenación, empates y lista vacía.

## API REST

- [ ] **T18. Implementar el endpoint de actualización anual**
  - **RF:** RF-1, RF-2
  - **Hecho cuando:** `PUT /api/v1/players/catalog` acepta el payload definido, ejecuta el caso de uso y devuelve el resumen de inserciones y actualizaciones.

- [ ] **T19. Implementar el endpoint de búsqueda**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** `GET /api/v1/regens` acepta fecha, nacionalidad y posición opcional, y devuelve coincidencias ordenadas o lista vacía con mensaje.

- [ ] **T20. Mapear errores y códigos HTTP**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** La API devuelve los códigos `200`, `400`, `409`, `503` y `500` definidos, con mensajes en español y sin aplicar cambios parciales.

- [ ] **T21. Probar el contrato REST**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** Los tests de backend verifican payloads, parámetros opcionales, respuestas exitosas, errores de validación, catálogo no disponible y fallos inesperados.

## Frontend

- [ ] **T22. Implementar el formulario de búsqueda**
  - **RF:** RF-3, RF-4
  - **Hecho cuando:** La pantalla permite introducir fecha y nacionalidad obligatorias, posición opcional, y bloquea envíos con datos inválidos.

- [ ] **T23. Integrar cliente REST y estados de pantalla**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** El frontend envía los parámetros correctos, muestra coincidencias y posición, respeta el orden recibido y presenta estados vacío, error y carga en español.

- [ ] **T24. Probar el frontend con ng test**
  - **RF:** RF-3, RF-4, RF-5, RF-6, RF-7
  - **Hecho cuando:** `ng test` verifica validación del formulario, posición opcional, construcción de la petición, resultados ordenados, lista vacía y errores HTTP.

## Verificación final

- [ ] **T25. Ejecutar la validación completa del MVP**
  - **RF:** RF-1 a RF-7
  - **Hecho cuando:** `pytest` y `ng test` terminan correctamente, cada RF tiene al menos un test asociado y se revisan los criterios de finalización de la spec.