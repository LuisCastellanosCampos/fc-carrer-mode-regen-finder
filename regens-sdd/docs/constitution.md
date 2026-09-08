 # Constitución del proyecto

Principios innegociables. Toda spec, plan y tarea debe cumplirlos.

1. **Stack simple:** Solo Python/FastAPI, Angular y las dependencias imprescindibles.
2. **Spec como contrato:** Todo cambio de código debe corresponder a una spec aprobada y trazable.
3. **Arquitectura hexagonal:** El dominio y sus puertos no dependerán de FastAPI, Angular ni de la persistencia.
4. **Lógica separada:** Las reglas de negocio estarán aisladas de la interfaz y se podrán probar sin ella.
5. **Tests obligatorios:** Cada requisito tendrá tests automatizados; ningún cambio se considerará terminado con fallos.
6. **Idioma**: El acceso a datos usará adaptadores reemplazables y código e identificadores en inglés; mensajes al usuario y
   documentación en español.
