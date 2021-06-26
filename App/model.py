﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from os import stat_result
import config as cf
from DISClib.ADT import list as lt
import time
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(type):
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos, adicionalmente, crea una lista vacia para las categorías,
    una lista vacía para las asociaciones video - categoría y una lista vacía
    para los paises. Retorna el catálogo inicializado. Dependiendo el type pasado inicializa
    las listas con ARRAY_LIST o SINGLE_LINKED

    Args:
        type: int -- 1 para cargar los datos en ARRAY_LIST, 2 para cargar los datos en SINGLE_LINKED
    """
    if type == 1:
        lstType = "ARRAY_LIST"
    elif type == 2:
        lstType = "SINGLE_LINKED"
    else:
        raise Exception("Invalid type in model.newCatalog()")
        
    catalog = {
        "videos": None,
        "countries": None,
        "tags": None,
        "categories": None,
    }

    catalog["videos"] = lt.newList(lstType)
    catalog["countries"] = lt.newList(lstType, comparecountry)
    catalog["tags"] = lt.newList(lstType, comparetags)
    catalog["categories"] = lt.newList(lstType, comparecats)

    return catalog


# Funciones para agregar informacion al catalogo

# -- Para cargar categorías
def loadCategory(catalog, category):
    """
    Añade una categoría a la lista de categorías. Inicializa
    lista para referenciar videos en la categoría en category["videos"]
    """
    cat = newCategory(category["id"], category["name"])
    lt.addLast(catalog["categories"], cat)
    

# -- Para añadir videos
def addVideo(catalog, video):
    """
    Añade un video a la lista de videos.
    """
    #Se adiciona el video a la lista de videos
    lt.addLast(catalog["videos"], video)
    #Se obtiene el país del video
    #country = video["country"]
    #Se añade el pais a la lista de paises (incluye asociación
    # país - video)
    #addVidCountry(catalog, country, video)

    #Se obtienen los tags del video
    #tags = getVidTags(video["tags"])
    #Se añaden los tags a la lista de tags (incluye asociación
    # tag - video)
    #for tag in tags:
        #addVidTag(catalog, tag.strip("\" "), video)
    
    #Se obtiene la categoría del video
    #category_id = video["category_id"]
    #Se añade el video a la lista de videos en la categoría
    #addVidCat(catalog, category_id, video)


def getVidTags(tagdStr: str) -> list:
    """
    Devuelve una lista con los tags de un video.
    """
    if tagdStr == "[none]":
        return []
    else:
        return tagdStr.split("|")
    

def addVidCountry(catalog, countryName, video):
    """
    Añade un país a la lista de paises, incluyendo referencia al video
    """
    countries = catalog["countries"]
    poscountry = lt.isPresent(countries, countryName)
    if poscountry > 0:
        country = lt.getElement(countries, poscountry)
    else:
        country = newCountry(countryName)
        lt.addLast(countries, country)
    #lt.addLast(country["videos"], video)


def addVidTag(catalog, tagName, video):
    """
    Añade un tag a la lista de tags. Incluye referencia al video
    """
    tags = catalog["tags"]
    postag = lt.isPresent(tags, tagName)
    if postag > 0:
        tag = lt.getElement(tags, postag)
    else:
        tag = newTag(tagName)
        lt.addLast(tags, tag)
    #lt.addLast(tag["videos"], video)


def addVidCat(catalog, catId, video):
    """
    Añade un video a la lista de videos de una categoría
    """
    categories = catalog["categories"]
    poscat = lt.isPresent(categories, catId)
    if poscat > 0:
        cat = lt.getElement(categories, poscat)
        #lt.addLast(cat["videos"], video)
    else:
        raise Exception("Categories have not been loaded " + 
        "or video category_id not present in category-id.csv")



# Funciones para creacion de datos

def newCategory(catId, catName):
    """
    Crea una estructura para modelar los videos de una
    categoría
    """
    category = {"id": int(catId), "name": catName, "videos": None}
    #category["videos"] = lt.newList("ARRAY_LIST")

    return category


def newCountry(countryName):
    """
    Crea una nueva estructura para modelar los
    videos de un país
    """
    country = {"name": countryName, "videos": None}
    #country["videos"] = lt.newList("ARRAY_LIST")
    
    return country


def newTag(tagName):
    """
    Crea una nueva estructura para modelar los videos
    de un tag
    """
    tag = {"name": tagName, "videos": None}
    #tag["videos"] = lt.newList("ARRAY_LIST")

    return tag


# Funciones de consulta

def mostLiked (catalog,category,country):
    likedvideos=lt.newList()
    vid=catalog['video']
    poscat=lt.isPresent(catalog['category'],category)
    postcount=lt.isPresent(catalog['country'],country)
    if poscat >0 and postcount>0:
       return None
    return None
 #no se como completar la funciion anterior   


    return None

# Funciones utilizadas para comparar elementos dentro de una lista
def comparecountry(countryName, country):
    """
    Compara si un str es igual al nombre de un elemento
    country

    Args:
        countryName: str a comparar con nombre de elemento country
        country: elemento country
    
    Returns:
        0 (int): si son iguales
        -1 (int): si son dieferentes
    """
    if countryName.lower() == country["name"].lower():
        return 0
    return -1


def comparetags(tagName, tag):
    """
    Compara si un str es igual al nombre de un elemento
    tag

    Args:
        countryName: str a comparar con nombre de elemento tag
        country: elemento tag
    
    Returns:
        0 (int): si son iguales
        -1 (int): si son dieferentes
    """
    if tagName.lower() == tag["name"].lower():
        return 0
    return -1


def comparecats(catId, cat):
    """
    Compara un int con el id de un elemento category

    Args:
        countryName: int a comparar con nombre de elemento category
        country: elemento category
    
    Returns:
        1 (int): si int > cat["id"]
        -1 (int): si int < cat["id"]
        0 (int): si son iguales
    """
    if int(catId) > int(cat["id"]):
        return 1
    elif int(catId) < int(cat["id"]):
        return -1
    return 0
    

def cmpVideosByLikes(video1, video2):
    """
    Devuelve verdadero (True) si los likes de video1 son menores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'likes'
    video2: informacion del segundo video que incluye su valor 'likes'
    """
    return int(video1["likes"]) > int(video2["likes"])


def compareviews(video1, video2):
    """
    Devielve verdadero si las vistas del video 1 son mayores a las vistas del video 2

    Args:
    video1: Elemento video que incluye llave "views"
    video2: Elemento video que incluye llave "views"
    """
    return int(video1['views']) > int(video2['views'])


# Funciones de ordenamiento

def srtVidsByLikes(catalog, sampleSize, srtType):
    """
    Ordena los videos del catálogo por likes. La acendencia o
    decendencia del orden depende de la función de comparación
    cmpVideosByLikes().

    Args:
        Catalog -- Catalogo con toda la información de videos
        sampleSize: int -- Número de elementos de la muestra
        srtType: int -- Tipo de algoritmo de ordenamiento:
            1. para selectionsort
            2. insertionsort
            3. shellsort
    
    Returns:
        Tad Lista con los videos ordenados.
    """
    if srtType == 1:
        from DISClib.Algorithms.Sorting import selectionsort as sa
    elif srtType == 2:
        from DISClib.Algorithms.Sorting import insertionsort as sa
    elif srtType == 3:
        from DISClib.Algorithms.Sorting import shellsort as sa
    else:
        raise Exception("Invalid sort type in model.srtVidsByLikes")

    if sampleSize > catalog["videos"]["size"]:
        raise Exception("Invalid sample size. Sample size bigger than video list size. " + 
        "In model.srtVidsByLikes()")
    
    sampleList = lt.subList(catalog["videos"], 0, sampleSize)
    startTime = time.process_time()
    sortedList = sa.sort(sampleList, cmpVideosByLikes)
    stopTime = time.process_time()
    elapsedTime = (stopTime - startTime) * 1000
    return sortedList, elapsedTime
