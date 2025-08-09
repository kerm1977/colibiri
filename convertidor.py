# -*- coding: utf-8 -*-

# Primero, necesitas instalar las bibliotecas PyPDF2 y tqdm.
# Puedes hacerlo abriendo tu terminal o línea de comandos y ejecutando:
# pip install PyPDF2 tqdm

import json
import PyPDF2
import re
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm # Importamos la biblioteca para la barra de progreso

# Lista de libros para una mejor detección.
LIBROS_BIBLIA = [
    "Génesis", "Éxodo", "Levítico", "Números", "Deuteronomio", "Josué", "Jueces", "Rut",
    "1 Samuel", "2 Samuel", "1 Reyes", "2 Reyes", "1 Crónicas", "2 Crónicas", "Esdras",
    "Nehemías", "Tobías", "Judit", "Ester", "1 Macabeos", "2 Macabeos", "Job", "Salmos",
    "Proverbios", "Eclesiastés", "Cantar de los Cantares", "Sabiduría", "Eclesiástico",
    "Isaías", "Jeremías", "Lamentaciones", "Baruc", "Ezequiel", "Daniel", "Oseas",
    "Joel", "Amós", "Abdías", "Jonás", "Miqueas", "Nahúm", "Habacuc", "Sofonías",
    "Ageo", "Zacarías", "Malaquías", "Mateo", "Marcos", "Lucas", "Juan", "Hechos",
    "Romanos", "1 Corintios", "2 Corintios", "Gálatas", "Efesios", "Filipenses",
    "Colosenses", "1 Tesalonicenses", "2 Tesalonicenses", "1 Timoteo", "2 Timoteo",
    "Tito", "Filemón", "Hebreos", "Santiago", "1 Pedro", "2 Pedro", "1 Juan",
    "2 Juan", "3 Juan", "Judas", "Apocalipsis"
]


def extract_data_from_pdf(pdf_path):
    """
    Extrae el texto de un PDF y lo devuelve como texto completo y como datos estructurados.

    Args:
        pdf_path (str): La ruta al archivo PDF.

    Returns:
        tuple: Una tupla conteniendo (datos_estructurados, texto_completo)
               o (None, None) si hay un error.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: El archivo PDF no se encontró en la ruta: {pdf_path}")
        return None, None

    print(f"\nProcesando el archivo PDF: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            
            full_text = ""
            print("Paso 1 de 2: Extrayendo texto de las páginas...")
            for page in tqdm(pdf_reader.pages, desc="Extrayendo texto", unit="pág"):
                full_text += page.extract_text() or ""
    except Exception as e:
        print(f"No se pudo leer el archivo PDF. Error: {e}")
        return None, None

    print("\nPaso 2 de 2: Analizando y estructurando el contenido...")
    bible_data = {}
    
    # --- LÓGICA DE DETECCIÓN DE LIBROS MEJORADA ---
    # Se asegura de que solo se detecten los títulos de los libros, no las menciones en el texto.
    book_positions = []
    for book in LIBROS_BIBLIA:
        for match in re.finditer(r'\b' + re.escape(book) + r'\b', full_text, re.IGNORECASE):
            # Un título de libro debe estar al principio del archivo o precedido por un salto de línea.
            # Esto evita falsos positivos de menciones de libros en notas o texto.
            if match.start() == 0 or full_text[match.start()-1] in ['\n', '\r']:
                book_positions.append((book, match.start()))

    # Eliminar duplicados y ordenar por posición
    book_positions = sorted(list(set(book_positions)), key=lambda x: x[1])

    if not book_positions:
        print("\nADVERTENCIA: No se encontró ningún libro conocido. El archivo de salida puede estar vacío.")
        return {}, full_text

    print(f"Libros detectados: {[book[0] for book in book_positions]}")

    for i, (book_name, start_pos) in enumerate(book_positions):
        end_pos = book_positions[i + 1][1] if i + 1 < len(book_positions) else len(full_text)
        book_text = full_text[start_pos:end_pos]
        
        bible_data[book_name] = {}
        
        # --- EXPRESIÓN REGULAR DEFINITIVA PARA CAPÍTULOS ---
        # Busca dos patrones: "Libro X" o un número solo en una línea.
        chapter_regex = re.compile(
            r'(?i)\b' + re.escape(book_name) + r'\s+(\d{1,3})\b' + '|' + r'^\s*(\d{1,3})\s*$',
            re.MULTILINE
        )
        
        chapters = list(chapter_regex.finditer(book_text))
        
        if not chapters:
            print(f"ADVERTENCIA: No se encontraron capítulos para el libro: {book_name}")
            continue
        
        print(f"Procesando libro: {book_name} - {len(chapters)} capítulos encontrados.")

        for j, chapter_match in enumerate(chapters):
            chapter_num = chapter_match.group(1) or chapter_match.group(2)
            if not chapter_num or chapter_num in bible_data[book_name]: continue

            bible_data[book_name][chapter_num] = {}
            
            chap_start = chapter_match.end()
            chap_end = chapters[j + 1].start() if j + 1 < len(chapters) else len(book_text)
            chapter_text = book_text[chap_start:chap_end]
            
            # Lógica para Versículos: Divide el texto del capítulo en cada número de versículo.
            verse_splitter = re.compile(r'\n\s*(\d+)\s')
            verse_parts = verse_splitter.split(chapter_text)

            if verse_parts and len(verse_parts) > 1:
                items = verse_parts[1:]
                for k in range(0, len(items), 2):
                    if k + 1 < len(items):
                        verse_num = items[k]
                        verse_text_content = items[k+1].strip().replace('\n', ' ')
                        
                        bible_data[book_name][chapter_num][verse_num] = {
                            "texto": verse_text_content,
                            "notas": ""
                        }

    print("Análisis completado.")
    return bible_data, full_text

def save_as_json(data, path):
    """Guarda los datos estructurados en un archivo JSON."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"¡Éxito! Archivo JSON guardado en: {path}")

