import requests
import pickle
from GestionCruceros import Crucero, read_file

class Cliente:
    def __init__(self, name, dni, age, disability):
        self.name = name
        self.dni = dni
        self.age = age
        self.disability = disability == True
        self.rooms = []

class Piso:
    def __init__(self, num_piso, piso_type, num_rooms, num_pasillos):
        self.num_piso = num_piso
        self.piso_type = piso_type
        self.num_rooms = num_rooms
        self.num_pasillos = num_pasillos
        self.pasillos = []
        self.rooms = []

class Pasillo:
    def __init__(self, name, num_rooms, pasillo_type):
        self.name = name
        self.num_rooms = num_rooms
        self.pasillo_type = pasillo_type

class Room:
    def __init__(self, name, capacity, room_price):
        self.name = name
        self.capacity = capacity
        self.room_price = room_price
        self.available = True
        self.room_service = False
        self.view_to_sea = False
        self.private_party = False
        self.clients = []

    def ocupy_room(self):
        self.available = False
    def desocupy_room(self):
        self.available = True

class Sencilla(Room):
    def __init__(self, name, capacity, room_price):
        super().__init__(name,capacity, room_price)
        self.room_service = True

class Premium(Room):
    def __init__(self, name, capacity, room_price):
        super().__init__(name, capacity, room_price)
        self.view_to_sea = True

class Vip(Room):
    def __init__(self, name, capacity, room_price):
        super().__init__(name, capacity, room_price)
        self.private_party = True


def create_piso(cruceros):
    piso_type = ['simple', 'premium', 'vip']
    pisos = []
    for crucero in cruceros:
        c = []
        for i in range(3): 
            num_rooms = crucero.rooms[piso_type[i]][0] * crucero.rooms[piso_type[i]][1] 
            num_pasillos = crucero.rooms[piso_type[i]][0] 
            piso = Piso(i+1, piso_type[i], num_rooms, num_pasillos)
            c.append(piso)
        pisos.append(c)
    return pisos

def create_pasillos(pisos_por_crucero):
    letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    pasillos_por_crucero= []
    for crucero in pisos_por_crucero:
        pasillos_por_piso = []
        for piso in crucero: 
            p = []
            j = 0
            for i in range(piso.num_pasillos):
                num_rooms = int(piso.num_rooms / piso.num_pasillos)
                pasillo = Pasillo(letter[j], num_rooms, piso.piso_type)
                p.append(pasillo)
                j += 1
            pasillos_por_piso.append(p)
        pasillos_por_crucero.append(pasillos_por_piso)
    return pasillos_por_crucero
          
def create_rooms(pasillos_por_crucero, cruceros, pisos_por_crucero):
    rooms_por_crucero= []
    for crucero in pasillos_por_crucero:
        c = 0
        rooms_por_piso = []
        for piso in crucero: 
            r = []
            j = 0
            p = 0
            for pasillo in piso:
                for i in range(pasillo.num_rooms):
                    if pasillo.pasillo_type == 'simple':
                        name = pasillo.name + str(i+1) 
                        room = Sencilla(name, cruceros[c].rooms_capacity['simple'], cruceros[c].ticket_price['simple'])
                        r.append(room)
                        j += 1
                    elif pasillo.pasillo_type == 'premium':
                        name = pasillo.name + str(i+1)
                        room = Premium(name, cruceros[c].rooms_capacity['premium'], cruceros[c].ticket_price['premium'])
                        r.append(room)
                        j += 1
                    elif pasillo.pasillo_type == 'vip':
                        name = pasillo.name + str(i+1)
                        room = Vip(name, cruceros[c].rooms_capacity['vip'], cruceros[c].ticket_price['vip'])
                        r.append(room)
                        j += 1
                p += 1
            rooms_por_piso.append(r)
            c += 1
        rooms_por_crucero.append(rooms_por_piso)
    return rooms_por_crucero

def add_pasillos_to_piso(pisos_por_crucero, pasillos_por_crucero):
    c = 0
    for crucero in pisos_por_crucero:
        p = 0
        for piso in crucero:
            piso.pasillos.append(pasillos_por_crucero[c][p])
            p += 1
        c += 1
    return pisos_por_crucero

def add_rooms_to_piso(pisos_por_crucero, rooms_por_crucero):
    c = 0
    for crucero in pisos_por_crucero:
        p = 0
        for piso in crucero:
            piso.rooms.append(rooms_por_crucero[c][p])
            p += 1
        c += 1
    return pisos_por_crucero

def matriz_rooms(rooms_por_crucero, pisos_por_crucero, p, c, cant_personas):
    R = []
    for r in rooms_por_crucero[c][p]:
        if (r.available == True):
            R.append(r.name)
    fila = pisos_por_crucero[c][p].num_pasillos
    print(fila)
    col = int(pisos_por_crucero[c][p].num_rooms / fila) 
    M = [R[col*i : col*(i+1)] for i in range(fila)]
    print(M)
    return M

def update(cruceros, pisos_por_crucero):
    """Updates the data in cruceros with the Pisos, Rooms, and Pasillos

    Args:
        cruceros ([list]): [Cruceros data]

    Returns:
        [list]: [Updated list]
    """
    for c in cruceros:
        for index in range(len(cruceros)):
            c.pisos = pisos_por_crucero[index]
    return cruceros

