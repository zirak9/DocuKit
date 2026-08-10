#!/usr/bin/env python3
# docufy_engine.py - Documentación con un solo clic
# Presentado por DAVOHOMEHOUSE · Tecnología VALKYRIE FIRE WIND · Hecho por zirak9

import os
import json
import datetime
from pathlib import Path
import sys

# ========== CONFIGURACIÓN ==========
CONFIG = {
    "version": "1.0",
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

def escanear_proyecto(ruta, tipo_proyecto):
    """Escanea automáticamente todo el proyecto"""
    metadatos = {
        "nombre_proyecto": ruta.name,
        "fecha_escaneo": datetime.datetime.now().isoformat(),
        "tipo": tipo_proyecto,
        "total_archivos": 0,
        "archivos_por_tipo": {},
        "archivos_por_carpeta": {},
        "ultima_modificacion": None,
        "tamano_total_mb": 0,
        "archivos_recientes": []
    }
    
    limite_reciente = datetime.datetime.now() - datetime.timedelta(days=7)
    
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
            
            mtime = datetime.datetime.fromtimestamp(archivo.stat().st_mtime)
            if not metadatos["ultima_modificacion"] or mtime > metadatos["ultima_modificacion"]:
                metadatos["ultima_modificacion"] = mtime.isoformat()
            
            if mtime > limite_reciente:
                metadatos["archivos_recientes"].append({
                    "nombre": archivo.name,
                    "carpeta": carpeta,
                    "fecha": mtime.strftime("%d/%m/%Y")
                })
            
            metadatos["tamano_total_mb"] += archivo.stat().st_size / (1024 * 1024)
    
    metadatos["tamano_total_mb"] = round(metadatos["tamano_total_mb"], 2)
    metadatos["archivos_recientes"] = metadatos["archivos_recientes"][:10]
    
    return metadatos

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

def generar_documentacion(ruta, metadatos, datos_formulario):
    """Genera la documentación en la carpeta Reportes/"""
    
    carpeta_reportes = ruta / CONFIG["carpeta_reportes"]
    carpeta_reportes.mkdir(exist_ok=True)
    
    # ===== 1. BITÁCORA PRINCIPAL (Markdown) =====
    bitacora_path = carpeta_reportes / "BITACORA_PROYECTO.md"
    
    if bitacora_path.exists():
        backup = bitacora_path.with_suffix(".md.old")
        bitacora_path.rename(backup)
    
    contenido = []
    contenido.append(f"# {metadatos['nombre_proyecto']}")
    contenido.append("")
    contenido.append(f"**Tipo:** {metadatos['tipo'].upper()}")
    contenido.append(f"**Ultima actualizacion:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
    contenido.append("")
    
    contenido.append("## Resumen Automatico")
    contenido.append("")
    contenido.append(f"- **Total de archivos:** {metadatos['total_archivos']}")
    contenido.append(f"- **Tamaño total:** {metadatos['tamano_total_mb']} MB")
    contenido.append(f"- **Ultima modificacion:** {metadatos['ultima_modificacion']}")
    contenido.append("")
    
    if metadatos["archivos_recientes"]:
        contenido.append("### Actividad reciente (ultimos 7 dias)")
        for arch in metadatos["archivos_recientes"]:
            contenido.append(f"- `{arch['nombre']}` ({arch['carpeta']}) - {arch['fecha']}")
        contenido.append("")
    
    contenido.append("### Distribucion de archivos")
    for carpeta, count in sorted(metadatos["archivos_por_carpeta"].items()):
        contenido.append(f"- `{carpeta}/`: {count} archivos")
    contenido.append("")
    
    if datos_formulario:
        contenido.append("## Metadatos del Proyecto")
        for clave, valor in datos_formulario.items():
            label = clave.replace("_", " ").title()
            contenido.append(f"- **{label}:** {valor}")
        contenido.append("")
    
    contenido.append("## Inventario de Activos")
    contenido.append("")
    contenido.append("| Nombre | Tipo | Ubicacion | Ultima modificacion |")
    contenido.append("|--------|------|-----------|-------------------|")
    
    contador = 0
    for archivo in ruta.rglob("*"):
        if archivo.is_file() and not archivo.name.startswith("."):
            if "DocuKit" in str(archivo) or "Reportes" in str(archivo):
                continue
            nombre = archivo.name
            ext = archivo.suffix.upper() or "SIN EXT"
            ubicacion = str(archivo.relative_to(ruta).parent)
            if ubicacion == ".":
                ubicacion = "Raiz"
            fecha = datetime.datetime.fromtimestamp(archivo.stat().st_mtime).strftime("%d/%m/%Y")
            contenido.append(f"| {nombre} | {ext} | {ubicacion} | {fecha} |")
            contador += 1
            if contador >= 15:
                contenido.append(f"| ... y {metadatos['total_archivos'] - 15} archivos mas | | | |")
                break
    
    contenido.append("")
    contenido.append("---")
    contenido.append(f"*Documentacion generada por DocuKit v{CONFIG['version']} - {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}*")
    contenido.append("")
    contenido.append("---")
    contenido.append("*Presentado por DAVOHOMEHOUSE · Tecnologia VALKYRIE FIRE WIND · Hecho por zirak9*")
    
    with open(bitacora_path, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))
    
    # ===== 2. JSON =====
    json_path = carpeta_reportes / "DOCUFY_DATA.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadatos": metadatos,
            "formulario": datos_formulario,
            "timestamp": datetime.datetime.now().isoformat(),
            "version": CONFIG["version"],
            "branding": {
                "presentado": "DAVOHOMEHOUSE",
                "tecnologia": "VALKYRIE FIRE WIND",
                "creador": "zirak9"
            }
        }, f, indent=2, ensure_ascii=False)
    
    # ===== 3. TXT simple =====
    txt_path = carpeta_reportes / "RESUMEN_PROYECTO.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"PROYECTO: {metadatos['nombre_proyecto']}\n")
        f.write(f"TIPO: {metadatos['tipo'].upper()}\n")
        f.write(f"FECHA: {datetime.datetime.now().strftime('%d/%m/%Y')}\n")
        f.write(f"ARCHIVOS: {metadatos['total_archivos']}\n")
        f.write(f"TAMAÑO: {metadatos['tamano_total_mb']} MB\n")
        f.write("-" * 40 + "\n")
        if datos_formulario:
            for clave, valor in datos_formulario.items():
                f.write(f"{clave}: {valor}\n")
        f.write("\n" + "-" * 40 + "\n")
        f.write("Presentado por DAVOHOMEHOUSE\n")
        f.write("Tecnologia VALKYRIE FIRE WIND\n")
        f.write("Hecho por zirak9\n")
    
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
    
    print("\nEscaneando archivos...")
    metadatos = escanear_proyecto(ruta, tipo)
    print(f"   {metadatos['total_archivos']} archivos encontrados")
    
    datos_formulario = {}
    if not (ruta / "Reportes" / "DOCUFY_DATA.json").exists():
        print("\nProyecto nuevo - Respondamos lo minimo:")
        datos_formulario = formulario_inteligente(tipo)
    else:
        print("\nDocumentacion existente detectada.")
        actualizar = input("  Quieres actualizar metadatos? (s/N): ").strip().lower()
        if actualizar == "s":
            datos_formulario = formulario_inteligente(tipo)
    
    print("\nGenerando documentacion...")
    bitacora, json_data, txt = generar_documentacion(ruta, metadatos, datos_formulario)
    
    print("\nPROYECTO DOCUMENTADO")
    print(f"   Bitacora: {bitacora}")
    print(f"   Datos JSON: {json_data}")
    print(f"   Resumen: {txt}")
    print("\nArchivos en la carpeta 'Reportes/'")
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
        input("\nPresiona Enter para salir...")