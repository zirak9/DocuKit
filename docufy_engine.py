#!/usr/bin/env python3
# docufy_engine.py - Documentación con un solo clic
# Presentado por DAVOHOMEHOUSE · Tecnología VALKYRIE FIRE WIND · Hecho por zirak9

import os
import json
import datetime
from pathlib import Path
import sys
import shutil

# ========== CONFIGURACIÓN ==========
CONFIG = {
    "version": "1.1",
    "carpeta_reportes": "Reportes",
    "tipos_proyecto": {
        "diseñador": {
            "preguntas": [
                "descripcion_visual",
                "herramientas_usadas",
                "estilo_artistico",
                "personajes_incluidos",
                "estado"
            ],
            "carpetas_clave": ["01_PERSONAJES", "02_BANCO_VARIOS", "03_PROYECTOS_Y_DEMOS"],
            "emoji": ""
        },
        "escritor": {
            "preguntas": [
                "titulo_obra",
                "genero_literario",
                "numero_palabras",
                "personajes_principales",
                "sinopsis"
            ],
            "carpetas_clave": ["01_CAPITULOS", "02_BORRADORES", "03_FINAL"],
            "emoji": ""
        },
        "desarrollador": {
            "preguntas": [
                "lenguaje_principal",
                "framework",
                "version",
                "dependencias_clave",
                "estado_desarrollo"
            ],
            "carpetas_clave": ["src", "tests", "docs", "assets"],
            "emoji": ""
        },
        "generico": {
            "preguntas": [
                "descripcion_general",
                "objetivo_principal",
                "recursos_utilizados",
                "equipo_responsable",
                "estado"
            ],
            "carpetas_clave": ["docs", "assets", "output"],
            "emoji": ""
        }
    }
}

def obtener_ruta_proyecto():
    """Detecta que estamos en DocuKit/ y sube un nivel"""
    ruta_actual = Path.cwd()
    
    if ruta_actual.name == "DocuKit":
        ruta_proyecto = ruta_actual.parent
        print(f"Detectado: DocuKit dentro de {ruta_proyecto.name}")
    else:
        ruta_proyecto = ruta_actual
        print(f"Carpeta actual: {ruta_proyecto.name}")
    
    return ruta_proyecto

def obtener_tipo_proyecto():
    """Detecta automáticamente o pregunta el tipo"""
    if Path("01_PERSONAJES").exists() and Path("03_PROYECTOS_Y_DEMOS").exists():
        return "diseñador"
    elif Path("01_CAPITULOS").exists() or Path("02_BORRADORES").exists():
        return "escritor"
    elif Path("src").exists() and Path("tests").exists():
        return "desarrollador"
    
    print("\nQue tipo de proyecto eres?")
    print("  1. Disenador (IA + Photoshop/GIMP)")
    print("  2. Escritor (libros, guiones)")
    print("  3. Desarrollador (software)")
    print("  4. Generico (cualquier cosa)")
    
    opcion = input("  Elige (1-4): ").strip()
    
    tipos = {
        "1": "diseñador", 
        "2": "escritor", 
        "3": "desarrollador", 
        "4": "generico"
    }
    
    return tipos.get(opcion, "generico")

def obtener_nivel_detalle():
    """Pregunta al usuario qué nivel de detalle quiere en el inventario"""
    print("\nNivel de detalle para el inventario de archivos:")
    print("  1. Todos los archivos (completo, puede ser extenso)")
    print("  2. Solo archivos del ultimo año")
    print("  3. Solo archivos del ultimo mes")
    print("  4. Solo los 20 archivos mas recientes (recomendado)")
    
    opcion = input("  Elige (1-4): ").strip()
    
    niveles = {
        "1": "todos",
        "2": "anio",
        "3": "mes",
        "4": "top20"
    }
    
    return niveles.get(opcion, "top20")

