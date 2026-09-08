# AGENTS.md — <fc-carrer-mode-regen-finderto>

## Proyecto
Qué es: FC Career Mode Regen Finder es una aplicación web diseñada para ayudar a los jugadores a identificar regens (reencarnaciones de jugadores retirados) ocultos en el Modo Carrera de EA FC. Cruzando fechas de nacimiento exactas y nacionalidades, permite localizar con precisión a las futuras estrellas mundiales.

Arquitectura y tecnologías: Desarrollado bajo una estructura de Monorepo, cuenta con un backend de alto rendimiento basado en arquitectura hexagonal en Python (FastAPI) que expone una API REST limpia, y un frontend robusto y reactivo construido con Angular.

## Comandos
- Ejecutar: `uvicorn main:app --reload (Backend) / ng serve (Frontend)`
- Tests: `pytest (Backend) / ng test (Frontend)`

## Estilo y convenciones
- Python 3.12+, type hints en todas las funciones públicas para el backend y TypeScript / JavaScript ES6+ para el frontend.
- Solo biblioteca estándar (pytest únicamente para tests).
- Identificadores en inglés; mensajes de usuario en español.

## Reglas
- Lee `docs/constitution.md` y la spec activa en `specs/` antes de tocar código.
- No añadas dependencias ni cambies el formato del JSON sin actualizar antes la spec.
- No modifiques archivos dentro de `specs/` salvo petición explícita.

## Al terminar cualquier tarea
- Ejecuta `pytest -q` y `ng test` y confirma en tu respuesta que todo pasa.