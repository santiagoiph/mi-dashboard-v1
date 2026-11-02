# Cambios al prompt de "Actualizar seguimiento reembolsos" (trig_018MKKEyJENKXzoYEDG5xeqb)

Estado: PROPUESTA, todavía no aplicada a la rutina. Prompt completo en `prompt_corregido.md`.
Ya hecho aparte (autorizado): se agregó "Seguimiento interno con David" en `Listas!C17`, dentro de la validación de N (`Listas!C2:C40`).

## Decisiones confirmadas
- La "rutina B" va DENTRO de la misma rutina, como Fase B, después de la Fase A. No se crea otra rutina programada y el horario no cambia.
- La Fase B revisa TODOS los casos abiertos con la cola de prioridad, no solo "Analizando el proveedor".
- AO queda vacío cuando la pelota no está en la casilla, con dos excepciones: proveedor externo con 7 o más días hábiles sin respuesta, y cliente con 5 o más días hábiles sin responder un pedido de documentos.

## Ajuste 2 (pedido de Fabiana): los comentarios del equipo avanzan la etapa
- El Paso 4d corre al inicio de la Fase A, antes de procesar los correos. Así, "Respuesta recomendada enviada" se interpreta con el AO que Fabiana vio y envió.
- **Cambia la regla anterior.** Un comentario de evento basta por sí solo para avanzar la etapa. El correo en "Elementos enviados" ya no es un requisito: si aparece, la confianza queda "Alta" y J toma su fecha; si no aparece, la etapa avanza igual con confianza "Media" y queda marcada como "(por comentario, sin correo)" en el resumen. La etapa solo NO avanza si el correo contradice el comentario (es un borrador, rebotó o es de otro caso) o si el comentario es una duda.
- "Respuesta recomendada enviada" se traduce en una etapa según lo que decía AO: pedido de documentos → Documentos solicitados; expediente al proveedor → Analizando el proveedor; aprobación comunicada → Resultado comunicado; rechazo comunicado → cierre. Regla mínima: si la fila estaba en "Sin gestionar" y el equipo respondió, pasa como mínimo a "Documentos solicitados".
- Se reconocen más frases: "respondí", "contesté", "gestionado", "comuniqué el resultado", "pagado".
- Si hay más de 9 filas con comentario, las búsquedas se hacen con subagentes, igual que en la Fase B.

## Ajuste 3: la rutina ya no deshace ediciones del equipo
- El paso de verificación ya no restaura "diferencias no planificadas", porque podían ser comentarios o etapas que el equipo escribió mientras corría la rutina. Solo restaura una celda que la propia rutina escribió por error (por ejemplo, en una fila equivocada).
- Antes de escribir, la rutina relee la fila. Si el equipo cambió una celda durante la corrida, la rutina respeta ese valor y no la sobrescribe.

## Qué cambió

### 1. Avance de etapa con evidencia
- Nueva sección "Tabla fija de evento a etapa": un evento, una etapa.
- Nueva definición de "evidencia suficiente": (a) correo leído completo, (b) envío de la casilla con plantilla reconocible ("Se envía documentación recibida el día…", "FORMULARIO REEMBOLSO MOK", etc.), sin necesidad de abrirlo, o (c) comentario del equipo que coincide con "Elementos enviados".
- "Alta" ya no exige abrir el correo: basta la evidencia (a), (b) o (c).
- Nueva regla AJ = I: si quedan distintas, AK debe llevar "AJ≠I: <motivo>". El Paso 5 avanza I siempre que la evidencia sea suficiente.

### 2. Comentarios del equipo (AI)
- Nuevo Paso 4d. Corre en todas las corridas para las filas abiertas con AI, aunque no tengan correos nuevos. Clasifica el comentario como evento ("Enviado a proveedor", "Le pedí formulario", "Respuesta recomendada enviada", "Aprobado…"), confirmación ("[Barrida] ok") o duda ("ya pregunté por teams", "no veo…").
- Un comentario de evento se cruza con "Elementos enviados". Si coincide, la etapa avanza y AK queda "[Equipo dd/mm] …". Si no coincide, o el comentario es una duda, la fila va a la nueva sección del resumen "Filas con comentario del equipo y etapa sin cambio" y la etapa no cambia.
- Si AI dice "No duplicado…", ese par no se reporta como duplicado.
- AI sigue siendo de solo lectura. El Paso 7 comprueba que no cambió.

