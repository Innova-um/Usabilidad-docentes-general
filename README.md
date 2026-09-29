# Usabilidad docentes · Campus Virtual (general)

Tablero interactivo del uso del aula virtual (Moodle) por parte de los docentes de la Universidad del Magdalena en **todas las modalidades** (pregrado presencial, distancia y posgrado), periodo académico 2026-2.

## Qué muestra

- Tiempo de uso docente, docentes activos en plataforma, minutos al día por docente activo, y recursos y actividades creados.
- Filtros de selección múltiple Modalidad → Facultad → Programa, y buscador por docente o curso.
- Colores fijos por modalidad y facultad, y colores distintos para los programas que se estén comparando.
- Panel **Comparativo** con los grupos lado a lado en seis indicadores.
- Tabla de detalle por curso, por docente y comparativa por grupo.
- Vista en totales del periodo o en promedio por día.

## Cómo generarlo

1. Exporta el informe de Configurable Reports a Excel y guárdalo en la raíz como `Usabilidad Docentes.xlsx` (no se sube a GitHub).
2. Revisa las fechas de `PERIODO` al inicio de `build/build.py`.
3. Ejecuta:

   ```bash
   python build/build.py
   ```

   Se genera `index.html` con los datos incluidos. Ábrelo en el navegador; no necesita servidor.

Requisitos: Python 3 con `pandas` y `openpyxl`.

## Publicación

`index.html` contiene nombres y usuarios de docentes, por eso está en `.gitignore`. Publícalo en GitHub Pages solo con autorización para divulgar esos datos.

## Notas de cálculo

- **Tiempo de uso:** estimación a partir del log de Moodle. Se suma el tiempo entre clics consecutivos y se descartan las pausas de más de 30 minutos.
- **Recursos creados:** se cuentan por curso, una sola vez aunque el curso tenga varios docentes.
