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
    if (catName.lower() == cat["name"].lower()):
        return 0
    return 1


def cmpVideos(videoName: str, video) -> int:
    """
    Compara un str con el nombre de un elemento video

    Args:
        videoName: str -- str a comparar con el nombre del elemento category
        video: elemento video
    
    Returns:
        0 (int): si el str es igual al nombre del video
        -1 (int): si son diferentes  
    """
    if (videoName.lower() == video["name"].lower()):
        return 0
    return -1
    

def cmpVideosByLikes(video1, video2):
    """
    Devuelve verdadero (True) si los likes de video1 son menores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'likes'
    video2: informacion del segundo video que incluye su valor 'likes'
    """
    return int(video1["likes"]) > int(video2["likes"])


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