### 3. Topes, cola y subagentes
- Se eliminan los topes de 60 correos, 30 aperturas y 15 filas del 4c, y el de "10 filas con AO vacío".
- La Fase A procesa todos los correos de la ventana, con un corte suave a los 30 minutos que nunca corta en medio de un minuto.
- La Fase B (nuevo Paso 6b, reemplaza al 4c) arma la cola de casos abiertos: (1) reclamos formales, (2) casos con tarea de MOK pendiente o AJ≠I sin nota, (3) el resto. Se procesa en lotes de unos 9 casos, con 2 o 3 subagentes de solo lectura a la vez. Los subagentes llevan una instrucción fija y devuelven JSON. El agente principal es el único que escribe, y escribe después de cada lote.
- Si la herramienta de subagentes no está disponible, el agente principal procesa los lotes uno por uno.
- Error 429: como máximo 3 lecturas simultáneas, con espera según Retry-After o 2, 4, 8, 16 y 32 s, hasta 5 reintentos. Si sigue fallando, el caso queda "no revisado (429)" sin cambios y no baja la confianza. Ese caso entra primero en la cola de la próxima corrida.
- Único límite: 50 minutos de corrida. Lo que no alcanza queda primero en la cola siguiente.
- 'Control rutina' sin columnas nuevas: el Estado agrega "; Fase B: N revisados, N en cola, N por 429".

### 4. Rebotes y borradores
- Nuevo Paso 4c, de rebotes. Un "No se puede entregar"/"Undeliverable" de postmaster@ o de Microsoft Outlook invalida el envío original. Si el envío era al proveedor, la fila no avanza, N pasa a "Responder / reenviar al proveedor" y AO propone el reenvío. Si era al cliente, la fila va a "Para revisar".
- Antes los rebotes se descartaban como ruido. Ahora no.
- isDraft = true nunca cuenta como envío, ni para W ni para la etapa. Ejemplo citado: el "Seguimiento de casos pendientes" a WMC del 30/10.

### 5. Búsqueda
- Nueva sección "Lecturas de correo": buscar siempre sin order, paginando todo, y además una búsqueda aparte con folderName="Sent Items". Se aplica en la Fase A, el Paso 2b, el Paso 4d y la Fase B.
- El 4c anterior limitaba la búsqueda a 2 páginas. Ese límite se elimina.

### 6. David Berríos y el equipo interno
- Nueva sección "Personas y dominios": David es evaluador interno y todo @grupomok.com es interno.
- Un correo de David no cuenta para V, P ni Q.
- Se corrige la contradicción del texto anterior: ahora el "destino de evaluación" es WMC, BTS/TW o David, y un caso solo es "sin envío" si no hubo envío a ninguno de los tres.
- Si el caso está con David: etapa "Analizando el proveedor", X = "Otro", N = "Seguimiento interno con David". AO va al cliente solo si este espera respuesta; si no, AO queda vacío con una nota en AK.
- Regla de destinatario prohibido: AO nunca va dirigido a David ni a nadie @grupomok.com. Hay una lección (8) nueva en el estilo, y el Paso 7 lo comprueba.
- Efecto colateral: el caso "aprobación autorizada al equipo de Perú" ya no genera AO a ese equipo interno. Queda AO vacío con una nota en AK. Lo mismo para "Sin información suficiente" cuando lo derivó alguien de @grupomok.com.
- X se puede escribir también en el Paso 5, al pasar a "Analizando el proveedor", con la misma regla que antes tenía solo el 4c.

