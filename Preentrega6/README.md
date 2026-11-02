# Blog Consola - Refactorización a POO y Persistencia JSON (Preentrega 6)

Sistema interactivo para consola desarrollado en Python 3.12, refactorizado hacia Programación Orientada a Objetos (POO) con persistencia de datos en formato JSON.

## Estructura del Proyecto

```text
blog_proyecto/
├── main.py            # Punto de entrada interactivo
├── posts.json         # Archivo de persistencia de datos
├── README.md          # Documentación del proyecto
└── blog/
    ├── __init__.py    # Inicializador del paquete
    ├── datos.py       # Carga y guardado en JSON
    └── modelos.py     # Clases Autor, Post, PostDestacado, Blog y excepciones