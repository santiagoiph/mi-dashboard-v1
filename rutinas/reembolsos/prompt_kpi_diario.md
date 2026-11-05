Reporte diario de KPI del área de reembolsos de Grupo MOK (casilla reembolsos.europ@grupomok.com). Reemplaza al antiguo triage diario. Trabaja en español. Esta tarea LEE la planilla y el resumen ya calculado, y de la casilla lee SOLO el conteo de correos sin leer de la Bandeja de entrada; no abre correos ni cambia casos.

## Reglas
- Solo puedes escribir en la pestaña 'KPI diario' (una fila por día, Paso 3). No toques ninguna otra pestaña, fórmula, formato ni gráfico.
- No envíes mensajes por Teams, correo ni ningún otro canal. El reporte va SOLO en tu respuesta final (llega como notificación).
- Lectura de correos: de la casilla reembolsos.europ@grupomok.com solo puedes obtener el CONTEO de correos sin leer de la Bandeja de entrada (Paso 1). No abras ni leas el contenido de ningún correo (no uses read_resource), no uses asuntos, remitentes ni resúmenes para nada, no los copies en ninguna parte, no marques nada como leído o no leído, no muevas, borres ni categorices correos, y no cambies ningún caso.
- No incluyas RUT, correos, montos ni datos bancarios de clientes; de los casos, solo ID y nombre.
- Si algo no calza (pestaña o encabezado distinto, conector de Google Sheets no disponible), no escribas nada y termina con un resumen del problema. Si lo único que falla es el conteo de correos sin leer, NO detengas la rutina: sigue el Paso 1b.

## Recursos
- Planilla Google Sheets id 1tdVTrz3EghENSIAF12iz0Wnjw3blTwWbTY4h2JsHWkY (conector Google Sheets; carga con ToolSearch "+google sheets"). Pestañas: 'Reportería' (todo calculado con fórmulas sobre 'Casos'), 'Casos', 'Control rutina', 'KPI diario'. Configuración regional es_CL.
- Correo (conector Microsoft 365; carga con ToolSearch "select:mcp__Microsoft_365__outlook_email_search"): solo para el conteo del Paso 1.
- Hora de referencia: Chile (America/Santiago). Hoy = fecha de Chile al correr.

## Paso 1: leer los datos
- 'Reportería'!A1:L220 (valores). Del bloque "Resumen general" toma: Casos totales, Abiertos, Cerrados (pagado/resuelto), Sin gestionar, Esperando nuestra respuesta, Esperando más que la alerta, Abiertos fuera de plazo, % de abiertos fuera de plazo, Reclamos formales abiertos, Prom. días hábiles esperando respuesta, Prom. días hábiles desde la solicitud (abiertos). De "Calidad de datos": Sin responsable asignado, Sin correo de cliente, Sin n° de caso. De la tabla "Por etapa": casos, esperando y fuera de plazo de cada etapa. De la tabla "Casos nuevos y cerrados por semana": las últimas 4 semanas. Toma también los parámetros (plazo comprometido y alerta de respuesta) y la fecha de corte. Ubica cada dato por su etiqueta, no por la posición de la celda; si una etiqueta no está, detente.
- 'KPI diario'!A1:W (fila 1 = encabezados; Fecha en formato dd/mm/aaaa).
- 'Control rutina'!A1:F (solo para "Correos procesados" del Paso 2). La columna "Pendientes" de 'Control rutina' es la cola interna de la rutina de correos: NO es el número de correos sin abrir y NUNCA se usa para la columna W.
- 'Casos'!A1:AO (procésalo con python -I si es grande); necesitas S (Fecha solicitud), V (Último mensaje recibido), W (Última respuesta nuestra), I (Etapa), H (Reclamo formal), P (¿Esperando nuestra respuesta?), R (Días hábiles esperando), T (Días hábiles desde solicitud), A (ID) y C (Cliente).
- Correos sin abrir (columna W de 'KPI diario'): cuenta los correos sin leer de la Bandeja de entrada de la casilla compartida.
  1. Llama a outlook_email_search con mailboxOwnerEmail = "reembolsos.europ@grupomok.com", folderName = "Inbox", query = "isread:false", limit = 25, sin sender, recipient, fechas ni order.
  2. Pagina hasta el final: si el último ítem trae nextCursor, vuelve a llamar solo con cursor = ese valor; si trae nextOffset, repite la llamada del punto 1 con offset = ese valor. Termina cuando no haya moreResults.
  3. Guarda SOLO el id y el campo isRead de cada resultado (descarta todo lo demás sin mirarlo). Deduplica por id. El conteo es el número de ids distintos con isRead = false.
  4. El conteo es VÁLIDO solo si: todas las páginas respondieron (ante un 429 o error temporal, espera 10 s, 30 s y 60 s y reintenta hasta 3 veces por página); todos los resultados traen isRead = false (si aparece alguno con isRead = true, el filtro no se aplicó y el conteo no sirve); y el total es menor que 1000 (con 1000 o más la búsqueda puede venir truncada).
  5. No uses read_resource sobre "mail:///folders/..." para este dato: ignora el buzón compartido y devuelve el buzón personal de quien creó la rutina.

## Paso 1b: si el conteo de correos sin abrir falla
No inventes el dato ni lo estimes, y no uses 'Control rutina'. Deja W vacía en la fila de hoy (Paso 3), escribe en el reporte la línea "Correos sin abrir: no disponible hoy" con el motivo en pocas palabras, y omite las comparaciones de W (Paso 4). Si además la fila anterior de 'KPI diario' (con fecha 06/11/2026 o posterior) también tiene W vacía, es una falla repetida: empieza la respuesta final con "⚠️ ALERTA: el conteo de correos sin abrir falló dos días seguidos; la columna W de 'KPI diario' debe llenarse a mano hasta revisar la conexión con Outlook."

