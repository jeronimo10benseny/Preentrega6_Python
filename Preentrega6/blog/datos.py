import json
import os


def cargar_datos_json(ruta="posts.json"):
    """Lee el archivo JSON y devuelve una lista de diccionarios."""
    if not os.path.exists(ruta):
        return []

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[!] Aviso al leer {ruta}: {e}. Se inicia con lista vacía.")
        return []


def guardar_datos_json(datos_dict, ruta="posts.json"):
    """Guarda una lista de diccionarios en el archivo JSON."""
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos_dict, f, indent=4, ensure_ascii=False)
        return True
    except OSError as e:
        print(f"[!] Error al guardar en {ruta}: {e}")
        return False