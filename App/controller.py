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
 """

import config as cf
import model
import csv
from mtTrace import mtTrace


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de videos

def initCatalog(type):
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    trace = mtTrace()
    catalog = model.newCatalog(type)
    trace = trace.stop()
    return catalog, trace

    
# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    trace = mtTrace()
    loadCategories(catalog)
    loadVideos(catalog)
    trace = trace.stop()
    return trace


def loadCategories(catalog):
    catfile = cf.data_dir + "Videos/category-id.csv"
    input_file = csv.DictReader(open(catfile,encoding='utf-8'), delimiter="\t")
    for category in input_file:
        model.loadCategory(catalog, category)

def loadVideos(catalog):
    # TODO Cambiar a videos-large.csv para producción
    vidsfile = cf.data_dir + "Videos/videos-large.csv"
    input_file = csv.DictReader(open(vidsfile,encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)

# Funciones de ordenamiento
def srtVidsByLikes(catalog, srtType):
    """
    Llama a la función sortVidsByLikes del model.py
    """
    return model.srtVidsByLikes(catalog, srtType)


# Funciones de consulta sobre el catálogo

def catPos(catalog, catName):
    """
    Llama a la función catPos del model.py
    """
    return model.catPos(catalog, catName)


def trendingVidCat(catalog, catPos):
    """
    Llama a la función model.trendingVidCat()
    """
    trace = mtTrace()
    video = model.trendingVidCat(catalog, catPos)
    trace = trace.stop()
    return video, trace


def topVidsCatCountry(catalog, catPos, countryName, topN):
    """
    Llama a la función topVidsCatCountry del model.py
    """
    trace = mtTrace()
    video = model.topVidsCatCountry(catalog, catPos, countryName,
    topN)
    trace = trace.stop()
    return video, trace


def mostCommentedVids(catalog, country, tagName, topN):
    """
    Llama a la función model.mostCommentedVids()
    """
    trace = mtTrace()
    video = model.mostCommentedVid(catalog, country, tagName, topN)
    trace = trace.stop()
    return video, trace


def trendingVidCountry(catalog, country):
    """
    Llama a la función model.trendingVidCountry()
    """
    trace = mtTrace()
    video = model.trendingVidCountry(catalog, country)
    trace = trace.stop()
    return video, trace