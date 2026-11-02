from blog.datos import cargar_datos_json, guardar_datos_json


class PostInvalidoError(Exception):
    """Excepción para reglas de negocio del Blog."""
    pass


class Autor:
    def __init__(self, nombre, bio="Sin biografía", email="autor@blog.com"):
        self.nombre = nombre
        self.bio = bio
        self.email = email

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "email": self.email
        }

    @classmethod
    def de_dict(cls, data):
        if isinstance(data, dict):
            return cls(
                nombre=data.get("nombre", "Anónimo"),
                bio=data.get("bio", "Sin biografía"),
                email=data.get("email", "autor@blog.com")
            )
        return cls(nombre=str(data))

    def __str__(self):
        return f"{self.nombre} ({self.bio})"


class Post:
    def __init__(self, titulo, contenido, autor, tags=None, likes=0, estado="publicado", id=None):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        
        if isinstance(autor, Autor):
            self.autor = autor
        elif isinstance(autor, dict):
            self.autor = Autor.de_dict(autor)
        else:
            self.autor = Autor(nombre=str(autor))

        self.tags = tags if tags is not None else []
        self.likes = likes
        self.estado = estado

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, nuevo_titulo):
        if not str(nuevo_titulo).strip():
            raise PostInvalidoError("El título del post no puede estar vacío.")
        self._titulo = str(nuevo_titulo).strip()

    @property
    def likes(self):
        return self._likes

    @likes.setter
    def likes(self, nuevo_valor):
        if not isinstance(nuevo_valor, int) or nuevo_valor < 0:
            raise PostInvalidoError("Los likes deben ser un entero mayor o igual a 0.")
        self._likes = nuevo_valor

    def dar_like(self):
        self.likes += 1

    def a_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.a_dict(),
            "tags": self.tags,
            "likes": self.likes,
            "estado": self.estado,
            "es_destacado": False
        }

    @classmethod
    def de_dict(cls, data):
        return cls(
            id=data.get("id"),
            titulo=data.get("titulo", "Sin Título"),
            contenido=data.get("contenido", ""),
            autor=Autor.de_dict(data.get("autor", "Anónimo")),
            tags=data.get("tags", []),
            likes=data.get("likes", 0),
            estado=data.get("estado", "publicado")
        )

    def __str__(self):
        return f"[{self.estado.upper()}] '{self.titulo}' por {self.autor.nombre} | Likes: {self.likes}"


class PostDestacado(Post):
    def __init__(self, titulo, contenido, autor, badge="⭐ DESTACADO", tags=None, likes=0, estado="publicado", id=None):
        super().__init__(titulo, contenido, autor, tags, likes, estado, id)
        self.badge = badge

    def dar_like(self):
        self.likes += 2

    def a_dict(self):
        data = super().a_dict()
        data["es_destacado"] = True
        data["badge"] = self.badge
        return data

    def __str__(self):
        return f"[{self.badge}] {super().__str__()}"


class Blog:
    def __init__(self, archivo_ruta="posts.json"):
        self.archivo_ruta = archivo_ruta
        self.posts = []
        self.cargar_desde_json()

    def cargar_desde_json(self):
        raw_data = cargar_datos_json(self.archivo_ruta)
        self.posts = []
        for item in raw_data:
            if item.get("es_destacado"):
                post_obj = PostDestacado.de_dict(item)
            else:
                post_obj = Post.de_dict(item)
            self.posts.append(post_obj)

    def guardar_en_json(self):
        datos_dict = [post.a_dict() for post in self.posts]
        return guardar_datos_json(datos_dict, self.archivo_ruta)

    def listar_posts(self):
        return self.posts

    def buscar_por_titulo(self, termino):
        termino_clean = termino.lower().strip()
        return [p for p in self.posts if termino_clean in p.titulo.lower()]

    def filtrar_por_tag(self, tag):
        tag_clean = tag.lower().strip()
        return [p for p in self.posts if any(tag_clean == t.lower() for t in p.tags)]

    def agregar_post(self, post_obj):
        if not isinstance(post_obj, Post):
            raise PostInvalidoError("Objeto no válido. Debe ser una instancia de Post.")
        post_obj.id = len(self.posts) + 1
        self.posts.append(post_obj)

    def validar_posts(self):
        reporte = []
        for p in self.posts:
            es_valido = bool(p.titulo and p.contenido and p.autor.nombre)
            reporte.append({"titulo": p.titulo, "valido": es_valido})
        return reporte