def save_as_txt(text, path):
    """Guarda el texto completo en un archivo TXT."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"¡Éxito! Archivo TXT guardado en: {path}")

def save_as_xml(data, path):
    """Guarda los datos estructurados en un archivo XML."""
    root = ET.Element("biblia")
    for book_name, chapters in data.items():
        if not chapters: continue
        book_elem = ET.SubElement(root, "libro", nombre=book_name)
        for chapter_num, verses in chapters.items():
            if not verses: continue
            chapter_elem = ET.SubElement(book_elem, "capitulo", numero=chapter_num)
            for verse_num, verse_data in verses.items():
                verse_elem = ET.SubElement(verse_elem, "versiculo", numero=verse_num)
                text_elem = ET.SubElement(verse_elem, "texto")
                text_elem.text = verse_data["texto"]
                notes_elem = ET.SubElement(verse_elem, "notas")
                notes_elem.text = verse_data["notas"]

    xml_str = ET.tostring(root, 'utf-8')
    parsed_str = minidom.parseString(xml_str)
    pretty_xml_str = parsed_str.toprettyxml(indent="  ")

    with open(path, "w", encoding='utf-8') as f:
        f.write(pretty_xml_str)
    print(f"¡Éxito! Archivo XML guardado en: {path}")

def main():
    """Función principal para ejecutar el convertidor."""
    
    try:
        pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    except FileNotFoundError:
        print("Error: No se pudo acceder al directorio actual.")
        return

    if not pdf_files:
        print("No se encontraron archivos PDF en este directorio.")
        print("Asegúrate de que el script esté en la misma carpeta que tus archivos PDF.")
        return

    print("\nPor favor, selecciona un archivo PDF para convertir:")
    for i, pdf_file in enumerate(pdf_files):
        print(f"  {i + 1}: {pdf_file}")
    
    choice = -1
    while True:
        try:
            choice_str = input(f"\nIntroduce el número del archivo (1-{len(pdf_files)}): ")
            choice = int(choice_str)
            if 1 <= choice <= len(pdf_files):
                break
            else:
                print("Selección fuera de rango. Inténtalo de nuevo.")
        except ValueError:
            print("Por favor, introduce un número válido.")

    input_pdf_file = pdf_files[choice - 1]
    
    output_format = ""
    while output_format not in ["json", "txt", "xml"]:
        output_format = input("¿A qué formato deseas convertir el archivo? (json, txt, xml): ").lower()
        if output_format not in ["json", "txt", "xml"]:
            print("Formato no válido. Por favor, elige entre 'json', 'txt', o 'xml'.")

    structured_data, full_text = extract_data_from_pdf(input_pdf_file)

    if not structured_data and not full_text:
        return

    base_name = os.path.splitext(os.path.basename(input_pdf_file))[0]
    output_file = f"{base_name}.{output_format}"

    try:
        if output_format == "json":
            if not any(structured_data.get(book) for book in structured_data):
                 print("ADVERTENCIA: No se extrajeron datos estructurados, el archivo JSON estará vacío o incompleto.")
            save_as_json(structured_data, output_file)
        elif output_format == "txt":
            save_as_txt(full_text, output_file)
        elif output_format == "xml":
            if not any(structured_data.get(book) for book in structured_data):
                 print("ADVERTENCIA: No se extrajeron datos estructurados, el archivo XML estará vacío o incompleto.")
            save_as_xml(structured_data, output_file)
    except Exception as e:
        print(f"Ocurrió un error durante la conversión a {output_format.upper()}: {e}")

if __name__ == "__main__":
    main()