def create_pisos_rooms_pasillos():
    cruceros = read_file()
    pisos_por_crucero = create_piso(cruceros)
    pasillos_por_crucero = create_pasillos(pisos_por_crucero)
    pisos_por_crucero = add_pasillos_to_piso(pisos_por_crucero, pasillos_por_crucero)
    rooms_por_crucero = create_rooms(pasillos_por_crucero,cruceros, pisos_por_crucero)
    pisos_por_crucero = add_rooms_to_piso(pisos_por_crucero, rooms_por_crucero)
    
    #for i in cruceros:
    #    print(i.rooms)
    #for i in pisos_por_crucero[0]:
    #    print(f'ID: {i.num_piso}. Type: {i.piso_type}. Num Habitaciones: {i.num_rooms}. Num Pasillos: {i.num_pasillos}')
    #for i in pasillos_por_crucero[0][0]: #Crucero/Piso
    #    print(i.pasillo_type)
    #for i in pisos_por_crucero[1]:
    #    print(f'\nID: {i.num_piso}. Type: {i.piso_type}. Num Habitaciones: {i.num_rooms}. Num Pasillos: {i.num_pasillos}. Pasillos: {i.rooms}')
    #matriz_rooms(rooms_por_crucero, pisos_por_crucero, 0, 1, 8)
    #for c in rooms_por_crucero:
    #    for p in c:
    #        for r in p:
    #            if r.name == 'B2':
    #                r.available = True
    #print(rooms_por_crucero[0][2][0].capacity)
    return pisos_por_crucero, rooms_por_crucero

def cruiship_selection(cruceros, search):
    """Selects a Crucero from the File

    Returns:
        [object]: [Selected Crucero]
        [List]: [list of objects]
    """
    if read_file():
        while True:
            try:
                for index, crucero in enumerate(cruceros,1):
                    if search == '1':
                        print(f'{index}. {crucero.name}')
                    else:
                        print(f'{index}. {crucero.route}')
                selection = int(input('Select a Cruiship: '))
                crucero_selected = cruceros[selection-1]
                cruceros.pop(selection-1)
                break
            except:
                print('Please make sure you enter one of the number of choices above.')
    return crucero_selected, cruceros, selection-1

def create_client():
    while True:
        try:
            name = input('Enter your name: ')
            dni = input('Enter your dni: ')
            age = int(input('Enter your age: '))
            disability = input('''Do you have any disabilities?: 
            1. Yes
            2. No
            >> ''') == '1'

        except:
            print('Please make sure you are entering validate data.')
    client = Cliente(name, dni, age, disability)
    return client


def main():
    cruceros = read_file()
    pisos_por_crucero, rooms_por_crucero = create_pisos_rooms_pasillos()
    cruceros = update(cruceros, pisos_por_crucero)
    while True:
        search = input('''Please input, ticket criteria: 
        1. Crucero
        2. Destino
        >> ''')
        if search == '1':
            crucero, cruceros, index_crucero = cruiship_selection(cruceros, search)
            while True:
                try:  
                    option = input('''What room type do you want:
                    1. Sencilla
                    2. Premium
                    3. Vip
                    >> ''')
                    cant_personas = int(input('Enter the number of people registering in the cruiship: '))
                    if option == '1':
                        available_rooms = matriz_rooms(rooms_por_crucero, pisos_por_crucero, 0, index_crucero, cant_personas)
                        contador = cant_personas
                        registered = 0
                        rooms = []
                        while True:
                            try:
                                for i, r in enumerate(rooms_por_crucero[index_crucero][0], 1):
                                    print(f'{i}. {r.name}')
                                selection = int(input('Select a Room: '))
                                room_selected = rooms_por_crucero[index_crucero][0][selection-1]
                                if room_selected.capacity <= cant_personas:
                                    while len(room_selected.clients) != cant_personas:
                                        client = create_client()
                                        room_selected.clients.append(client)
                                    room_selected.ocupy_room()
                                    rooms.append(room_selected)
                                else:
                                    while len(room_selected.clients) != room_selected.capacity:
                                        client = create_client()
                                        room_selected.clients.append(client)
                                        contador -= 1
                                        registered +=1
                                    room_selected.ocupy_room()
                                    rooms.append(room_selected)
                                    print('You exceeded our room capacity, please select a second room.')
                                    while contador != 0:
                                        available_rooms = matriz_rooms(rooms_por_crucero, pisos_por_crucero, 0, index_crucero, cant_personas)
                                        for i,r in enumerate(rooms_por_crucero[index_crucero][0], 1):
                                             print(f'{i}. {r.name}')
                                             selection = int(input('Select a Room: '))
                                        while (registered != cant_personas) or(len(room_selected.clients) != room_selected.capacity):
                                            client = create_client()
                                            room_selected.clients.append(client)
                                            contador -= 1
                                            registered += 1
                                        room_selected.ocupy_room()
                                        rooms.append(room_selected)
                                       
                                    break
                            except:
                                print('Please make sure you enter one of the number of choices above.')
                            
                        else:
                            pass
                        break
                    elif option == '2':
                        matriz_rooms(rooms_por_crucero, pisos_por_crucero, 1, index_crucero, cant_personas)
                        break
                    elif option == '3':
                        matriz_rooms(rooms_por_crucero, pisos_por_crucero, 2, index_crucero, cant_personas)
                        break
                    else:
                        raise ZeroDivisionError
                except ZeroDivisionError:
                    print('Please make sure you enter one of the number of rooms above.')
                except ValueError:
                    print('Please make sure you enter an integer number.')
            break
        elif search == '2':
            crucero, cruceros = cruiship_selection(cruceros, search)
            break
        else:
            break

main()