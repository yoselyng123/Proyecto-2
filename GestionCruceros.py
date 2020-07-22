import requests
import pickle
# Object Crucero
class Crucero:
    def __init__(self, name, route, departure_date, ticket_price, rooms, rooms_capacity, menu):
        self.name = name
        self.route = route
        self.departure_date = departure_date
        self.ticket_price = ticket_price
        self.rooms = rooms
        self.rooms_capacity = rooms_capacity
        # NO TOCAR
        self.menu = menu
        self.menu_combos = []
        # FIN
        self.num_pisos = 3
        self.pisos = []
# Access the information from the API
def api_saman_caribbean():
    """Recolecta la informacion de la API

    Returns:
        [dict]: [Data de la API]
    """
    url = 'https://saman-caribbean.vercel.app/api/cruise-ships'

    response = requests.request("GET", url)

    return response.json()
# Creates 4 Objects (Crucero)
def create_cruceros():
    """Crea una lista con los objetos Crucero

    Returns:
        [list]: [Lista de Cruceros]
    """
    data = api_saman_caribbean()
    cruceros = []
    for i in range(len(data)):
        c = Crucero(data[i]['name'], data[i]['route'], data[i]['departure'], data[i]['cost'], data[i]['rooms'], data[i]['capacity'], data[i]['sells'])
        cruceros.append(c)
    return cruceros
# Creates a file with the data from the cruceros
def create_file(cruceros):
    """Crea un archivo nuevo con los datos de los cruceros

    Args:
        cruceros ([list]): [List of objects]

    Returns:
        [bool]: [when the file is created returns True]
    """
    data = open('Cruceros', 'wb')
    pickle.dump(cruceros, data)
    data.close()
    del data
    return True
# Reads the existing file of Crucero
def read_file():
    """Reads the Crucero File

    Returns:
        [list]: [List of objects]
    """
    try:
        data = open('Cruceros', 'rb')
        cruceros = pickle.load(data)
        data.close()
        return cruceros
    except:
        return False
# Creates the file if the file does not exist, Reads the file and updates it if the file already exists.
def main():
    if read_file():
        print('Reading...')
        cruceros = read_file()
        # Linea en donde se modifiquen los datos de crucero y luego se actualiza
        data = open('Cruceros', 'wb')
        pickle.dump(cruceros, data)
        data.close()
    else:
        print('Creating file...')
        cruceros = create_cruceros()
        create_file(cruceros)
    
main()