"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Top N videos con más likes tendencia en país - categoría")
    print("3- Vídeo que más días ha sido trending en un país")
    print("4- Video que más días ha sido trending en una categoría")
    print("5- N videos con más comentarios en país")


def initCatalog():
    """
    Inicializa el catálogo de videos
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los datos de los videos
    """
    return controller.loadData(catalog)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorías cargadas: ' + str(lt.size(catalog['category'])))

    elif int(inputs[0]) == 2:
        number = input("Buscar los TOP ?: ")
        country = input("Buscar en país: ")
        category = input("Buscar en categoría: ")
        videos = controller.topVidCountryCat(number, pais, categoria)
        print(videos)
    
    elif int(inputs[0]) == 3:
        country = input("Buscar en país: ")
        videos = controller.trendingVidCountry(country)
        print(videos)

    elif int(inputs[0]) == 4:
        category = input("Buscar en categoría: ")
        videos = controller.trendingVidCat(category)
        print(videos)

    elif int(inputs[0]) == 5:
        country = input("Buscar en país: ")
        number = input("Número de videos a listar: ")
        tag = input("Etiqueta (tag) a buscar: ")
        videos = controller.mostCommentedVid(country, number, tag)
        print(videos)

    else:
        sys.exit(0)
sys.exit(0)