### 7. Calidad de datos
- El id de correo se valida con `^AA[A-Za-z0-9_-]{100,250}={0,2}$` antes de armar AM o de llamar a read_resource. Si el id no es válido, AM no se toca y la fila va a "Para revisar".
- Todas las fechas y horas de 'Casos' y del resumen van en hora de Chile. 'Control rutina' sigue en UTC, como dicen sus encabezados.
- Nueva sección "Formato de AK": como máximo un "| Antes:", sin "Antes" si el detalle anterior es del mismo día, y un solo prefijo de cada tipo ([Rev], [Equipo], [Prov]).
- "[Rev dd/mm]": un 429, una búsqueda incompleta o un resumen ambiguo no justifican bajar la confianza. Solo la baja un correo nuevo posterior a la fecha del [Rev], y el prefijo se conserva.
- Nuevo Paso 6c, de duplicados (solo reporte): agrupa filas por n° de caso, correo, RUT o nombres normalizados con tokens en común. Incluye los ejemplos citados.
- Regla de pelota para AO: no hay recordatorios si la pelota no está en la casilla, salvo las dos excepciones de arriba.

### 8. Verificación
- Diff automático en python contra `inicio.json` (copia completa del Paso 1).
- Comprobaciones nuevas: AJ≠I sin nota (se corrige si la fila se tocó en la corrida; si no, se reporta y entra con prioridad a la cola), AI sin cambios, AO sin destinatario interno, AM con id válido, y AK con un solo "| Antes:", máximo 330 caracteres y sin UTC.

### Resumen final
- Cifras de la Fase B en el encabezado.
- Nueva sección 8, "💬 Filas con comentario del equipo y etapa sin cambio".
- "Avanzaron de etapa" indica qué evidencia se usó.
- "Consultar al proveedor" agrega los casos con David.
- Los rebotes van a "Requieren acción hoy".

## Reglas que quedaron intactas
- Casilla SOLO LECTURA (sin enviar, responder, reenviar, mover, borrar, marcar ni categorizar; sin crear, editar ni borrar borradores). Se extiende de forma explícita a los subagentes.
- Ningún mensaje por ningún canal. El resumen va solo al chat de la sesión.
- Columnas permitidas: las mismas. Nunca F, G, H, M, AE ni AI. B, C, D y E solo si están vacías. K, L, R, T, U, AP y AQ son fórmulas. AS es de la rutina de borradores. No se tocan otras pestañas, formatos ni validaciones, ni se borran filas.
- Ante un error de encabezados o de conector: no escribir y registrar "Error: …" sin mover el punto de avance.
- Validación exacta de encabezados A..AO.
- Punto de avance incremental, margen de −5 minutos e "IDs en el borde".
- Paso 2b de borradores: los cuatro valores de AR, el tope de 40 por corrida y la clasificación sin cambios / editado leve / editado fuerte.
- Asociación de correos a casos (Paso 3), con el agregado de rebotes e internos.
- Paso 4b (B, C, D, E vacíos) y su lista de dominios excluidos.
- Reglas de V, W, P y Q (con la exclusión de internos y borradores).
- Fórmula y base del hipervínculo de AM.
- Formato, estilo y lecciones (1) a (7) de AO. "no borrador" o "redacción manual" bloquea AO. "Borrador desactualizado" pasa AR a Obsoleto.
- Paso 5: cierres por pago y rechazo, reapertura sin reabrir, orden de avance sin retroceso (con la única excepción de 3 a 2) y duplicados SIN-ID sin cerrar.
- Paso 6 de casos nuevos (con "Otro" en X si el envío fue a David).
- Escritura con update_values, null = no tocar, AR como celda individual y relectura de la columna A antes de escribir.
- Formato del resumen, máximo 10 ítems por sección, link a la planilla, "Sin novedades" y protección de datos personales.

## Puntos a tener en cuenta
- El prompt pasa de unos 25 mil a unos 52 mil caracteres. Si la rutina tiene un límite de largo, habrá que recortar.
- La duración de la corrida puede crecer: la última tardó 16 minutos. El corte de 50 minutos lo acota.
- Se asume que los subagentes heredan los conectores de Microsoft 365 de la rutina. Si no los heredan, se usa el modo secuencial previsto.
