# Cambios a las rutinas de seguimiento de reembolsos

Estado: APLICADO el 02/11/2026.
- Rutina principal (trig_018MKKEyJENKXzoYEDG5xeqb): prompt reemplazado por `prompt_rutina_A.md`; horario y conectores sin cambios.
- Rutina manual (trig_0171AF4dqUKptwX9aS1GdU6q): creada con `prompt_revision_cola.md`, sin horario. PENDIENTE: agregarle los conectores Microsoft 365 y Google Sheets desde la interfaz de rutinas de claude.ai, porque la herramienta no permitió asignarlos al crearla.
- `prompt_rutina_A.md` reemplaza el prompt de la rutina programada existente "Actualizar seguimiento reembolsos" (trig_018MKKEyJENKXzoYEDG5xeqb). Mantiene su horario: 9, 13, 17 y 22 h de París, de lunes a viernes.
- `prompt_revision_cola.md` es una rutina NUEVA, "Revisión manual de cola reembolsos". No tiene horario, solo se lanza a mano, y usa los mismos conectores (Microsoft 365 y Google Sheets).
- Ya aplicado aparte (autorizado): se agregó "Seguimiento interno con David" en `Listas!C17`.

## Decisiones confirmadas por Santiago
1. **Comentarios del equipo (AI).** Son una pista; la verdad es el correo. El comentario dice qué correo buscar. Si el correo muestra la gestión, la etapa avanza según lo que dice el correo. Si no hay gestión visible en el correo, la etapa no cambia y la fila va a "Filas con comentario del equipo y etapa sin cambio" con lo que se encontró (por ejemplo, "solo hay un borrador del 30/10").
2. **La rutina principal abre los correos para lograr confianza Alta.**
   - Abre todos los correos del lote que no sean ruido, también los que tienen plantilla reconocible (la plantilla ya no basta sola).
   - Si la etapa depende de un correo anterior al lote, o la fila estaba con confianza Media o Baja o con AJ≠I, busca el hilo y abre el correo que define la etapa.
   - "Alta" exige haber leído completo ese correo. "Media" solo se usa si, después de abrir, sigue faltando algo, y AK dice qué falta.
3. **La revisión de la cola (antigua Fase B) es una rutina aparte que solo se corre a mano.** La rutina principal ya no revisa casos sin correos nuevos. Solo los lista en el resumen ("Consultar al proveedor", calculado con la planilla, y "N filas para la revisión manual").
4. **AO:** queda vacío si la pelota no está en la casilla. Excepciones: proveedor externo con 7 o más días hábiles sin respuesta, y cliente con 5 o más días hábiles sin responder un pedido de documentos.
5. **N = "Seguimiento interno con David"** cuando el caso está con David.

## Rutina principal: qué cambió respecto al prompt original
1. **Etapas:** tabla fija de evento a etapa. Regla AJ = I: si quedan distintas, AK lleva "AJ≠I: motivo".
2. **Comentarios del equipo:** nuevo Paso 4d. Corre antes de procesar los correos, en todas las corridas y para todas las filas abiertas con comentario, aunque no tengan correos nuevos. Distingue tres tipos de comentario:
   - evento: se confirma con el correo;
   - confirmación ("ok"): no hace nada;
   - duda ("ya pregunté por teams"): va a revisión.
   Además, "No duplicado" evita que se reporte ese par como duplicado.
3. **Sin topes fijos de 60 correos ni 30 aperturas.** El único límite es de tiempo: 40 minutos, cortando al final de un minuto completo.
   - Error 429: como máximo 3 lecturas a la vez y hasta 5 reintentos con espera. Si sigue fallando, la fila no se toca y el lote se corta antes de ese correo para releerlo en la próxima corrida.
4. **Rebotes:** nuevo Paso 4c. Un "No se puede entregar" invalida el envío original. Si era al proveedor, la fila no avanza, N pasa a "Responder / reenviar al proveedor" y AO propone el reenvío.
   - **Borradores:** un correo con isDraft = true nunca cuenta como envío.
5. **Búsqueda:** siempre sin order, paginando todo, y además una búsqueda aparte en "Sent Items".
6. **David y el equipo interno:**
   - Todo @grupomok.com es interno. David es evaluador interno.
   - El "destino de evaluación" es WMC, BTS/TW o David, lo que corrige la contradicción del prompt original.
   - Los correos de David no cuentan para P, Q ni V.
   - AO nunca va a David ni a nadie @grupomok.com. Por eso el caso del equipo de Perú queda con AO vacío y una nota en AK.
   - X = "Otro" cuando el envío fue a David. X también se puede escribir en el Paso 5.