def escanear_proyecto(ruta, tipo_proyecto, nivel_detalle):
    """Escanea automáticamente todo el proyecto"""
    metadatos = {
        "nombre_proyecto": ruta.name,
        "fecha_escaneo": datetime.datetime.now().isoformat(),
        "tipo": tipo_proyecto,
        "nivel_detalle": nivel_detalle,
        "total_archivos": 0,
        "archivos_por_tipo": {},
        "archivos_por_carpeta": {},
        "ultima_modificacion": None,
        "ultima_modificacion_str": None,
        "tamano_total_mb": 0,
        "archivos_recientes": [],
        "todos_los_archivos": []
    }
    
    ahora = datetime.datetime.now()
    limite_reciente = ahora - datetime.timedelta(days=7)
    
    for archivo in ruta.rglob("*"):
        if archivo.is_file() and not archivo.name.startswith("."):
            if "DocuKit" in str(archivo) or "Reportes" in str(archivo):
                continue
                
            metadatos["total_archivos"] += 1
            
            ext = archivo.suffix.lower()
            metadatos["archivos_por_tipo"][ext] = metadatos["archivos_por_tipo"].get(ext, 0) + 1
            
            rel_path = str(archivo.relative_to(ruta))
            carpeta = str(Path(rel_path).parent)
            if carpeta and carpeta != ".":
                metadatos["archivos_por_carpeta"][carpeta] = metadatos["archivos_por_carpeta"].get(carpeta, 0) + 1
            
            try:
                mtime = datetime.datetime.fromtimestamp(archivo.stat().st_mtime)
            except Exception:
                mtime = ahora
            
            if metadatos["ultima_modificacion"] is None or mtime > metadatos["ultima_modificacion"]:
                metadatos["ultima_modificacion"] = mtime
                metadatos["ultima_modificacion_str"] = mtime.isoformat()
            
            if mtime > limite_reciente:
                metadatos["archivos_recientes"].append({
                    "nombre": archivo.name,
                    "carpeta": carpeta,
                    "fecha": mtime.strftime("%d/%m/%Y"),
                    "mtime": mtime
                })
            
            metadatos["todos_los_archivos"].append({
                "nombre": archivo.name,
                "carpeta": carpeta,
                "fecha": mtime.strftime("%d/%m/%Y"),
                "mtime": mtime,
                "ext": archivo.suffix.upper() or "SIN EXT",
                "ruta": archivo
            })
            
            metadatos["tamano_total_mb"] += archivo.stat().st_size / (1024 * 1024)
    
    metadatos["tamano_total_mb"] = round(metadatos["tamano_total_mb"], 2)
    metadatos["archivos_recientes"] = metadatos["archivos_recientes"][:10]
    metadatos["todos_los_archivos"].sort(key=lambda x: x["mtime"], reverse=True)
    
    if metadatos["ultima_modificacion"] is None:
        metadatos["ultima_modificacion"] = ahora
        metadatos["ultima_modificacion_str"] = ahora.isoformat()
    
    return metadatos

def filtrar_archivos(metadatos, nivel_detalle):
    """Filtra los archivos según el nivel de detalle seleccionado"""
    ahora = datetime.datetime.now()
    
    if nivel_detalle == "todos":
        return metadatos["todos_los_archivos"]
    elif nivel_detalle == "anio":
        fecha_limite = ahora - datetime.timedelta(days=365)
        return [a for a in metadatos["todos_los_archivos"] if a["mtime"] > fecha_limite]
    elif nivel_detalle == "mes":
        fecha_limite = ahora - datetime.timedelta(days=30)
        return [a for a in metadatos["todos_los_archivos"] if a["mtime"] > fecha_limite]
    elif nivel_detalle == "top20":
        return metadatos["todos_los_archivos"][:20]
    else:
        return metadatos["todos_los_archivos"][:20]

def formulario_inteligente(tipo_proyecto):
    """Formulario adaptativo según el tipo"""
    preguntas = CONFIG["tipos_proyecto"][tipo_proyecto]["preguntas"]
    
    print(f"\nCuestionario para {tipo_proyecto.upper()}")
    print("   (Presiona Enter para omitir)")
    print("-" * 50)
    
    datos = {}
    for pregunta in preguntas:
        label = pregunta.replace("_", " ").title()
        valor = input(f"  {label}: ").strip()
        if valor:
            datos[pregunta] = valor
    
    return datos

