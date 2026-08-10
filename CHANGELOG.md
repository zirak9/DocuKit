# Changelog

## Version 1.1.0 - 2026-08-09

### Nuevas características
- Historial de reportes: Cada ejecución genera un archivo con timestamp (BITACORA_YYYY-MM-DD_HH-MM.md)
- Reporte "Ultimo": Siempre disponible como BITACORA_ULTIMO.md (el mas reciente)
- Filtros de inventario: Todos | Ultimo año | Ultimo mes | Top 20 archivos mas recientes
- Seccion de historial en cada bitacora con todos los reportes generados

### Mejoras
- Nunca se borran reportes anteriores (historico completo)
- Interfaz HTA ahora busca BITACORA_ULTIMO.md automaticamente
- Pie de pagina actualizado con nuevo branding
- Distribucion de archivos: Top 10 carpetas mas grandes

### Branding
- Desarrollado por zirak9
- Impulsado por DAVOHOMEHOUSE
- Con tecnologia VALKYRIE FIRE WIND

### Correcciones
- Solucionado error de comparacion de fechas (datetime vs str)
- Mejor manejo de errores con traceback
- Encoding UTF-8 para caracteres especiales

---

# Changelog

## Version 1.0.0 - 2026-08-09

### Lanzamiento inicial

DocuKit nace en el ecosistema de DAVOHOMEHOUSE y VALKYRIE FIRE WIND.

### Características principales

- Escaneo automático de proyectos
- Perfiles: diseñador, escritor, desarrollador, genérico
- Generación de Reportes/BITACORA_PROYECTO.md, DOCUFY_DATA.json, RESUMEN_PROYECTO.txt
- Interfaz gráfica con DocuFlow.hta
- Scripts .bat para un solo clic
- Portable, sin dependencias externas
- Extensible: agregar nuevos perfiles en CONFIG

### Funcionalidades

- Detección automática del tipo de proyecto
- Formulario inteligente (solo 5 preguntas)
- Resumen de actividad reciente (últimos 7 días)
- Tabla de inventario de activos
- Backup automático de bitácora existente

### Aspectos técnicos

- Python 3.x compatible
- Sin dependencias externas
- Cross-platform (Windows, Mac, Linux)

---

**Presentado por DAVOHOMEHOUSE**  
**Tecnología VALKYRIE FIRE WIND**  
**Hecho por zirak9**