## Paso 2: definir el período
El período va desde el día siguiente a la fecha de la última fila de 'KPI diario' anterior a hoy hasta ayer, ambos inclusive (un lunes cubre viernes, sábado y domingo). Si no hay fila anterior, el período es ayer. Calcula para el período:
- Casos nuevos = Casos totales de hoy − Casos totales de la fila anterior (si no hay fila anterior, filas de 'Casos' con Fecha solicitud dentro del período).
- Cerrados = Cerrados (total) de hoy − Cerrados (total) de la fila anterior (mínimo 0; si es negativo, alguien reabrió casos: anótalo).
- Respuestas enviadas = filas de 'Casos' con W (Última respuesta nuestra) dentro del período.
- Mensajes de clientes recibidos = filas con V dentro del período.
- Correos procesados = suma de "Correos procesados" (columna E) de 'Control rutina' en filas cuyo "Inicio corrida" (columna A) cae dentro del período (en hora de Chile).

## Paso 3: guardar la foto del día en 'KPI diario'
Una fila por fecha. Si ya existe una fila con la fecha de hoy, reemplázala; si no, agrégala en la fila siguiente a la última fila con valor en A (sin dejar filas vacías entre medio). La fila tiene 23 columnas, A..W, en este orden: Fecha (hoy, dd/mm/aaaa) | Casos totales | Casos nuevos (período) | Cerrados (período) | Respuestas enviadas (período) | Correos procesados (período) | Abiertos | Sin gestionar | Documentos solicitados | Analizando el proveedor | Resultado recibido, falta comunicar | Resultado comunicado, falta pagar | Sin información suficiente | Cerrados (total) | Esperando nuestra respuesta | Esperando más que la alerta | Fuera de plazo | % fuera de plazo (como número entre 0 y 1) | Reclamos formales abiertos | Prom. días hábiles esperando | Prom. días hábiles desde solicitud (abiertos) | Sin responsable | Correos pendientes (sin abrir).
- La columna W "Correos pendientes (sin abrir)" lleva el conteo válido del Paso 1, como número; si el conteo no es válido, va vacía ("").
- Antes de escribir, verifica que la fila 1 tenga exactamente esos 23 encabezados en A..W, en ese orden (el de W es exactamente "Correos pendientes (sin abrir)"). Si no calza, no escribas nada y detente. Nunca escribas en la fila 1.
- Escribe con update_values solo el rango 'KPI diario'!A<fila>:W<fila> de la fila de hoy. Después relee 'KPI diario'!A1:W y confirma que la fila 1 no cambió, que la fila de hoy quedó en la fila esperada (inmediatamente después de la última fila con fecha anterior, o reemplazando la de hoy) y que las filas anteriores no cambiaron.

## Paso 4: comparar
Para cada indicador de estado (abiertos, sin gestionar, esperando respuesta, fuera de plazo, % fuera de plazo, reclamos, promedios y correos sin abrir) calcula la variación contra la fila anterior y contra la fila de hace 7 días o la más cercana anterior (si no hay, omite esa comparación). Usa ▲ y ▼ con el número; marca con ✅ las mejoras y con ⚠️ los empeoramientos: para estos indicadores, bajar es mejor (▼ ✅, ▲ ⚠️). Para los correos sin abrir (W): si la fila de comparación no tiene valor en W, omite esa comparación (las filas anteriores al 05/11/2026 no lo tienen); si hoy no hay conteo válido, omite las dos. Para nuevos, cerrados y respuestas enviadas, compara contra el promedio de los últimos 5 períodos disponibles.

## Respuesta final (es el reporte)
Termina con el reporte en texto markdown, legible en menos de 2 minutos, sin guiones largos, en este orden:
1. Si corresponde, la línea "⚠️ ALERTA: …" del Paso 1b.
2. Título en negrita: "Reporte diario de reembolsos – dd/mm/aaaa" y el período cubierto.
3. Una línea de lectura: la conclusión más importante del día en una frase (por ejemplo, si el backlog sube o baja y por qué).
4. "Movimiento del período": casos nuevos, cerrados, respuestas enviadas, mensajes de clientes recibidos, correos procesados por la rutina; cada uno con su comparación contra el promedio.
5. "Estado actual": abiertos, sin gestionar, esperando nuestra respuesta (y cuántos sobre la alerta), fuera de plazo (n° y %), reclamos formales abiertos, prom. días hábiles esperando, prom. días hábiles desde la solicitud, y "Correos sin abrir: N" (o "Correos sin abrir: no disponible hoy" con el motivo); con variación vs ayer y vs hace 7 días.
6. "Embudo por etapa": etapa | casos | esperando | fuera de plazo, en el orden del proceso.
7. "Tendencia semanal": las últimas 4 semanas de nuevos vs cerrados, en una línea por semana.
8. "Para atender hoy": los 5 reclamos formales abiertos más antiguos y los 5 casos con más días hábiles esperando nuestra respuesta (ID, cliente, etapa, días). Toma las listas de 'Reportería'.
9. "Calidad de datos": sin responsable, sin correo de cliente, sin n° de caso, en una línea.
10. Una línea final: si se escribió la fila de 'KPI diario' (n° de fila) y si W quedó con conteo o vacía.
11. Links: Reportería https://docs.google.com/spreadsheets/d/1tdVTrz3EghENSIAF12iz0Wnjw3blTwWbTY4h2JsHWkY/edit#gid=900 y KPI diario (gráficos de tendencia) https://docs.google.com/spreadsheets/d/1tdVTrz3EghENSIAF12iz0Wnjw3blTwWbTY4h2JsHWkY/edit#gid=746324557.
