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


from DISClib.DataStructures.arraylist import newList
from os import stat_result
import config as cf
from DISClib.ADT import list as lt
import time
assert cf
from DISClib.Algorithms.Sorting import mergesort as sa
import sys
import re #Regular expression

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
    for video in lt.iterator(catalog["videos"]):
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
    srtVidsByTrendDays(hiPerVids)
    #Retorna el video que más días ha sido trend
    return lt.firstElement(hiPerVids)


def topVidsCatCountry(catalog, catPos, countryName, topN):
    """
    Retorna el top N videos de una categoría y un país con más likes

    Args:
        catalog -- Catálogo de videos
        catPos: int -- Posición de la categoría en catalog["categories"]
        countryName: str -- nombre del país en el cual buscar
        topN: int -- Númerod de videos a listar en el top

    Returns:
        Tad lista con el top de videos ordenados de más a menos likes
    """
    catCountryVids = lt.newList("ARRAY_LIST")
    #Get Category Id
    catId = lt.getElement(catalog["categories"], catPos)["id"]
    #Iteración por todos los videos
    for video in lt.iterator(catalog["videos"]):
        if (countryName.lower() in video["country"].lower()) and (video["category_id"] == catId):
            lt.addLast(catCountryVids, video)
    #Ordenamiento de videos
    srtVidsByLikes(catCountryVids)
    if topN > catCountryVids["size"]:
        topN = catCountryVids["size"]
        
    return lt.subList(catCountryVids, 1, topN)


def mostCommentedVid(catalog, countryName: str, tagName: str, topN: int):
    """
    Devuelve los n videos DIFERENTES de un país específico y
    que tengan un tag específico.

    Args:
        catalog -- Catálogo de videos
        countryName: str -- nombre de el país
        tagName: str -- nombre del tag
        topN: int -- número de videos a listar en el top

    Retorna:
        Tad lista con el top n videos ordenados de más a menos
        comentarios
    """
    tagCountryVids = lt.newList("ARRAY_LIST")
    difTagCountryVids = lt.newList("ARRAY_LIST", cmpVideos)
    #Iteración por todos los videos para encontrar los que cumplen
    #el filtro
    #RegEx para tags
    tagRegEx = "(?i)\"" + tagName + "\""
    for video in lt.iterator(catalog["videos"]):
        if (countryName.lower() in video["country"].lower() and
        not(re.search(tagRegEx, video["tags"]) is None)):
            lt.addLast(tagCountryVids, video)
    #Ordena los videos por número de comentarios
    srtVidsByComments(tagCountryVids)
    #Selecciona los n videos diferentes
    for video in lt.iterator(tagCountryVids):
        if difTagCountryVids["size"] == topN:
            break
        if lt.isPresent(difTagCountryVids, video["title"]) == 0:
            lt.addLast(difTagCountryVids, video)
    
    return difTagCountryVids


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


def cmpVideosByLikes(video1, video2) -> bool:
    """
    Devuelve verdadero (True) si los likes de video1 son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'likes'
    video2: informacion del segundo video que incluye su valor 'likes'
    """
    return int(video1["likes"]) > int(video2["likes"])


def cmpVideosByTrendDays(video1, video2) -> bool:
    """
    Devuelve verdadero (True) si los días de tendencia del video 1 son MAYORES que los del video 2
    CUIDADO: los elementos video1 y video2 no son elementos video del catalogo de videos
    deben tener una llave "day_count": int. Ver función trendingVidCat()

    Args:
        video1: información del video 1 que incluye llave day_count
        video2: información del video 2 que incluye llave day_count
    """
    return int(video1["day_count"]) > int(video2["day_count"])


def cmpVideosByViews(video1, video2) -> bool:
    """ 
    Devielve verdadero si las vistas del video 1 son mayores a las vistas del video 2

    Args:
    video1: Elemento video que incluye llave "views"
    video2: Elemento video que incluye llave "views"
    """
    return int(video1['views']) > int(video2['views'])


def cmpVideosByComments(video1, video2) -> bool:
    """
    Devuleve verdadero (true) se el número de comentarios del video1 es MAYOR
    al número de comentarios del video 2.

    Args:
        video1 -- información del video 1 que incluye llave comment_count
        video2 -- información del video 2 que incluye llave comment_count
    """
    return int(video1["comment_count"]) > int(video2["comment_count"])

