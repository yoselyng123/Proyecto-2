import pickle

class Cliente:
    def __init__(self, dni, cant_personas):
        self.dni = dni
        self.cant_personas = cant_personas
        
class PuertoTour:
    tour_description = 'Tour en el puerto'
    def __init__(self):
        self.price = 30
        self.cupo_cliente = 4
        self.cupos_disponibles = 10
        self.horario_de_inicio = '7AM'
        self.discount = 0.1 # Tercera y cuarta
        self.registered_clients = []

    def add_people(self, client):
        if self.cupo_cliente >= client.cant_personas:
            if self.cupos_disponibles >= client.cant_personas:
                self.cupos_disponibles -= client.cant_personas
                return True
            else: 
                raise Exception
        else:
            return False

class DegustacionTour:
    tour_description = 'Degustacion de comida local'
    def __init__(self):
        self.price = 100
        self.cupo_cliente = 2
        self.cupos_disponibles = 100
        self.horario_de_inicio = '12PM'
        self.discount = 0
        self.registered_clients = []

    def add_people(self, client):
        if self.cupo_cliente >= client.cant_personas:
            if self.cupos_disponibles >= client.cant_personas:
                self.cupos_disponibles -= client.cant_personas
                return True
            else: 
                raise Exception
        else:
            return False

class TrotarTour:
    tour_description = 'Trotar por el pueblo/ciudad'
    def __init__(self):
        self.price = 0
        self.horario_de_inicio = '6AM'
        self.discount = 0
        self.registered_clients = []

    def add_people(self, client):
        return True
        

class LugaresHistoricosTour:
    tour_description = 'Visita a lugares Historicos'
    def __init__(self):
        self.price = 40
        self.cupo_cliente = 4
        self.cupos_disponibles = 15
        self.horario_de_inicio = '10AM'
        self.discount = 0.1 # A partir de la tercera
        self.registered_clients = []

    def add_people(self, client):
        if self.cupo_cliente >= client.cant_personas:
            if self.cupos_disponibles >= client.cant_personas:
                self.cupos_disponibles -= client.cant_personas
                return True
            else: 
                raise Exception
        else:
            return False


def resumen_de_compra(horario_de_inicio, precio):
    """Muestra un resumen de la compra de los Tours realizada por el cliente

    Args:
        horario_de_inicio ([str]): [Hora de Inicio del Tour]
        precio ([int]): [Precio total a pagar]
    """
    print(f'''
    Hora: {horario_de_inicio}.
    Monto con Descuento {precio}$.
    ''')

def sign_up_in_tour(tours):
    
    # Pregunta al cliente su dni y la cantidad de personas a registrar en el tour
    dni = input('Inserte su dni: ')
    while True:
        try:
            cant_personas = int(input('Inserte la cantidad de personas: '))
            break
        except:
            print('Please enter a valid number.')
    client = Cliente(dni, cant_personas)
    
    # Muestra las opciones de Tours Disponibles.
    tour_selection = input('''\nThe Tours are:
    1. Tour en el puerto
    2. Degustacion de comida local
    3. Trotar por el pueblo/ciudad
    4. Visita a lugares Historicos
    5. Exit
    >> ''')
    # Evalua la seleccion del cliente y lo agrega al registro de cada Tour.
    while True:
        # If the client enters 1, he/she will be registering in "Tour en el puerto" Tour
        if tour_selection == '1':
            try:
                if tours[0].add_people(client):
                    tours[0].registered_clients.append(client)
                    print('Succesfully registered in Tour.')
                    precio = 0
                    contador = 0
                    # Calculates the total price for the amount of people registered in the Tour
                    for i in range(cant_personas):
                        contador += 1
                        if (contador == 3) or (contador == 4):
                            precio += (tours[0].price - (tours[0].price * tours[0].discount))
                        else:
                            precio += tours[0].price
                    resumen_de_compra(tours[0].horario_de_inicio, precio)
                    
                else:
                    print('The Maximum quantity of people for this Tour is 4. Please try again.')
                #print(puerto_tour.cupos_disponibles)
            except: 
                print('This tour is maxed out, please try registering less people, or registering in another Tour.')
        
        # If the client enters 2, he/she will be registering in "Degustacion de comida local" Tour
        elif tour_selection == '2':
            try:
                if tours[1].add_people(client):
                    tours[1].registered_clients.append(client)
                    print('Succesfully registered in Tour.')
                    precio = 0
                    # Calculates the total price for the amount of people registered in the Tour
                    for i in range(cant_personas):
                        precio += tours[1].price
                    resumen_de_compra(tours[1].horario_de_inicio, precio)
                    
                else: 
                    print('The Maximum quantity of people for this Tour is 2. Please try again.')
                #print(degustacion_tour.cupos_disponibles)
                
            except:
                print('This tour is maxed out, please try registering less people, or registering in another Tour.')
        # If the client enters 3, he/she will be registering in "Trotar por el pueblo/ciudad" Tour
        elif tour_selection == '3':
            if tours[2].add_people(client):
                tours[2].registered_clients.append(client)
                print('Succesfully registered in Tour.')
                precio = 0
            resumen_de_compra(tours[2].horario_de_inicio, precio)
        # If the client enters 4, he/she will be registering in "Visita a lugares Historicos" Tour 
        elif tour_selection == '4':
            try:
                if tours[3].add_people(client):
                    tours[3].registered_clients.append(client)
                    print('Succesfully registered in Tour.')
                    precio = 0
                    contador = 0
                    # Calculates the total price for the amount of people registered in the Tour
                    for i in range(cant_personas):
                        contador += 1
                        if (contador == 3) or (contador == 4):
                            precio += (tours[3].price - (tours[3].price * tours[3].discount))
                        else:
                            precio += tours[3].price
                    resumen_de_compra(tours[3].horario_de_inicio, precio)
                    
                else:
                    print('The Maximum quantity of people for this Tour is 4. Please try again.')
                #print(lugares_historicos_tour.cupos_disponibles)
            except:
                print('This tour is maxed out, please try registering less people, or registering in another Tour.')
        else:
            break
        break

    return tours

def create_tours():
    # Crea un objeto de cada Tour
    puerto_tour = PuertoTour()
    degustacion_tour = DegustacionTour()
    trotar_tour = TrotarTour()
    lugares_historicos_tour = LugaresHistoricosTour()
    tours = [puerto_tour, degustacion_tour, trotar_tour, lugares_historicos_tour]
    return tours

def create_file(tours):
    # Crea un archivo con los objetos creados
    data = open('Tours', 'wb')
    pickle.dump(tours, data)
    data.close()
    del data
    return True

def read_file():
    try:
        data = open('Tours', 'rb')
        tours = pickle.load(data)
        data.close()
        return tours
    except:
        return False

def main():
    if read_file():
        print('Reading...')
        tours = read_file()
        tours = sign_up_in_tour(tours)
        data = open('Tours', 'wb')
        pickle.dump(tours, data)
        data.close()
    else:
        print('Creating file...')
        tours = create_tours()
        tours = sign_up_in_tour(tours)
        create_file(tours)

main()