def generar_documentacion(ruta, metadatos, datos_formulario, archivos_filtrados):
    """Genera la documentación en la carpeta Reportes/ con timestamp"""
    
    carpeta_reportes = ruta / CONFIG["carpeta_reportes"]
    carpeta_reportes.mkdir(exist_ok=True)
    
    # ===== GENERAR TIMESTAMP PARA EL NOMBRE DEL ARCHIVO =====
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # ===== 1. BITÁCORA PRINCIPAL CON TIMESTAMP =====
    bitacora_path = carpeta_reportes / f"BITACORA_{timestamp}.md"
    bitacora_ultimo = carpeta_reportes / "BITACORA_ULTIMO.md"
    
    contenido = []
    
    # ===== TÍTULO Y ENCABEZADO =====
    contenido.append(f"# {metadatos['nombre_proyecto']}")
    contenido.append("")
    contenido.append(f"**Tipo:** {metadatos['tipo'].upper()}")
    contenido.append(f"**Ultima actualizacion:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
    contenido.append("")
    
    # ===== RESUMEN EJECUTIVO =====
    contenido.append("## Resumen Ejecutivo")
    contenido.append("")
    contenido.append(f"- **Total de archivos:** {metadatos['total_archivos']}")
    contenido.append(f"- **Tamaño total:** {metadatos['tamano_total_mb']} MB")
    contenido.append(f"- **Ultima modificacion:** {metadatos['ultima_modificacion_str']}")
    contenido.append("")
    
    # ===== METADATOS DEL PROYECTO =====
    if datos_formulario:
        contenido.append("## Metadatos del Proyecto")
        contenido.append("")
        for clave, valor in datos_formulario.items():
            label = clave.replace("_", " ").title()
            contenido.append(f"- **{label}:** {valor}")
        contenido.append("")
    
    # ===== DISTRIBUCIÓN DE ARCHIVOS =====
    contenido.append("## Distribucion de Archivos")
    contenido.append("")
    carpetas_ordenadas = sorted(metadatos["archivos_por_carpeta"].items(), key=lambda x: x[1], reverse=True)[:10]
    for carpeta, count in carpetas_ordenadas:
        contenido.append(f"- `{carpeta}/`: {count} archivos")
    
    if len(metadatos["archivos_por_carpeta"]) > 10:
        total_carpetas = len(metadatos["archivos_por_carpeta"])
        contenido.append(f"- ... y {total_carpetas - 10} carpetas adicionales")
    contenido.append("")
    
    # ===== ACTIVIDAD RECIENTE =====
    if metadatos["archivos_recientes"]:
        contenido.append("## Actividad Reciente (ultimos 7 dias)")
        contenido.append("")
        for arch in metadatos["archivos_recientes"]:
            contenido.append(f"- `{arch['nombre']}` ({arch['carpeta']}) - {arch['fecha']}")
        contenido.append("")
    
    # ===== INVENTARIO DE ACTIVOS =====
    contenido.append("## Inventario de Activos")
    contenido.append("")
    
    filtros = {
        "todos": "Todos los archivos",
        "anio": "Archivos del ultimo año",
        "mes": "Archivos del ultimo mes",
        "top20": "20 archivos mas recientes"
    }
    contenido.append(f"**Filtro aplicado:** {filtros.get(metadatos['nivel_detalle'], '20 mas recientes')}")
    contenido.append("")
    contenido.append("| Nombre | Tipo | Ubicacion | Ultima modificacion |")
    contenido.append("|--------|------|-----------|-------------------|")
    
    for arch in archivos_filtrados:
        nombre = arch["nombre"]
        ext = arch["ext"]
        ubicacion = arch["carpeta"] if arch["carpeta"] != "." else "Raiz"
        fecha = arch["fecha"]
        contenido.append(f"| {nombre} | {ext} | {ubicacion} | {fecha} |")
    
    total_mostrados = len(archivos_filtrados)
    total_reales = metadatos["total_archivos"]
    if total_mostrados < total_reales:
        contenido.append(f"| ... y {total_reales - total_mostrados} archivos no mostrados | | | |")
    
    contenido.append("")
    
    # ===== HISTÓRICO DE REPORTES =====
    contenido.append("## Historial de Reportes")
    contenido.append("")
    contenido.append("| Fecha | Archivo |")
    contenido.append("|-------|---------|")
    
    reportes = sorted(carpeta_reportes.glob("BITACORA_*.md"))
    for reporte in reportes:
        try:
            fecha_str = reporte.stem.replace("BITACORA_", "")
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d_%H-%M")
            fecha_legible = fecha.strftime("%d/%m/%Y %H:%M")
        except:
            fecha_legible = "Fecha desconocida"
        contenido.append(f"| {fecha_legible} | `{reporte.name}` |")
    
    contenido.append("")
    
    # ===== PIE DE PÁGINA (NUEVA REDACCIÓN) =====
    contenido.append("")
    contenido.append(f"*Documentacion generada por DocuKit v{CONFIG['version']} - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}*")
    contenido.append("")
    contenido.append(f"*Desarrollado por zirak9 | Impulsado por DAVOHOMEHOUSE | Con tecnologia VALKYRIE FIRE WIND*")

    with open(bitacora_path, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))
    
    shutil.copy2(bitacora_path, bitacora_ultimo)
    
    # ===== 2. JSON CON TIMESTAMP =====
    json_path = carpeta_reportes / f"DOCUFY_DATA_{timestamp}.json"
    json_ultimo = carpeta_reportes / "DOCUFY_DATA_ULTIMO.json"
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadatos": {
                "nombre_proyecto": metadatos["nombre_proyecto"],
                "fecha_escaneo": metadatos["fecha_escaneo"],
                "tipo": metadatos["tipo"],
                "nivel_detalle": metadatos["nivel_detalle"],
                "total_archivos": metadatos["total_archivos"],
                "archivos_por_tipo": metadatos["archivos_por_tipo"],
                "archivos_por_carpeta": metadatos["archivos_por_carpeta"],
                "ultima_modificacion": metadatos["ultima_modificacion_str"],
                "tamano_total_mb": metadatos["tamano_total_mb"],
                "archivos_recientes": metadatos["archivos_recientes"]
            },
            "formulario": datos_formulario,
            "timestamp": datetime.datetime.now().isoformat(),
            "version": CONFIG["version"],
            "reporte_numero": len(list(carpeta_reportes.glob("BITACORA_*.md"))),
            "branding": {
                "desarrollado": "zirak9",
                "impulsado": "DAVOHOMEHOUSE",
                "tecnologia": "VALKYRIE FIRE WIND"
            }
        }, f, indent=2, ensure_ascii=False)
    
    shutil.copy2(json_path, json_ultimo)
    
    # ===== 3. TXT simple =====
    txt_path = carpeta_reportes / f"RESUMEN_{timestamp}.txt"
    txt_ultimo = carpeta_reportes / "RESUMEN_ULTIMO.txt"
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"PROYECTO: {metadatos['nombre_proyecto']}\n")
        f.write(f"TIPO: {metadatos['tipo'].upper()}\n")
        f.write(f"FECHA: {datetime.datetime.now().strftime('%d/%m/%Y')}\n")
        f.write(f"HORA: {datetime.datetime.now().strftime('%H:%M')}\n")
        f.write(f"REPORTE NRO: {len(list(carpeta_reportes.glob('BITACORA_*.md')))}\n")
        f.write(f"ARCHIVOS: {metadatos['total_archivos']}\n")
        f.write(f"TAMAÑO: {metadatos['tamano_total_mb']} MB\n")
        f.write(f"FILTRO: {metadatos['nivel_detalle']}\n")
        f.write("-" * 40 + "\n")
        if datos_formulario:
            for clave, valor in datos_formulario.items():
                f.write(f"{clave}: {valor}\n")
        f.write("\n" + "-" * 40 + "\n")
        f.write("Desarrollado por zirak9\n")
        f.write("Impulsado por DAVOHOMEHOUSE\n")
        f.write("Con tecnologia VALKYRIE FIRE WIND\n")
    
    shutil.copy2(txt_path, txt_ultimo)
    
    return bitacora_path, json_path, txt_path

