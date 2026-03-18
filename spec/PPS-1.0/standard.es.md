---
title: Prompt Protocol Specification (PPS) v1.0 — Especificación Normativa (Español)
status: community-specification
version: 1.0.0
lang: es
---

**Language / 语言 / 言語 / 언어 / Idioma**：[中文](standard.md) · [English](standard.en.md) · [日本語](standard.ja.md) · [한국어](standard.ko.md) · [Español](standard.es.md)

---

## Tabla de Contenidos

| Sección | Contenido |
|---------|-----------|
| [§1](#1-alcance) | Alcance |
| [§2](#2-términos) | Términos |
| [§3](#3-modelo-de-datos-esquema-normativo) | Modelo de Datos (8 Dimensiones) |
| [§4](#4-cabecera-requerida) | Cabecera |
| [§5](#5-cuerpo-requerido) | Cuerpo |
| [§6](#6-integridad-requerida) | Integridad |
| [§7](#7-determinismo--reproducción) | Determinismo & Reproducción |
| [§8](#8-seguridad--cumplimiento) | Seguridad & Cumplimiento |
| [§9](#9-conformidad) | Conformidad |
| [§10](#10-versionado) | Versionado |
| [§11](#11-perfil-de-interoperabilidad) | Perfil de Interoperabilidad |
| [§12](#12-implementación-de-referencia-informativo) | Implementación de Referencia |
| [Anexo A](#anexo-a-informativo-vocabulario-de-restricciones-controlado) | Vocabulario de Restricciones |
| [Anexo B](#anexo-b-informativo-perfil-de-contenido-pps--umbrales-de-rigurosidad) | Umbrales de Conformidad |
| [Anexo C](#anexo-c-informativo-ejemplo-mínimo-interoperable) | Ejemplo Mínimo |
| [Anexo D](#anexo-d-informativo-listas-de-verificación-de-validación) | Listas de Verificación |
| [Anexo E](#anexo-e-informativo-especificación-de-vinculación-opcional-pps-qr) | Vinculación PPS-QR |

---

# 1. Alcance

Esta especificación define la implementación mínima interoperable de PPS (Especificación del Protocolo de Prompts), un protocolo de instrucciones para la interacción humano-IA. Los requisitos normativos se expresan usando MUST / SHOULD / MAY (según RFC 2119) y llevan identificadores REQ.

# 2. Términos

- **Envoltorio**: El portador del protocolo para una única interacción, compuesto por `header`, `body` e `integrity`.
- **Canonicalización**: Ordenamiento y serialización deterministas de JSON para producir un hash estable.
- **Decodificación Determinista**: Parámetros de decodificación fijos que permiten la reproducción reproducible.

# 3. Modelo de Datos (Esquema Normativo)

Los implementadores MUST aceptar y producir Envoltorios que se ajusten a `schema/pps-1.0.schema.json` (REQ-001).

## 3.1 Ocho Dimensiones y Rutas JSON (Mapeo Normativo)

- **REQ-100 (What/Qué)**: MUST proporcionar `body.what.task`; si la salida es JSON estructurado, SHOULD proporcionar `body.what.output_schema`.
  - Ruta JSON: `/body/what/{task, input_schema?, output_schema?}`

- **REQ-110 (Why/Por qué)**: SHOULD listar `body.why.goals`; las restricciones SHOULD provenir del vocabulario controlado (Anexo A), p. ej. `no_external_browse`, `citations_required`, `use_provided_evidence`.
  - Ruta JSON: `/body/why/{goals?, constraints?}`

- **REQ-120 (Who/Quién)**: SHOULD especificar `persona`; si se usarán herramientas, MUST incluirlas en la lista blanca de `who.capabilities`.
  - Ruta JSON: `/body/who/{persona?, capabilities?, policy?}`

- **REQ-130 (When/Cuándo)**: MUST proporcionar al menos uno de `timeframe` o `validity_window`.
  - Ruta JSON: `/body/when/{timeframe?, validity_window?, staleness_policy?}`

- **REQ-140 (Where/Dónde)**: Si `citations_required=true`, MUST proporcionar al menos una entrada de `evidence`; la evidencia SHOULD incluir `digest` y `title`.
  - Ruta JSON: `/body/where/{environment?, evidence[], jurisdiction?, citations_required?}`

- **REQ-150 (How-to-do/Cómo hacerlo)**: SHOULD especificar `paradigm` y `steps`; cualquier `tools` usado MUST satisfacer REQ-181 (restricción de capacidad).
  - Ruta JSON: `/body/how_to_do/{paradigm?, steps?, tools?}`

- **REQ-160 (How-much/Cuánto)**: SHOULD especificar elementos cuantitativos dirigidos al *contenido generado mismo* (p. ej. longitud, estructura, densidad de detalle, orientación de calidad, profundidad cultural). Los nombres de campo son un conjunto abierto; se permiten claves y unidades específicas del dominio.
  - Ruta JSON: `/body/how_much/{content_length?, structure_elements?, detail_richness?, quality_guidance?, cultural_depth?}`

- **REQ-161 (How-much como contenedor de cuantificación unificado)**: Esta especificación no distingue entre *how much* y *how many* como dimensiones separadas. Todas las cuantificaciones relacionadas con cantidad y recursos se consolidan en `how_much`. Las implementaciones MUST normalizar los campos sinónimos (p. ej. `how_many`) mapeándolos a `how_much`.

- **REQ-170 (How-feel/Cómo sentirlo)**: SHOULD especificar `tone` y `style`; si se dirige a una audiencia específica, `audience_level` MUST tomarse de la enumeración.
  - Ruta JSON: `/body/how_feel/{tone?, style?, audience_level?}`

- **REQ-175 (Interfaz / Gobernanza)**: Si la interfaz de salida es JSON, el esquema MUST aparecer en al menos uno de `what.output_schema` o `how_interface.schema`.

## 3.2 Especificación Parcial y Autocompletado

- **REQ-340**: `what.task` es la entrada mínima que el usuario MUST proporcionar.
- **REQ-341**: Las siete dimensiones restantes MAY omitirse o parcialmente omitirse; las implementaciones las completan usando políticas predeterminadas, resultados de recuperación o inferencia.
- **REQ-342**: Cuando ocurre el autocompletado, el sistema MUST registrar los campos completados o sobreescritos en `header.implementation.filled_fields` (como un array de JSON Pointer).
- **REQ-343**: El autocompletado MUST NOT violar las restricciones de gobernanza.

---

# 4. Cabecera (Requerida)

- **REQ-010**: MUST incluir `pps_version` en la forma `PPS-vMAJOR.MINOR.PATCH`.
- **REQ-011**: MUST especificar `model.name`, `model.digest` y `model.data_cutoff`.
- **REQ-012**: MUST especificar `decode.seed`, `decode.temperature` y `decode.top_p`; usar `temperature=0` y `top_p=1` para reproducción determinista.
- **REQ-013**: MUST especificar `locale`; `header.created_at` SHOULD registrar el timestamp de creación.

---

# 5. Cuerpo (Requerido)

- **REQ-020**: MUST contener las ocho dimensiones planas: `what`, `why`, `who`, `when`, `where`, `how_to_do`, `how_much`, `how_feel`.
- **REQ-021**: `how_to_do`, `how_much` y `how_feel` son campos hermanos; las herramientas solo están disponibles cuando se declara la capacidad correspondiente.
- **REQ-022**: Si `where.citations_required=true`, MUST proporcionar al menos una entrada de `evidence` (URI + digest o title).

---

# 6. Integridad (Requerida)

- **REQ-030**: MUST completar `integrity.canonical_hash`; su valor se calcula serializando canónicamente el Envoltorio, aplicando SHA-256 y prefijando con `sha256:`.

---

# 7. Determinismo & Reproducción

- **REQ-040**: MUST fijar `model.digest` y los parámetros `decode` de la Cabecera al reproducir.
- **REQ-041**: SHOULD especificar `stop` para obtener truncado estable.

## 7.1 Reproducibilidad

- **REQ-300**: Un Envoltorio MUST ser canonicalizable; cualquier cambio en `body`, `header` o `integrity` cambia el hash.
- **REQ-301**: Reproducibilidad de evidencia: cuando `where.evidence[].uri` apunta a un recurso mutable, SHOULD proporcionar también campos de instantánea `digest` y `title`.
- **REQ-302**: Reproducibilidad de decodificación: `decode.seed`, `temperature` y `top_p` MUST estar fijos (ver REQ-012).
- **REQ-303**: Reproducibilidad del modelo: `model.digest` MUST identificar una versión específica.
- **REQ-304**: Los implementadores MUST documentar los pasos de reproducción: canonicalizar → validar → verificar política → decodificación determinista.

## 7.2 Estabilidad del Hash

- **REQ-305**: Múltiples canonicalizaciones del mismo Envoltorio MUST producir el mismo `canonical_hash` (idempotencia).
- **REQ-306**: Cuando cambia el algoritmo de canonicalización, `pps_version` MUST incrementarse (MAJOR o MINOR).

## 7.3 Algoritmo de Canonicalización

Para garantizar la consistencia entre plataformas, las implementaciones SHOULD adoptar una implementación mínima compatible con RFC 8785 (JCS — JSON Canonicalization Scheme):

- **Entrada**: Envoltorio completo. Eliminar temporalmente `integrity.canonical_hash` antes de canonicalizar.
- **Cadenas**: Codificación UTF-8 con escape JSON estándar.
- **Objetos**: Claves ordenadas en orden lexicográfico.
- **Arrays**: Orden original preservado.
- **Números**: Representación JSON estándar (sin ceros finales).
- **Salida**: SHA-256 de la cadena de bytes canonicalizada, prefijada con `sha256:`.
- **Escritura de vuelta**: Almacenar el resultado en `integrity.canonical_hash`.

Implementación de referencia: `tests/pps-conformance/canonicalize.js`

## 7.4 Artefactos de Reproducción

- **REQ-310**: Los sistemas generadores SHOULD emitir un registro de reproducción (timestamp, host, versión de implementación) a `header.implementation` o un log de auditoría externo.

---

# 8. Seguridad & Cumplimiento

- **REQ-050**: Si `gdpr` está presente en `header.compliance`, MUST incluir explícitamente `no_pii` en `who.policy`.
- **REQ-051**: Si `why.constraints` prohíbe la navegación externa, MUST NOT incluir `web_browse` u otra herramienta de red externa.
- **REQ-052**: Si `why.constraints` prohíbe la navegación externa y `what.task` contiene una URL `http(s)://`, MUST reemplazarla o marcarla (p. ej. `[URL_REMOVED]`).
- **REQ-053**: Cada herramienta en `how_to_do.tools` MUST aparecer en `who.capabilities` (sandbox de capacidades).

## 8.1 Invariantes de Campos Cruzados

- **REQ-180**: `where.citations_required=true` ⇒ número de entradas de evidencia ≥ 1.
- **REQ-181**: `how_to_do.tools ⊆ who.capabilities`.
- **REQ-182**: `gdpr ∈ header.compliance` ⇒ `no_pii ∈ who.policy`.
- **REQ-183**: `no_external_browse ∈ why.constraints` ⇒ `web_browse ∉ how_to_do.tools`.

## 8.2 Bloqueos de Campo y Refinamiento Iterativo

- **REQ-344**: Los implementadores MAY proporcionar una lista de JSON Pointers en `body.how_meta.governance.locks` marcando rutas como "protegidas contra escritura".
- **REQ-345**: Los implementadores SHOULD registrar el origen de los campos clave en `header.implementation.origins` para propósitos de auditoría.

## 8.3 Pruebas de Cumplimiento de IA y Anclaje

- **REQ-346 (Prioridad de Anclaje)**: Cuando hay entrada del usuario o existen `locks` explícitos, la regeneración de IA MUST tratar esas rutas como anclas y MUST NOT sobreescribirlas.
- **REQ-347 (Semántica Operacional de Bloqueo)**:
  - Granularidad de bloqueo: cualquier JSON Pointer (escalar, objeto o array).
  - Prioridad: `locks` > `origins` > otras políticas de mejora.
  - Mecanismo de desbloqueo: una ruta MAY sobreescribirse solo cuando el usuario elimine explícitamente el puntero o pase `unlock=[...]` via UI o API.
- **REQ-348 (Restricción de Consistencia)**: Si `why.constraints` prohíbe la navegación externa, `how_to_do.tools` MUST NOT contener `web_browse`.
- **REQ-349 (Verificación Entre Turnos)**: Los implementadores SHOULD proporcionar una herramienta de comparación antes/después verificando que los valores en rutas designadas por `locks` permanezcan sin cambios.
- **REQ-350 (Manejo de Fallos)**: Cuando se viola una restricción de `locks` o consistencia, el sistema MUST revertir al valor anterior y registrar el evento de violación y remediación.

---

# 9. Conformidad

Los implementadores MUST pasar las siguientes pruebas:
1. La validación del JSON Schema pasa (REQ-001).
2. Las verificaciones de políticas pasan (REQ-050/051 etc.).
3. Consistencia del hash canónico: el mismo Envoltorio siempre produce el mismo `canonical_hash`.
4. Prueba de reproducibilidad: la misma entrada y estrategia de decodificación produce salida consistente entre plataformas (o dentro de la tolerancia definida).

## 9.1 Alineación Humano-IA

- **REQ-320**: `body.what.kpi` SHOULD proporcionar métricas medibles o criterios de aceptación.
- **REQ-321**: `body.why.goals` y `body.what.kpi` SHOULD ser mapeables (objetivo → métrica).
- **REQ-322**: Si se especifican `how_much.quality_guidance` u otros criterios medibles, SHOULD proporcionar también un `what.output_schema` computable o script de evaluación externo.
- **REQ-323**: `how_meta.governance.verification` SHOULD incluir `schema_validate` y `policy_check`.

---

# 10. Versionado

- **REQ-060**: `pps_version` sigue el versionado semántico; v1.0 es retrocompatible con nuevos campos opcionales añadidos en futuras versiones v1.x.

---

# 11. Perfil de Interoperabilidad

- **REQ-070**: El subconjunto mínimo comprende los campos requeridos de Cabecera + Cuerpo + Integridad descritos anteriormente; `how_meta` es opcional.

---

# 12. Implementación de Referencia (Informativo)

Este paquete de especificación no incluye scripts. Los implementadores MAY usar la implementación de referencia y la suite de conformidad publicadas por separado para validación y benchmarking a nivel de ingeniería. Consulte la página de lanzamiento para el enlace y número de versión autorizados.

---

# Anexo A (Informativo): Vocabulario de Restricciones Controlado

| Descripción | Clave en inglés |
|-------------|-----------------|
| Prohibir navegación externa | `no_external_browse` |
| Usar solo la evidencia proporcionada | `use_provided_evidence` |
| Citaciones requeridas | `citations_required` |
| Prohibir información de identificación personal | `no_pii` |

---

# Anexo B (Informativo): Perfil de Contenido PPS & Umbrales de Rigurosidad

Este anexo proporciona umbrales agnósticos al dominio para la creación de contenido y ejecución de tareas. No modifica la especificación principal; es un perfil de interoperabilidad opcional.

## B.1 Declaración de Perfil

Declarar en `header.compliance`:
- Perfil: `pps-content` (o `pps-core`, `pps-analysis`, `pps-code`, `custom`)
- Rigurosidad: `strict` | `balanced` (predeterminado) | `permissive`
- Ejemplo: `["pps-content", "balanced"]`

## B.2 Requisitos Estructurales y de Tipo (Bajo Este Perfil)

- `body.what.task` MUST ser una cadena no vacía.
- `body.who.audience`, si está presente, MUST ser un array.
- `body.how_to_do.steps`, si está presente, MUST ser un array.
- `body.how_much` SHOULD adoptar los cinco elementos de cuantificación:
  - `content_length` — longitud / escala
  - `structure_elements` — estructura / secciones / módulos
  - `detail_richness` — detalle / densidad de elementos
  - `quality_guidance` — estándares de calidad
  - `cultural_depth` — contexto cultural / profundidad de compromiso

## B.3 Umbrales Mínimos (por Rigurosidad)

| Nivel | `why.goals` | `who.audience` | `how_to_do.steps` | Elementos `how_much` |
|-------|:-----------:|:--------------:|:-----------------:|:--------------------:|
| `strict` | ≥ 4 | ≥ 4 | ≥ 6 | 5 / 5 |
| `balanced` (predeterminado) | ≥ 3 | ≥ 3 | ≥ 5 | ≥ 3 / 5 |
| `permissive` | ≥ 2 | ≥ 2 | ≥ 4 | ≥ 2 / 5 |

Bajo `strict`, el incumplimiento de los umbrales SHOULD reportarse como error; bajo `balanced` / `permissive`, como advertencia.

---

# Anexo C (Informativo): Ejemplo Mínimo Interoperable (balanced)

```json
{
  "header": {
    "pps_version": "PPS-v1.0.0",
    "model": {
      "name": "example-model",
      "digest": "sha256-model-xyz",
      "data_cutoff": "2025-01-01"
    },
    "decode": { "seed": 0, "temperature": 0, "top_p": 1 },
    "locale": "es-ES",
    "compliance": ["pps-content", "balanced"],
    "created_at": "2025-10-01T12:00:00Z"
  },
  "body": {
    "what": { "task": "Escribir una introducción estructurada sobre el tema" },
    "why": {
      "goals": [
        "Transmitir los conceptos fundamentales",
        "Proporcionar información accionable",
        "Facilitar la comprensión y aplicación"
      ]
    },
    "who": {
      "persona": "Asistente profesional",
      "audience": ["Principiantes", "Profesionales", "Tomadores de decisiones"]
    },
    "when": { "timeframe": "Ciclo actual, entrega por etapas" },
    "where": { "environment": "Documentación en línea y entorno de trabajo general" },
    "how_to_do": {
      "paradigm": "CoT",
      "steps": [
        "Identificar puntos clave",
        "Organizar estructura",
        "Redactar contenido",
        "Revisar y publicar",
        "Recopilar retroalimentación"
      ]
    },
    "how_much": {
      "content_length": "1000-1500 palabras",
      "structure_elements": "3-4 secciones principales con encabezados y resumen",
      "detail_richness": "5-8 puntos clave con ejemplos y datos donde sea necesario",
      "quality_guidance": "Flujo lógico, terminología consistente, alta legibilidad",
      "cultural_depth": "Referencias moderadas al contexto autoritativo o de la industria"
    },
    "how_feel": {
      "tone": "Profesional y accesible",
      "style": "Claro",
      "audience_level": "intermediate"
    }
  },
  "integrity": {
    "canonical_hash": "sha256:TO_BE_FILLED_AFTER_CANONICALIZATION"
  }
}
```

---

# Anexo D (Informativo): Listas de Verificación de Validación

## D.1 Estructura y Consistencia

- [ ] La validación del JSON Schema pasa (REQ-001)
- [ ] `body.what.task` no está vacío (REQ-100)
- [ ] `who.audience` es un array si está presente
- [ ] `how_to_do.steps` es un array si está presente
- [ ] `where.citations_required=true` ⇒ `evidence` ≥ 1 (REQ-180)
- [ ] `how_to_do.tools ⊆ who.capabilities` (REQ-181)
- [ ] Conflicto de restricción: `no_external_browse` ⇒ `web_browse` no permitido (REQ-183)

## D.2 Umbrales de Calidad (por Rigurosidad)

- **strict**:
  - [ ] `why.goals` ≥ 4
  - [ ] `who.audience` ≥ 4
  - [ ] `how_to_do.steps` ≥ 6
  - [ ] Los cinco elementos `how_much` completados (5/5)
- **balanced** (predeterminado): 3 / 3 / 5 / 3
- **permissive**: 2 / 2 / 4 / 2

## D.3 Reproducibilidad

- [ ] `decode.temperature=0` y `top_p=1` (determinista, REQ-012)
- [ ] `integrity.canonical_hash` calculado y almacenado (REQ-030 / REQ-300)
- [ ] Modelo y parámetros de decodificación registrados para garantizar consistencia de reproducción (REQ-040 / REQ-302 / REQ-303)

## D.4 Interfaz / Estructura de Salida Opcional

- [ ] Si `how_interface.schema` restringe la forma de salida, su valor es un objeto
- [ ] Si el esquema se proporciona solo en `what.output_schema`, el runtime MAY copiarlo a `how_interface.schema` para validación (REQ-175)

---

# Anexo E (Informativo): Especificación de Vinculación Opcional PPS-QR (Vinculación v1)

Este anexo define una vinculación opcional para transportar instrucciones PPS mediante código QR. No modifica la especificación principal.

## E.1 Objetivos

- Tras el escaneo, se puede leer directamente un resumen de instrucciones 5W3H legible por humanos, junto con la información necesaria para la verificación de integridad.
- No se incluye información sensible o privada; `integrity.canonical_hash` sirve como único ancla de integridad.

## E.2 Payload (Texto Plano UTF-8)

**MUST incluir:**
- `pps_version` (de `header.pps_version`)
- `created_at` (de `header.created_at`)
- `task` (de `body.what.task`)
- `canonical_hash` (valor completo `sha256:…`)
- `verification_hint` (p. ej. "Compare el hash para confirmar la integridad de la instrucción")
- `instruction` (texto de instrucción legible por humanos organizado por 5W3H)

**SHOULD incluir:**
- `id_short`: truncado de longitud fija de `canonical_hash` (últimos 12-16 caracteres recomendado)
- `provider_note`: nota legible por humanos

**MAY incluir:**
- `signature` / `public_key_id`: si la implementación usa firma
- `retrieval_uri`: URI opcional para recuperar el Envoltorio JSON

Diseño de texto recomendado:
```
Certificado de Instrucción PPS
Tarea: <task>
Creado: <created_at>
ID de Instrucción: <id_short>
Verificación: Compare el hash para confirmar la integridad de la instrucción
Versión PPS: <pps_version>
Hash Completo: <sha256:...>

=== Instrucción Completa ===

Qué:           ...
Por qué:       ...
Quién:         ...
Cuándo:        ...
Dónde:         ...
Cómo hacerlo:  ...
Cuánto:        ...
Cómo sentirlo: ...

=== Instrucciones de Uso ===
Por favor complete la tarea según el contenido anterior.
```

## E.3 Codificación y Corrección de Errores

- Codificación de caracteres: texto plano UTF-8.
- Nivel de corrección de errores: L o M; si el contenido es demasiado largo, las descripciones legibles por humanos MAY comprimirse moderadamente, pero las claves de encabezado 5W3H MUST NOT eliminarse.

## E.4 Seguridad y Privacidad

- MUST NOT incluir información de identificación personal, claves, tokens de acceso u otros datos sensibles.
- `id_short` es un identificador no sensible; la verificación estricta depende de recomputar y comparar `canonical_hash`.

## E.5 Flujo de Verificación (Lado del Escáner)

1. Leer `canonical_hash` e instrucción 5W3H.
2. Reconstruir un Envoltorio mínimo a partir de la instrucción (o recuperar el Envoltorio JSON via `retrieval_uri`).
3. Realizar la serialización canónica (eliminar `integrity`, ordenar claves de objeto lexicográficamente, JSON compacto).
4. Calcular SHA-256 y comparar con `canonical_hash`.
5. Coincidencia → verificación aprobada.

## E.6 Versionado

- Versión de vinculación: `PPS-QR Vinculación v1`.
- Añadir campos opcionales al formato de vinculación es retrocompatible con implementaciones existentes; los campos MUST permanecen sin cambios.
