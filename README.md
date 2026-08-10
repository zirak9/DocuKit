# DocuKit - Documentación con un solo clic

<p align="center">
  <strong>
    Presentado por DAVOHOMEHOUSE · 
    Tecnología VALKYRIE FIRE WIND · 
    Hecho por zirak9
  </strong>
</p>

---

> "Documenta tu proyecto mientras creas, no mientras sufres"

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/zirak9/DocuKit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

---

## Tabla de Contenidos

- [¿Qué es DocuKit?](#qué-es-docukit)
- [¿Quién está detrás?](#quién-está-detrás)
- [Cómo funciona](#cómo-funciona)
- [Perfiles disponibles](#perfiles-disponibles)
- [Documentos generados](#documentos-generados)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Extensibilidad](#extensibilidad)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

---

## ¿Qué es DocuKit?

**DocuKit** es una herramienta portable que documenta automáticamente cualquier proyecto con solo hacer doble clic.

**Olvídate de:**
- Llenar formularios interminables
- Mantener bitácoras manuales
- Explicar a los artistas/escritores/desarrolladores cómo documentar

**Con DocuKit:**
- Escanea automáticamente tu proyecto
- Infiere el tipo de proyecto (diseñador, escritor, desarrollador, genérico)
- Solo pregunta 5 datos clave (opcional)
- Genera 3 documentos: Markdown, JSON y TXT

---

## ¿Quién está detrás?

DocuKit es una herramienta desarrollada en el ecosistema creativo de:

| Organización | Rol | Descripción |
|--------------|-----|-------------|
| **DAVOHOMEHOUSE** | Presenta | Portal de arte y creatividad digital |
| **VALKYRIE FIRE WIND** | Tecnología | Empresa mexicana de innovación tecnológica |
| **zirak9** | Creador | Desarrollador independiente y artista digital |

> DocuKit nace de la necesidad de documentar sin interrumpir el flujo creativo. Es el puente entre el arte y la tecnología.

---

## Cómo funciona

### 1. Copia la carpeta

```bash
MI_PROYECTO/
├── DocuKit/          # Copia esta carpeta aquí
├── 01_PERSONAJES/
├── 03_PROYECTOS_Y_DEMOS/
└── ...
```

### 2. Haz doble clic en tu perfil

```bash
DocuKit/
└── scripts/
    ├── disenador.bat        # Para artistas/ilustradores
    ├── escritor.bat         # Para escritores
    ├── desarrollador.bat    # Para programadores
    └── generico.bat         # Para cualquier proyecto
```

### 3. Responde 5 preguntas (opcional)
```bash
Cuestionario para DISENADOR
   (Presiona Enter para omitir)
--------------------------------------------------
  Descripcion Visual: Personaje principal para serie
  Herramientas Usadas: Midjourney, Photoshop
  Estilo Artistico: Cyberpunk
  Personajes Incluidos: Neon, Glitch
  Estado: WIP
```

### 4. ¡Listo!
```bash
PROYECTO DOCUMENTADO
   Reportes/BITACORA_PROYECTO.md
   Reportes/DOCUFY_DATA.json
   Reportes/RESUMEN_PROYECTO.txt
```

### Interfaz Gráfica Alternativa

Si no quieres usar la terminal, haz doble clic en DocuFlow.hta:

Selecciona tu perfil

Presiona "Documentar ahora"

Sin tocar la terminal

---

## Perfiles disponibles
| Perfil | Para | Preguntas clave |
|--------|------|-----------------|
| **Diseñador** | IA + Photoshop/GIMP | Descripción, herramientas, estilo, personajes, estado |
| **Escritor** | Libros, guiones, narrativa | Título, género, palabras, personajes, sinopsis |
| **Desarrollador** | Código, software | Lenguaje, framework, versiones, dependencias, estado |
| **Genérico** | Cualquier proyecto | Descripción, objetivo, recursos, equipo, estado |

---

## Documentos generados
| Archivo | Formato | Ubicación | Propósito |
|---------|---------|-----------|-----------|
| `BITACORA_PROYECTO.md` | Markdown | `/Reportes/` | Trazabilidad legal, reportes, presentaciones |
| `DOCUFY_DATA.json` | JSON | `/Reportes/` | Integración con otras herramientas, automatización |
| `RESUMEN_PROYECTO.txt` | TXT | `/Reportes/` | Vista rápida, compartir por chat |

### Ejemplo de BITACORA_PROYECTO.md

```markdown
# Neon_Cyberpunk

**Tipo:** DISENADOR
**Ultima actualizacion:** 09/08/2026 14:30

## Resumen Automatico
- **Total de archivos:** 847
- **Tamaño total:** 234.5 MB
- **Ultima modificacion:** 2026-08-09T14:28:12

### Actividad reciente (ultimos 7 dias)
- `neon_character.png` (03_PROYECTOS_Y_DEMOS/) - 09/08/2026
- `glitch_animation.gif` (03_PROYECTOS_Y_DEMOS/) - 08/08/2026

### Distribucion de archivos
- `01_PERSONAJES/Final_Assets/`: 156 archivos
- `01_PERSONAJES/Raw_AI/`: 234 archivos
- `03_PROYECTOS_Y_DEMOS/`: 368 archivos

## Metadatos del Proyecto
- **Descripcion Visual:** Personaje principal para serie Cyberpunk
- **Herramientas Usadas:** Midjourney, Photoshop
- **Estado:** WIP
```

---

# Requisitos
Python 3.x (cualquier versión)

Sin dependencias externas (solo usa librerías estándar)

Windows (también funciona en Mac/Linux con python3)

---

# Instalación
### Opción 1: Clonar (recomendado)
```bash
git clone https://github.com/zirak9/DocuKit.git
```
### Opción 2: Descargar ZIP
Ve a https://github.com/zirak9/DocuKit

Click en "Code" → "Download ZIP"

Extrae la carpeta dentro de tu proyecto

### Opción 3: Copia manual
Copia la carpeta DocuKit/ en la raíz de cualquier proyecto.

---

# Extensibilidad
Puedes agregar tu propio perfil editando docufy_engine.py:

```python
"musico": {
    "preguntas": [
        "genero_musical",
        "instrumentos_usados",
        "bpm",
        "duracion_estimada",
        "estado"
    ],
    "carpetas_clave": ["01_PISTAS", "02_SAMPLES", "03_MEZCLAS"],
    "emoji": ""
}
```

Luego crea tu archivo .bat personalizado:

```batch
@echo off
python "%~dp0..\docufy_engine.py"
pause
```

---

## Contribuir
Las contribuciones son bienvenidas.

### Áreas de mejora
* Más perfiles (músico, arquitecto, data scientist, etc.)
* Modo "watch" (documentar automáticamente al detectar cambios)
* Generación de copy para Patreon
* Integración con Git (auto-documentar en cada commit)
* Versión compilada (.exe) sin Python
* Exportar a PDF

### Proceso
* Fork el repositorio
* Crea una rama (git checkout -b feature/nueva-funcion)
* Commit (git commit -am 'Agrego perfil para músicos')
* Push (git push origin feature/nueva-funcion)
* Pull Request

---

## Licencia
MIT License - Copyright (c) 2026 zirak9 · DAVOHOMEHOUSE · VALKYRIE FIRE WIND

DocuKit es software libre. Úsalo, modifícalo, compártelo. Solo recuerda de dónde viene.

Autor: zirak9

GitHub: @zirak9

DAVOHOMEHOUSE: davohomehouse.com

VALKYRIE FIRE WIND: valkyriefirewind.com

---

Créditos institucionales
| Entidad	| Aporte |
|---------|--------|
| DAVOHOMEHOUSE |	Concepto creativo y dirección de arte |
| VALKYRIE FIRE WIND |	Infraestructura tecnológica y soporte  |
| zirak9 |	Desarrollo, diseño e implementación|

> "Documenta tu proyecto mientras creas, no mientras sufres"
<p align="center">
  <strong>
    Desarrollado por zirak9 · 
    Presentado por DAVOHOMEHOUSE · 
    Tecnología VALKYRIE FIRE WIND
  </strong>
</p>
