# Tasks: Convertidor de Temperatura

**Input**: Design documents from `/specs/001-temperature-converter/`

**Prerequisites**: [plan.md](file:///C:/Users/pc/cursokt/curso-mcp-karentenorio/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/plan.md), [spec.md](file:///C:/Users/pc/cursokt/curso-mcp-karentenorio/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/spec.md), [research.md](file:///C:/Users/pc/cursokt/curso-mcp-karentenorio/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/research.md), [data-model.md](file:///C:/Users/pc/cursokt/curso-mcp-karentenorio/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/data-model.md), [contracts/cli-api.md](file:///C:/Users/pc/cursokt/curso-mcp-karentenorio/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/contracts/cli-api.md)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Exact file paths are provided for each task.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify project environment and uv dependencies in pyproject.toml
- [x] T002 Configure test suite directory structure in tests/test_converter.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T003 Implement Unit enum and base exceptions in src/mi_proyecto_speckit/converter.py
- [x] T004 Implement rounding and numeric formatting helpers in src/mi_proyecto_speckit/converter.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Conversión entre Celsius y Fahrenheit (Priority: P1) 🎯 MVP

**Goal**: Convertir de forma bidireccional entre grados Celsius y Fahrenheit con redondeo a 3 decimales.

**Independent Test**: Ejecutar pruebas unitarias de conversión C <-> F y verificar resultados esperados como 0°C = 32.000°F y 212°F = 100.000°F.

### Tests for User Story 1 ⚠️

- [x] T005 [P] [US1] Unit test for Celsius to Fahrenheit and reverse conversions in tests/test_converter.py

### Implementation for User Story 1

- [x] T006 [US1] Implement Celsius <-> Fahrenheit conversion formulas in src/mi_proyecto_speckit/converter.py

**Checkpoint**: User Story 1 (MVP) functional and testable independently

---

## Phase 4: User Story 2 - Conversión con Kelvin y Validación de Cero Absoluto (Priority: P2)

**Goal**: Soporte completo de Kelvin (Kelvin <-> Celsius, Kelvin <-> Fahrenheit) y validación estricta del cero absoluto (<0 K).

**Independent Test**: Verificar conversiones exactas con Kelvin (ej. 0°C = 273.150 K) y confirmar que cualquier valor < 0 K lance ValueError descriptivo.

### Tests for User Story 2 ⚠️

- [x] T007 [P] [US2] Unit test for Kelvin conversions and absolute zero rejection in tests/test_converter.py

### Implementation for User Story 2

- [x] T008 [US2] Implement Kelvin conversions and absolute zero validation rules in src/mi_proyecto_speckit/converter.py

**Checkpoint**: User Stories 1 and 2 functional and testable independently

---

## Phase 5: User Story 3 - Manejo de Identidad y Entradas No Numéricas (Priority: P3)

**Goal**: Manejar conversiones de la misma unidad (identidad), números negativos válidos y capturar entradas no numéricas/vacías con mensajes limpios.

**Independent Test**: Verificar conversiones identidad (C -> C), números negativos (ej. -40°C = -40.000°F) y mensajes de error amigables ante entradas de texto o vacías.

### Tests for User Story 3 ⚠️

- [x] T009 [P] [US3] Unit test for identity conversions, negative values, and non-numeric inputs in tests/test_converter.py

### Implementation for User Story 3

- [x] T010 [US3] Implement identity conversion and input validation logic in src/mi_proyecto_speckit/converter.py
- [x] T011 [US3] Implement CLI user interface and entrypoint with error handling in src/mi_proyecto_speckit/cli.py
- [x] T012 [US3] Expose main CLI entrypoint in src/mi_proyecto_speckit/__init__.py

**Checkpoint**: All user stories functional and testable independently

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verificación integral, contratos y ejecución end-to-end

- [x] T013 [P] Execute end-to-end CLI validation scenarios per specs/001-temperature-converter/quickstart.md
- [x] T014 Run complete test suite via uv run pytest and verify 100% pass rate in tests/test_converter.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - Can proceed sequentially: US1 (MVP) → US2 → US3.
- **Polish (Phase 6)**: Depends on all user stories completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P2)**: Can start after Foundational (Phase 2).
- **User Story 3 (P3)**: Can start after Foundational (Phase 2).

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup (T001 - T002)
2. Complete Phase 2: Foundational (T003 - T004)
3. Complete Phase 3: User Story 1 (T005 - T006)
4. Validate MVP independently.

### Incremental Delivery
1. Foundation ready (Phases 1-2).
2. Add Celsius ↔ Fahrenheit (MVP, Phase 3).
3. Add Kelvin & Cero Absoluto (Phase 4).
4. Add CLI & Robustez ante errores (Phase 5).
5. Final Polish & Quickstart (Phase 6).
