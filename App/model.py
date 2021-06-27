"""
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
from DISClib.Algorithms.Sorting import mergesort as sa
import sys

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
        "categories": None,
    }

    catalog["videos"] = lt.newList(lstType)
    catalog["categories"] = lt.newList(lstType, cmpCats)

    return catalog


# Funciones para agregar informacion al catalogo

# -- Para cargar categorías
def loadCategory(catalog, category):
    """
    Añade una categoría a la lista de categorías.
    """
    lt.addLast(catalog["categories"], category)
    

# -- Para añadir videos
def addVideo(catalog, video):
    """
    Añade un video a la lista de videos.
    """
    lt.addLast(catalog["videos"], video)

# Funciones para creacion de datos

# Funciones de consulta

def catPos(catalog, catName: str) -> int:
    """
    Revisa si una categoría está presente en la lista de categorías del catálogo.
    Devuelve la posición en la que se encuentra.

    Args:
        catalog: Catalogo de videos.
        catName: str -- nombre de la categoría.
    
    Returns:
        Si encuentra la categoría devuelve su posición (int). Si no la encuentra
        devuelve 0 (int).
    """
    return lt.isPresent(catalog["categories"], catName)


def trendingVidCat(catalog, catPos):
    """
    Retorna el video de una categoría específica, cuya persepción es sumamente positiva
    (ratio likes/dislikes > 20) que más días ha sido trending.

    Args:
        catalog -- catalogo de videos
        catPos -- posición de la categoría en la lista de categorías

    Returns:
        Elemento video
        False (bool) -- Si no se encontró ningún video que cumpla con las condiciones
    """
    if catPos <= 0:
        raise Exception("Invalid catPos in model.trendingVidCat()")
    
    categoryID = lt.getElement(catalog["categories"], catPos)["id"]
    hiPerVids = lt.newList("ARRAY_LIST", cmpVideos) #hiPerVids hace referencia a hi perception videos
    #Recorrer todos los videos del catalogo para ver encontrar
    #los videos en la categoría especificada y con persepción
    #sumamente positiva
    for pos in range(1, catalog["videos"]["size"]):
        video = lt.getElement(catalog["videos"], pos)
        #Evitar división por 0
        if int(video["dislikes"]) == 0:
            likeDislikeRatio == 30
        else:
            likeDislikeRatio = int(video["likes"]) / int(video["dislikes"])
        #Revisar si el video cumple los criterios
        if (video["category_id"] == categoryID) and likeDislikeRatio > 20:
            #Revisar si el video ya existe en trendVids
            hiPerVidPos = lt.isPresent(hiPerVids, video["title"])
            if hiPerVidPos > 0:
                hiPerVid = lt.getElement(hiPerVids, hiPerVidPos)
                #Añade 1 a la cuenta de días que ha aparecido el video
                hiPerVid["day_count"] += 1
            else:
                hiPerVid = {
                    "title": video["title"],
                    "channel_title": video["channel_title"],
                    "category_id": video["category_id"],
                    "ratio_likes_dislikes": likeDislikeRatio,
                    "day_count": 1
                    }
                lt.addLast(hiPerVids, hiPerVid)
    
    #Revisa si hay videos que cumplen con la condición
    if lt.isEmpty(hiPerVids):
        return False
    #Ordena los hiPerVids
    sa.sort(hiPerVids, cmpVideosByTrendDays)
    #Retorna el video que más días ha sido trend
    return lt.firstElement(hiPerVids)

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpCats(catName: str, cat) -> int:
    """
    Compara un str con el nombre de un elemento category

    Args:
        catName: str a comparar con nombre de elemento category
        cat: elemento category
    
    Returns:
        0 (int): si el str es igual al nombre de la categoría
        -1 (int): si son diferentes
    """
    if (catName.lower() in cat["name"].lower()):
        return 0
    return -1


def cmpVideos(videoTitle, video) -> int:
    """
    Compara un str con el nombre de un elemento video

    Args:
        videoTitle: str a comparar
        video: elemento video a comparar
    
    Returns:
        0 (int): si el str es igual al id del elemento video
        -1 (int): si son diferentes  
    """
    if (videoTitle == video["title"]):
        return 0
    return -1
    

def cmpVideosByLikes(video1, video2):
    """
    Devuelve verdadero (True) si los likes de video1 son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'likes'
    video2: informacion del segundo video que incluye su valor 'likes'
    """
    return int(video1["likes"]) > int(video2["likes"])


def cmpVideosByTrendDays(video1, video2):
    """
    Devuelve verdadero (True) si los días de tendencia del video 1 son MAYORES que los del video 2
    CUIDADO: los elementos video1 y video2 no son elementos video del catalogo de videos
    deben tener una llave "day_count": int. Ver función trendingVidCat()

    Args:
        video1: información del video 1 que incluye llave day_count
        video2: información del video 2 que incluye llave day_count
    """
    return int(video1["day_count"]) > int(video2["day_count"])


def cmpVideosByViews(video1, video2):
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
            4. quicksort
            5. mergesort
    
    Returns:
        Tad Lista con los videos ordenados.
    """
    if srtType == 1:
        from DISClib.Algorithms.Sorting import selectionsort as sa
    elif srtType == 2:
        from DISClib.Algorithms.Sorting import insertionsort as sa
    elif srtType == 3:
        from DISClib.Algorithms.Sorting import shellsort as sa
    elif srtType == 4:
        from DISClib.Algorithms.Sorting import quicksort as sa
    elif srtType == 5:
        from DISClib.Algorithms.Sorting import mergesort as sa
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