7. **Calidad de datos:**
   - El id de correo se valida con una expresión regular antes de armar AM.
   - Todas las fechas en 'Casos' van en hora de Chile.
   - AK lleva como máximo un "| Antes:" y un solo prefijo de cada tipo.
   - Las filas "[Rev dd/mm]" solo bajan con un correo nuevo.
   - Nuevo Paso 6c de duplicados (solo reporte).
   - Y (ticket) se puede completar en el Paso 4 si está vacía.
8. **Verificación:**
   - Diff automático contra la copia del inicio.
   - Ya NO restaura ediciones del equipo hechas durante la corrida. Antes de escribir, relee la fila y respeta los cambios del equipo.
   - Comprobaciones: AJ≠I sin nota, AO sin destinatario interno, AM con id válido, AK con un solo "| Antes:", máximo 330 caracteres y sin UTC.
9. **Resumen:**
   - El encabezado muestra la confianza de las filas tocadas.
   - Nueva sección "💬 Filas con comentario del equipo y etapa sin cambio".
   - "Avanzaron de etapa" indica qué evidencia se usó.
   - Los rebotes van a "Requieren acción hoy".
   - "Consultar al proveedor" se calcula con la planilla.

## Rutina manual de revisión de la cola: qué hace
- Arma la cola de casos abiertos no revisados en los últimos 2 días hábiles. Siempre incluye los que tienen AJ≠I sin nota o confianza Media o Baja.
- Prioridad: reclamos formales, luego casos con tarea de MOK pendiente, luego el resto.
- Lotes de unos 9 casos, con 2 o 3 subagentes de solo lectura a la vez. Los subagentes abren el correo que define la etapa, tratan el comentario de AI como pista con el correo como verdad, y devuelven JSON. Solo el agente principal escribe, lote por lote.
- Escribe solo I, J, N, X, Y, AF, AH y AJ a AO en filas existentes, y AR solo por "Borrador desactualizado". No crea filas ni escribe en 'Control rutina'.
- Límite de 50 minutos. Lo que no alcanza queda primero en la próxima corrida manual.
- Diff de verificación sin restaurar ediciones de otros, y resumen propio en el chat.
- Comparte con la rutina principal la tabla de evento a etapa, las reglas de AO, los rebotes, las reglas de etapa y la escritura (texto copiado, porque cada rutina tiene que ser autónoma).

## Reglas que quedaron intactas
- La casilla es SOLO LECTURA, en ambas rutinas y en los subagentes.
- Ningún mensaje por ningún canal. El resumen va solo al chat de la sesión.
- Columnas permitidas: nunca F, G, H, M, AE ni AI. B, C, D y E solo si están vacías. K, L, R, T, U, AP y AQ son fórmulas. AS es de la rutina de borradores. No se tocan otras pestañas, formatos ni validaciones, ni se borran filas.
- Ante un error de encabezados o de conector: no escribir y registrar "Error: …" sin mover el punto de avance.
- Validación exacta de encabezados A..AO, punto de avance incremental, margen de −5 minutos e "IDs en el borde".
- Paso 2b de borradores (los cuatro valores de AR, el tope de 40 y la clasificación de ediciones). Paso 3 de asociación. Paso 4b de identificación.
- Reglas de V, W, P y Q (con la exclusión de internos y borradores). Fórmula del hipervínculo de AM.
- Formato, estilo y lecciones de AO. "no borrador" o "redacción manual" bloquea AO. "Borrador desactualizado".
- Paso 5: cierres, reapertura sin reabrir, orden de avance sin retroceso y duplicados SIN-ID sin cerrar.
- Paso 6 de casos nuevos. Escritura con null = no tocar y AR como celda individual.
- Formato del resumen, máximo 10 ítems por sección, link a la planilla, "Sin novedades" y protección de datos personales.

## Puntos a tener en cuenta
- Abrir todos los correos hace la rutina principal más lenta. Con mucho volumen cortará por tiempo a los 40 minutos y seguirá en la próxima corrida.
- El seguimiento al proveedor de casos sin correos nuevos ya no es automático. Depende de lanzar la rutina manual.
- Largo de los prompts: la rutina principal tiene unos 49 mil caracteres y la manual unos 34 mil.
