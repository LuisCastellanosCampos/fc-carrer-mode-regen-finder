# Plan de implementación: Regen Finder MVP

## 1. Alcance y trazabilidad

Este plan convierte la especificación en una solución implementable para un
monorepo con backend en Python/FastAPI y frontend en Angular. No añade reglas
de negocio fuera de la spec.

| Parte del plan | RF cubiertos |
|---|---|
| Modelo de datos y validación | RF-1, RF-2 |
| Caso de uso de actualización anual | RF-1, RF-2 |
| Caso de uso de detección | RF-3, RF-4, RF-5, RF-6, RF-7 |
| API REST | RF-1 a RF-7 |
| Interfaz web | RF-3 a RF-7 |
| Persistencia y adaptadores | RF-1, RF-2, RF-7 |
| Estrategia de tests | RF-1 a RF-7 |

## 2. Estructura del monorepo

La estructura separa el dominio de los detalles tecnológicos. Los nombres de
código e identificadores estarán en inglés; los mensajes visibles y la
documentación estarán en español.

```text
habits-cli/
├── backend/
│   ├── domain/
│   │   ├── entities/          # Player, RegenMatch y value objects
│   │   ├── services/           # reglas de cruce, filtrado y ordenación
│   │   └── exceptions/         # errores de dominio
│   ├── application/
│   │   ├── ports/              # contratos de entrada y salida
│   │   └── use_cases/          # actualización y búsqueda
│   ├── adapters/
│   │   ├── inbound/http/       # controladores y esquemas REST
│   │   └── outbound/           # fuente anual y persistencia
│   └── main.py                 # composición de dependencias
├── frontend/
│   └── src/app/
│       ├── core/               # cliente HTTP y modelos
│       ├── features/regen/     # formulario y resultados
│       └── shared/             # componentes reutilizables
└── tests/
    ├── backend/
    └── frontend/
```

**Regla de dependencia:** `domain` no importará FastAPI, Angular ni clases de
persistencia. `application` dependerá de puertos; los adaptadores implementarán
esos puertos. La interfaz web consumirá el contrato REST y no reproducirá las
reglas de coincidencia.

## 3. Modelo de datos

### 3.1 Jugador activo

Campos obligatorios:

- `id`: identificador estable del jugador.
- `name`: nombre visible.
- `birth_date`: fecha ISO `YYYY-MM-DD`.
- `nationality`: nacionalidad normalizada.
- `position`: posición principal.
- `overall`: media numérica entre 0 y 100.
- `age`: edad no negativa.
- `season`: temporada de la actualización anual.

La fecha y la nacionalidad representan los datos del jugador activo que pueden
coincidir con los del jugador retirado introducidos por el usuario. La posición
del jugador retirado será opcional en la consulta.

### 3.2 Resultado de una posible coincidencia

`RegenMatch` será una proyección de lectura, no un jugador persistido. Incluirá
el jugador activo, el estado de coincidencia por fecha y nacionalidad, el estado
de coincidencia de posición cuando se haya enviado, y una explicación visible.

Ejemplo de payload de datos:

```json
{
  "player": {
    "id": "p-1042",
    "name": "Alejandro Ruiz",
    "birth_date": "1998-04-12",
    "nationality": "Spain",
    "position": "ST",
    "overall": 87,
    "age": 24,
    "season": "2026"
  },
  "match": {
    "birth_date": true,
    "nationality": true,
    "position": true,
    "is_possible_regen": true,
    "message": "Posible regen: coinciden fecha de nacimiento, nacionalidad y posición."
  }
}
```

La carga anual será una colección de jugadores. El identificador será la clave
de actualización: los nuevos se insertan y los existentes se reemplazan con
la versión nueva. La operación será atómica: si un registro falla, no se
aplicará ningún cambio.

**Cubre:** RF-1, RF-2, RF-4 y RF-7.

## 4. Algoritmo de cruce y detección

