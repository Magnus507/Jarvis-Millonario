---
skill: Mantenimiento de Estructura e Instrucciones
agent: Jarvisin
---

# 🛠️ Skill: Guardián del Orden (Folders & Docs)

Este módulo le da a Jarvisin la capacidad de mantener el Vault como un reloj suizo.

## 📋 Capacidades

### 1. Auto-Limpieza de Carpetas
- **Trigger:** Creación de archivos fuera de la estructura PARA.
- **Acción:** Jarvisin identificará el archivo y sugerirá al usuario moverlo a `01_Proyectos`, `02_Recursos` o `99_Media`.

### 2. Actualización Dinámica de Guías
- **Trigger:** Cambio en la metodología de trabajo del equipo.
- **Acción:** Jarvisin actualizará automáticamente la `[[Guia_de_Uso_Jarvis_Millonario]]` para reflejar las nuevas reglas.

### 3. Auditoría de MOCs (Maps of Content)
- **Trigger:** Creación de una nueva nota técnica.
- **Acción:** Jarvisin verificará que la nota principal del proyecto correspondiente tenga un enlace a esta nueva información.

## 📑 Protocolo de Documentación
Jarvisin debe asegurar que cada archivo tenga:
1. **Propiedades (YAML):** tags, estado y última actualización.
2. **Backlinks:** Enlace de retorno al proyecto o al índice central.
3. **Claridad:** Un resumen ejecutivo al inicio si la nota es extensa.

---
*Módulo de Skill: v1.1*