def main():
    print("\n" + "="*60)
    print("DocuKit - Documentacion con un solo clic")
    print(f"   Version {CONFIG['version']} - Sin dependencias")
    print("="*60)
    
    ruta = obtener_ruta_proyecto()
    os.chdir(ruta)
    
    tipo = obtener_tipo_proyecto()
    print(f"   Tipo detectado: {tipo.upper()}")
    
    nivel_detalle = obtener_nivel_detalle()
    print(f"   Nivel de detalle: {nivel_detalle}")
    
    print("\nEscaneando archivos...")
    metadatos = escanear_proyecto(ruta, tipo, nivel_detalle)
    print(f"   {metadatos['total_archivos']} archivos encontrados")
    
    datos_formulario = {}
    if not (ruta / "Reportes" / "DOCUFY_DATA_ULTIMO.json").exists():
        print("\nProyecto nuevo - Respondamos lo minimo:")
        datos_formulario = formulario_inteligente(tipo)
    else:
        print("\nDocumentacion existente detectada.")
        actualizar = input("  Quieres actualizar metadatos? (s/N): ").strip().lower()
        if actualizar == "s":
            datos_formulario = formulario_inteligente(tipo)
    
    archivos_filtrados = filtrar_archivos(metadatos, nivel_detalle)
    
    print("\nGenerando documentacion...")
    bitacora, json_data, txt = generar_documentacion(ruta, metadatos, datos_formulario, archivos_filtrados)
    
    print("\nPROYECTO DOCUMENTADO")
    print(f"   Bitacora: {bitacora.name}")
    print(f"   Datos JSON: {json_data.name}")
    print(f"   Resumen: {txt.name}")
    print(f"   Archivos en inventario: {len(archivos_filtrados)} de {metadatos['total_archivos']}")
    
    # Contar reportes existentes
    carpeta_reportes = ruta / "Reportes"
    total_reportes = len(list(carpeta_reportes.glob("BITACORA_*.md")))
    print(f"   Total de reportes historicos: {total_reportes}")
    
    print("\nArchivos en la carpeta 'Reportes/'")
    print("   - BITACORA_ULTIMO.md (siempre el mas reciente)")
    print("   - BITACORA_YYYY-MM-DD_HH-MM.md (historicos)")
    print("   - DOCUFY_DATA_ULTIMO.json")
    print("   - RESUMEN_ULTIMO.txt")
    print("   Listo para usar")
    print("\n---")
    print("Presentado por DAVOHOMEHOUSE")
    print("Tecnologia VALKYRIE FIRE WIND")
    print("Hecho por zirak9")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProceso cancelado por el usuario")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")