La fecha de nacimiento y la nacionalidad son criterios obligatorios y exactos.
La posición es opcional: aporta información, pero no convierte una coincidencia
principal en no coincidencia si difiere. El umbral `overall >= 85` se aplica a
los resultados según RF-5; debe confirmarse antes de cerrar el contrato si
también debe ocultar un candidato concreto con media inferior a 85.

```text
function findPossibleRegens(players, birthDate, nationality, position?):
    validate birthDate
    validate nationality is not empty
    if position is present:
        validate position

    candidates = []
    for player in players:
        dateMatches = player.birthDate == birthDate
        nationalityMatches = normalize(player.nationality) == normalize(nationality)

        if dateMatches and nationalityMatches and player.overall >= 85:
            positionMatches = null
            if position is present:
                positionMatches = normalize(player.position) == normalize(position)

            candidates.append(
                match(player, dateMatches, nationalityMatches, positionMatches)
            )

    sort candidates by player.overall descending,
                    then player.age descending,
                    then player.id ascending

    if candidates is empty:
        return empty list and informative Spanish message

    return candidates
```

La comparación no será aproximada: una fecha distinta o una nacionalidad
distinta excluye al jugador. El tercer criterio `id` solo garantiza un resultado
determinista mientras la duda sobre empates completos siga abierta; deberá
validarse como decisión definitiva.

**Cubre:** RF-3, RF-4, RF-5, RF-6 y RF-7.

## 5. Contrato de la API REST

### 5.1 Actualización anual

`PUT /api/v1/players/catalog`

Payload:

```json
{
  "season": "2026",
  "players": [
    {
      "id": "p-1042",
      "name": "Alejandro Ruiz",
      "birth_date": "1998-04-12",
      "nationality": "Spain",
      "position": "ST",
      "overall": 87,
      "age": 24
    }
  ]
}
```

Respuestas:

- `200 OK`: catálogo actualizado; devuelve temporada, cantidad insertada y
  cantidad actualizada.
- `400 Bad Request`: payload ausente, formato inválido, campos obligatorios
  ausentes, media fuera de rango, edad inválida o ID duplicado en la carga.
- `409 Conflict`: la temporada enviada es anterior a la última actualización,
  si se decide aplicar control temporal.
- `500 Internal Server Error`: fallo inesperado sin confirmar ni aplicar cambios.

El cuerpo de error tendrá un mensaje en español y, cuando proceda, el ID y
campo que originan el problema.

### 5.2 Búsqueda de posibles regens

`GET /api/v1/regens?birth_date=1998-04-12&nationality=Spain&position=ST`

Parámetros:

- `birth_date`: obligatorio, fecha ISO exacta del jugador retirado.
- `nationality`: obligatorio, nacionalidad del jugador retirado.
- `position`: opcional, posición del jugador retirado.

Respuesta `200 OK`:

```json
{
  "query": {
    "birth_date": "1998-04-12",
    "nationality": "Spain",
    "position": "ST"
  },
  "matches": [],
  "message": "No se encontraron posibles regens."
}
```

Respuestas:

- `200 OK`: devuelve la lista ordenada de coincidencias; una lista vacía es
  válida y debe incluir un mensaje informativo.
- `400 Bad Request`: fecha imposible, nacionalidad vacía o posición inválida.
- `503 Service Unavailable`: catálogo no disponible para consultar.

**Cubre:** RF-3, RF-4, RF-5, RF-6 y RF-7.

### 5.3 Convenciones REST

- Los nombres de campos del JSON estarán en `snake_case` e inglés para cumplir
  la convención de identificadores; los valores de `message` estarán en español.
- Las fechas usarán ISO 8601 sin hora.
- La API no expondrá objetos de persistencia directamente: devolverá esquemas
  de entrada y salida propios del adaptador HTTP.

## 6. Decisiones técnicas

