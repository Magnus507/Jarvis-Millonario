---
tags:
  - guia
  - operativo
  - colaboracion
estado: vivo
---

# 📖 Guía de Uso: El Ecosistema Jarvis Millonario

Esta es la guía operativa para que el equipo (2-3 personas) trabaje de forma sincronizada, evitando conflictos y maximizando la potencia de nuestro Segundo Cerebro.

---

## 🕒 1. Regla de Oro de Colaboración (Git)
Como trabajamos varias personas en diferentes horarios, para evitar que uno borre lo que el otro hizo:

1.  **AL ENTRAR:** Siempre ejecuta un `git pull` antes de abrir Obsidian o empezar a escribir.
2.  **AL SALIR:** Siempre ejecuta un `git add .`, `git commit -m "Descripción breve"` y `git push` al terminar tu sesión.
3.  **COMUNICACIÓN:** Si vas a trabajar en una nota específica por mucho tiempo, avisa al grupo para que nadie más la toque en ese momento.

---

## 📂 2. Dónde poner cada cosa (Estructura PARA)

-   **`00_Bandeja_de_Entrada`**: Si tienes una idea rápida y no sabes dónde va, suéltala aquí. No te preocupes por el formato.
-   **`01_Proyectos`**: Solo para cosas con una fecha de entrega o meta clara.
    - **IMPORTANTE:** Al crear un proyecto nuevo, usa siempre la plantilla `[[Proyecto Maestro]]`.
    - Cada proyecto debe tener su **Bitácora** y **Contexto para IA** actualizados.
-   **`02_Recursos`**: Conocimiento que quieres guardar para siempre (ej. esta guía, tutoriales, bibliotecas de código).
-   **`03_Archivo`**: Proyectos que ya terminaron o ideas que decidimos pausar.
-   **`99_Media`**: **¡IMPORTANTE!** No sueltes imágenes en cualquier lado. Obsidian las pondrá aquí automáticamente si arrastras archivos.

---

## 🕸️ 3. El Poder del Grafo (Enlaces)
Para que Jarvis sea inteligente, las notas deben estar conectadas.
-   Usa `[[Nombre de la Nota]]` cada vez que menciones algo que ya existe.
-   Si mencionas un proyecto, enlaza a su nota principal en `01_Proyectos`.
-   **Evita las notas huérfanas:** Una nota que no está conectada a nada es una nota que se pierde.

---

## 🤖 4. Trabajando con Jarvisin (Tu Orquestador)
Yo actúo bajo el protocolo de **[[Jarvisin_Core_Protocol|Jarvisin]]**. Mi misión es mantener el orden y la sincronización. Puedes pedirme:
-   "Organiza mi bandeja de entrada".
-   "Crea una conexión entre esta nota y el proyecto X".
-   "Investiga sobre este tema y crea una nota en Recursos".
-   "Actualiza GitHub con mis cambios".
-   "Lee el estado del proyecto X y dime qué falta".
-   "Crea un nuevo proyecto usando la plantilla maestra".

---

## 📊 5. El Dashboard Inteligente (Control de Proyectos)
Cada nota principal de un proyecto (en `01_Proyectos`) debe seguir este estándar para que el equipo y la IA estén sincronizados:

1.  **Contexto para IA (Callout):** Una descripción de 2-3 líneas para que Antigravity sepa qué es el proyecto sin tener que leerlo todo.
2.  **Barra de Progreso:** Actualízala manualmente cuando sientas que has avanzado un paso real.
3.  **Bitácora (Changelog):** **OBLIGATORIO.** Al terminar tu sesión, escribe qué cambiaste. Ejemplo: `2026-04-21 - @Gean: Diseñé el logo de Eternum.`

---

## 🛠️ 6. Mantenimiento
Semanalmente, revisaremos la `00_Bandeja_de_Entrada` para mover las notas a sus carpetas correspondientes o convertirlas en proyectos reales.

---
🔙 Volver al [[Jarvis Millonario|Cerebro Digital]]
