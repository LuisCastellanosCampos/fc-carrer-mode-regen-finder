# Plan de implementación: frontend profesional para búsqueda de regens

## 1. Trazabilidad

Esta fase depende de `001-regen-mvp` y consume el contrato estabilizado por
`002-sofifa-catalog`. Su alcance está limitado a Angular y no modifica dominio,
API ni persistencia.

| Área | Requisitos |
|---|---|
| Shell, navegación y composición | PF-1, PF-6 |
| Formulario y acciones | PF-2, PF-4 |
| Resultados y comparación | PF-3, PF-4 |
| Responsive y accesibilidad | PF-5, PF-6, PF-7 |
| Contrato, pruebas y calidad | PF-7 |

## 2. Flujo propuesto

1. Montar una aplicación shell con cabecera, navegación de la vista activa y
   área principal de búsqueda.
2. Convertir el formulario actual en un panel de filtros visualmente agrupado,
   conservando sus controles reactivos y el payload del servicio.
3. Ejecutar la consulta existente y mostrar un resumen persistente de los
   criterios enviados.
4. Representar cada `RegenMatch` en una tarjeta o fila densa con sus atributos y
   estados de coincidencia.
5. Cubrir explícitamente carga, error, vacío, validación y limpieza.
6. Aplicar breakpoints y navegación por teclado, y comprobar la experiencia en
   320 px, 768 px y 1440 px.
7. Ejecutar pruebas de Angular y build de producción sin cambiar el backend.

## 3. Fronteras arquitectónicas

- `RegenApiService` seguirá siendo el único punto de acceso HTTP del feature.
- El componente de búsqueda coordinará formulario, estado de consulta y
  resultados; los componentes visuales podrán recibir datos mediante inputs y
  emitir acciones sin conocer HTTP.
- Los modelos `Player`, `RegenMatch` y `RegenSearchResponse` seguirán siendo la
  representación del contrato actual.
- El estilo global definirá tokens mínimos; los estilos específicos permanecerán
  junto a sus componentes para evitar una hoja monolítica.
- La navegación se limitará a rutas o estados reales. Un elemento visual que no
  tenga comportamiento no se presentará como una función disponible.

## 4. Decisiones técnicas pendientes de aprobación

Antes de implementar se deberá fijar:

- si los resultados se presentan únicamente como tarjetas o también con vista de
  tabla;
- el nombre definitivo de la herramienta, paleta y tipografía con licencia
  compatible;
- si la navegación lateral se mantiene visible en escritorio o se reduce a una
  cabecera compacta;
- la estrategia de test responsive compatible con la configuración actual de
  Vitest/JSDOM;
- si se necesitan nuevos componentes compartidos o basta con dividir el feature
  de regen.

Estas decisiones no deben alterar el JSON ni añadir dependencias sin una nueva
aprobación.

## 5. Estrategia de pruebas

- Componente de formulario: validación, payload exacto, limpieza y bloqueo
  durante carga.
- Componente de resultados: resumen, campos del jugador, indicadores de
  coincidencia, orden recibido y estado vacío.
- Estados de servicio: éxito, error HTTP/red y reintento conservando filtros.
- Shell: título, navegación activa y landmarks accesibles.
- Accesibilidad: labels, roles, foco y recorrido de teclado en el flujo principal.
- Responsive: comprobaciones de layout o snapshots focalizados en los tres
  anchos definidos, sin convertir los tests en pruebas frágiles de píxeles.
- `npm test` y `npm run build` como validación final del frontend.
