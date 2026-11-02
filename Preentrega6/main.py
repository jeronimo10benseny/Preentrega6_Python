from blog.modelos import Autor, Blog, Post, PostInvalidoError


def mostrar_menu():
    print("\n--- MENU DEL BLOG (PREENTREGA 6) ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Crear nuevo post")
    print("5. Validar posts")
    print("6. Guardar posts en JSON")
    print("7. Salir")


def ejecutar():
    blog = Blog(archivo_ruta="posts.json")
    print(f"[SYSTEM] Preentrega6 iniciada. {len(blog.listar_posts())} posts cargados desde posts.json.")

    while True:
        mostrar_menu()
        opcion = input("Seleccioná una opción (1-7): ").strip()

        if opcion == "1":
            posts = blog.listar_posts()
            print("\n=== TODOS LOS POSTS ===")
            if not posts:
                print("No hay posts en el blog.")
            else:
                for idx, p in enumerate(posts, 1):
                    print(f"{idx}. {p}")

        elif opcion == "2":
            termino = input("Ingresá el título a buscar: ")
            resultados = blog.buscar_por_titulo(termino)
            print(f"\n=== RESULTADOS DE BÚSQUEDA ('{termino}') ===")
            if not resultados:
                print("No se encontraron coincidencias.")
            else:
                for p in resultados:
                    print(f"• {p}")

        elif opcion == "3":
            tag = input("Ingresá el tag a filtrar: ")
            resultados = blog.filtrar_por_tag(tag)
            print(f"\n=== POSTS CON TAG '{tag}' ===")
            if not resultados:
                print("No se encontraron posts con ese tag.")
            else:
                for p in resultados:
                    print(f"• {p}")

        elif opcion == "4":
            print("\n=== CREAR NUEVO POST ===")
            try:
                titulo = input("Título: ").strip()
                contenido = input("Contenido: ").strip()
                nombre_autor = input("Nombre del Autor: ").strip()
                bio_autor = input("Biografía del Autor: ").strip()
                tags_str = input("Tags (separados por coma): ").strip()

                tags = [t.strip() for t in tags_str.split(",") if t.strip()]
                autor_obj = Autor(nombre=nombre_autor, bio=bio_autor if bio_autor else "Redactor")

                nuevo_post = Post(
                    titulo=titulo,
                    contenido=contenido,
                    autor=autor_obj,
                    tags=tags
                )

                blog.agregar_post(nuevo_post)
                print(f"[+] Post '{nuevo_post.titulo}' creado exitosamente en memoria.")
            except PostInvalidoError as e:
                print(f"[!] Error de validación: {e}")
            except Exception as e:
                print(f"[!] Error inesperado: {e}")

        elif opcion == "5":
            print("\n=== VALIDACIÓN DE POSTS ===")
            reporte = blog.validar_posts()
            if not reporte:
                print("No hay posts para validar.")
            else:
                for r in reporte:
                    estado = "OK" if r["valido"] else "CON ERRORES"
                    print(f"• [{estado}] {r['titulo']}")

        elif opcion == "6":
            if blog.guardar_en_json():
                print("[+] Posts guardados exitosamente en 'posts.json'.")

        elif opcion == "7":
            print("Guardando cambios antes de salir...")
            blog.guardar_en_json()
            print("¡Hasta luego!")
            break

        else:
            print("[!] Opción inválida. Ingresá un número del 1 al 7.")


if __name__ == "__main__":
    ejecutar()