# Funciones de ordenamiento

def srtVidsByLikes(lst):
    """
    Ordena los videos del catálogo por likes. La acendencia o
    decendencia del orden depende de la función de comparación
    cmpVideosByLikes(). Utiliza la función de ordenamiento importada
    como "sa"

    Args:
        lst -- Lista con elementos video a ordenar
    
    Returns:
        Tad Lista con los videos ordenados.
    """
    startTime = time.process_time()
    sortedList = sa.sort(lst, cmpVideosByLikes)
    stopTime = time.process_time()
    elapsedTime = (stopTime - startTime) * 1000

    return sortedList, elapsedTime


def srtVidsByTrendDays(lst):
    """
    Ordena los videos por días de trend. Retorna la lista ordenada
    La acendencia o decendencia del ordenamiento depende de la
    función cmpVideosByTrendDays().
    ADVERTENCIA: los elementos video1 y video2 NO son elementos video del
    catalogo de videos deben tener una llave "day_count": int.
    Ver función trendingVidCat()

    Args:
        lst -- lista con elementos video que tienen la llave day_count
    """
    return sa.sort(lst, cmpVideosByTrendDays)


def srtVidsByComments(lst):
    """
    Ordena los videos por número de comentarios. Retorna la lista ordenada.
    La acendencia o decedencia del ordenamiento depende de la función
    cmpVidsByComments(). Utiliza el algoritmo de ordenamiento importado
    como "sa".

    Args:
        lst -- lista con elementos video que tienen la llave "comment_count"
    """
    return sa.sort(lst, cmpVideosByComments)

def ratio_likes_dislikes(likes,dislikes):
    
    if float(dislikes)>0:
        x=(float(float(likes))/(float(dislikes)))
    else:
        x=0
    return x

def trendingVidCountrys(catalog,country):
    """""
  
    ans={}
    i=0
    
    while i < lt.size(catalog['videos']):
        video=lt.getElement(catalog['videos'],i)
        likes=video['likes']
        dislikes=video['dislikes']
        video_name=video['title']
        channel=video['channel_title']
        pais=video['country']
        if video_name not in ans and ratio_likes_dislikes(likes,dislikes)>10 and pais==country:
            newdict={}
            newdict['ratio_likes_dislikes']=ratio_likes_dislikes(likes,dislikes)
            newdict['channel_title']=channel
            newdict['country']=pais
            newdict['dias']=1
            ans[video_name]=newdict
        if video_name in ans and ratio_likes_dislikes(likes,dislikes)>10 and pais==country:
            newdict=ans[video_name]
            newdict['dias']+=1
            newdict['ratio_likes_dislikes']=ratio_likes_dislikes(likes,dislikes)
            
        i+=1
    dias=0
    title=0
    channel_title=0
    ratio=0

    for x in ans.keys():
        newdict=ans[x]
        if newdict['dias']>dias and newdict['ratio_likes_dislikes']>ratio:
            dias=newdict['dias']
            title=x
            channel_title=newdict['channel_title']
            ratio=newdict['ratio_likes_dislikes']

   
    return title,channel_title,ratio,dias
  """
    i=0
    video= lt.getElement(catalog["video"],i)
    hiPerVids = lt.newList("ARRAY_LIST", cmpVideos) #hiPerVids hace referencia a hi perception videos
    #Recorrer todos los videos del catalogo para ver encontrar
    #los videos en la categoría especificada y con persepción
    #sumamente positiva
    for video in lt.iterator(catalog["videos"]):
        #Evitar división por 0
        if int(video["dislikes"]) == 0:
            likeDislikeRatio == 30
        else:
            likeDislikeRatio = int(video["likes"]) / int(video["dislikes"])
        #Revisar si el video cumple los criterios
        if (video["country"] == country) and likeDislikeRatio > 10:
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
                    "country": video["country"],
                    "ratio_likes_dislikes": likeDislikeRatio,
                    "day_count": 1
                    }
                lt.addLast(hiPerVids, hiPerVid)
    #Revisa si hay videos que cumplen con la condición
    if lt.isEmpty(hiPerVids):
        return False
    #Ordena los hiPerVids
    srtVidsByTrendDays(hiPerVids)
    #Retorna el video que más días ha sido trend
    return lt.firstElement(hiPerVids)
