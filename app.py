from fastapi import FastAPI, HTTPException

#Validación de datos, creando un modelo base
from pydantic import BaseModel 

from datetime import date, datetime

#tipo de dato text
from typing import Text, Optional

# IDs unicos
from uuid import uuid4 as uuid

app = FastAPI()

# Arreglo donde guarda el ultimo dato cargado, si se crea otro lo pisa
posts = []

# Post Model
class Post(BaseModel):
    id:Optional[str]
    title:str
    author:str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False #False por default


@app.get("/") # Ruta inicial
def road_root():
    return {'welcome':'welcome to my REST API'}


@app.get('/posts') # Base de datos en el que vamos guardando los posts
def get_posts():
    return posts

# Vemos que al ir cargando muchas publicaciones pero no se guargan todas, solo la ultima
# Por eso es recomendable utilizar una base de datos.

@app.post('/posts')
def save_post(post:Post):
    post.id = str(uuid())
    # result = uuid()
    # print(type(result)) es una clase lo convertimos en str
    posts.append(post.dict())
    return posts[-1] #nos devuelve el ultimo añadido

# ERROR 422 SIGNIFICA UN ERROR EN EL JSON/DIC
# Fijarse en el vinculo/docs

@app.get('/posts/{post_id}')
def get_post(post_id:str):
    for p in posts:
        if p['id'] == post_id:
            return p
    raise HTTPException(status_code=404, detail='Post Not Found')

# RAISE para errores al cargar un dato

@app.delete('/posts/{post_id}')
def delete_post(post_id:str):
    for index, p in enumerate(posts):
        if p['id'] == post_id:
            posts.pop(index)
            return {'Mensaje': 'La publicacion se ha eliminado exitosamente'}
    raise HTTPException(status_code=404, detail='Post Not Found')

# posts= [{1},{2},{3}], si quito el 2
# Deberia actualizar los id, quedaria
# posts= [{1},{2}]

@app.put('/posts/{post_id')
def update_post(post_id:str, updatePost:Post):
    for index, p in enumerate(posts):
        if p['id'] == post_id:
            posts[index]['title'] = updatePost.title
            posts[index]['content'] = updatePost.content
            posts[index]['author'] = updatePost.author
            return {'Mensaje': 'El post se actualizo exitosamente'}
    raise HTTPException(status_code=404, detail='Post Not Found')
