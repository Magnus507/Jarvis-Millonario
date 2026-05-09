# ⚖️ Cumplimiento Técnico: Ley 81 de Panamá (Protección de Datos)
Proyecto: [[Plataforma Médica Panamá]]

Para operar legalmente en Panamá, la plataforma debe cumplir con los siguientes pilares de la Ley 81 de 2019 y su reglamento:

## 1. Consentimiento Informado y Explícito
- **Acción:** Implementar un modal de términos y condiciones específico para "Datos Sensibles de Salud" en el registro.
- **Técnico:** Guardar `consentimiento_timestamp` y `consentimiento_version` en la tabla `usuarios`.

## 2. Derechos ARCO (Acceso, Rectificación, Cancelación y Oposición)
- **Acción:** Crear una sección en el perfil del paciente llamada "Gestionar mi Información".
- **Funcionalidades:**
    - Botón "Descargar mi Historial" (Portabilidad/Acceso).
    - Botón "Eliminar mi Cuenta y Datos" (Cancelación - considerar anonimización si hay registros clínicos compartidos).
    - Opción "Revocar acceso a Médicos" (Oposición).

## 3. Seguridad de Datos Sensibles
- **Acción:** Reforzar Supabase RLS.
- **Auditoría:** Crear tabla `logs_acceso_medico` para registrar quién vio qué perfil, con qué QR y en qué momento. Esto es exigido para demostrar la trazabilidad del dato sensible.

## 4. Transferencia de Datos
- **Acción:** El sistema de QR de 2 horas cumple con la "temporalidad" del acceso, minimizando el riesgo de exposición prolongada.

---
*Documento generado por Jarvisin - 2026-05-09*