| Decisión | Justificación | Alternativa descartada |
|---|---|---|
| Monorepo con backend y frontend separados | Permite mantener una única spec y una trazabilidad sencilla para un proyecto educativo. | Repositorios separados, que duplicarían configuración y coordinación. |
| Dominio hexagonal con puertos | Aísla las reglas de regen de FastAPI, Angular y persistencia, como exige la constitución. | Poner la lógica en controladores REST, que dificultaría las pruebas y acoplaría el dominio a la interfaz. |
| Dataset anual con upsert por ID | Conserva identificadores estables y permite actualizar medias y atributos sin duplicar jugadores. | Reemplazar toda la base sin identificar registros, que impediría distinguir altas, actualizaciones y errores. |
| Importación atómica | Evita que una actualización inválida deje una mezcla de temporadas o datos incompletos. | Importación parcial, que contradice RF-2 y puede producir resultados incorrectos. |
| Fecha ISO y comparación exacta | Evita ambigüedades regionales y respeta el criterio exacto de RF-3. | Fechas aproximadas o texto libre, que producirían falsos positivos. |
| Nacionalidad normalizada para comparar | Tolera diferencias de mayúsculas y espacios sin convertir la coincidencia en aproximada. | Comparación textual sin normalización, que generaría falsos negativos. |
| Posición como indicio, no filtro obligatorio | Respeta RF-4 y permite consultas cuando el usuario no conoce la posición. | Hacerla obligatoria, que excluiría coincidencias válidas. |
| Media mínima de 85 | Prioriza candidatos destacados y mantiene RF-5. | Mostrar cualquier media, que ampliaría resultados fuera del MVP. |
| Desempate por edad y después ID provisional | Produce resultados ordenados y repetibles. | Orden no determinista, que cambiaría la respuesta con los mismos datos. |
| Cliente Angular consumiendo REST | Mantiene la interfaz separada y permite reutilizar el contrato desde otros clientes. | Duplicar las reglas en frontend, con riesgo de resultados distintos al backend. |

Las dos dudas abiertas de la spec deben resolverse antes de cerrar el contrato:
confirmar el alcance del umbral 85 para candidatos concretos y aprobar el ID
como tercer criterio de desempate.

## 7. Estrategia de tests

### 7.1 Backend con pytest

Los tests de dominio no levantarán FastAPI ni accederán a la persistencia.

- RF-1: carga inicial, inserción de nuevos IDs, actualización de IDs existentes,
  duplicado dentro de la carga y atomicidad ante error.
- RF-2: campos ausentes, fecha imposible, nacionalidad vacía, media menor que
  0 o mayor que 100, edad negativa y colección válida.
- RF-3: coincidencia exacta de fecha y nacionalidad, coincidencia parcial y
  consultas inválidas.
- RF-4: posición ausente, posición coincidente y posición discrepante sin
  invalidar la coincidencia principal.
- RF-5: exclusión de media menor que 85 e inclusión de media exactamente 85.
- RF-6: orden por media, desempate por edad y orden determinista del tercer
  criterio.
- RF-7: lista vacía y mensaje informativo sin coincidencias.

Tests de adaptadores:

- Contrato del repositorio para leer y reemplazar el catálogo.
- Conversión de payloads HTTP a comandos de aplicación y de resultados a JSON.
- Códigos `200`, `400`, `409`, `503` y `500` según cada escenario.
- Verificación de que ningún error de validación persiste cambios parciales.

### 7.2 Frontend con ng test

- RF-3 y RF-4: formulario con fecha, nacionalidad y posición opcional; envío
  correcto y presentación de coincidencia de posición.
- RF-5 y RF-6: representación del orden recibido y media mínima visible.
- RF-7: estado de lista vacía con mensaje informativo.
- Errores `400`: mensajes en español y conservación de los valores válidos del
  formulario.
- Errores de disponibilidad: estado de error sin mostrar resultados antiguos
  como si fueran actuales.
- Cliente HTTP: payload correcto, parámetros opcionales y mapeo de respuestas.

### 7.3 Criterio de calidad

Cada RF tendrá al menos un test de comportamiento y los casos límite relevantes
tendrán cobertura explícita. La implementación no se considerará terminada si
`pytest` o `ng test` falla. Los tests de frontend no sustituirán los tests del
dominio; cada regla se verificará en el backend y la interfaz solo comprobará
presentación e integración.

**Cubre:** RF-1 a RF-7.