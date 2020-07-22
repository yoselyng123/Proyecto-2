import requests
import pickle
from GestionCruceros import Crucero, read_file

# Ask the user to select a Crucero to modify its menu.
def cruiship_selection():
    """Selects a Crucero from the File

    Returns:
        [object]: [Selected Crucero]
        [List]: [list of objects]
    """
    if read_file():
        cruceros = read_file()
        while True:
            try:
                for index, crucero in enumerate(cruceros,1):
                    print(f'{index}. {crucero.name}')
                selection = int(input('A que crucero le desea modificar el menu?: '))
                crucero_selected = cruceros[selection-1]
                cruceros.pop(selection-1)
                break
            except:
                print('Please make sure you enter one of the number of choices above.')
    return crucero_selected, cruceros
# Algoritmos de Busqueda y Ordenamiento.
def binary_search(menu, search, sort_by='name'):
    first = 0
    last = len(menu)-1
    index = -1
    while (first <= last) and (index == -1):
        mid = (first + last)//2
        if menu[mid].get(sort_by) == search:
            if mid == 0:
                mid = 'cero'
                return mid
            return mid
        else:
            if search < menu[mid].get(sort_by):
                last = mid - 1
            else:
                first = mid + 1
    return False
def merge_sort(array, left_index, right_index, sort_by='name'):
    if left_index >= right_index:
        return
    middle = (left_index + right_index) // 2
    merge_sort(array, left_index, middle, sort_by)
    merge_sort(array, middle + 1, right_index, sort_by)
    merge(array, left_index, right_index, middle, sort_by)
    return array
def merge(array, left_index, right_index, middle, sort_by='name'):
    left_copy = array[left_index:middle + 1]
    right_copy = array[middle + 1:right_index + 1]
    left_copy_index = 0
    right_copy_index = 0
    sorted_index = left_index

    while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
        if left_copy[left_copy_index].get(sort_by) <= right_copy[right_copy_index].get(sort_by):
            array[sorted_index] = left_copy[left_copy_index]
            left_copy_index = left_copy_index + 1
        else:
            array[sorted_index] = right_copy[right_copy_index]
            right_copy_index = right_copy_index + 1
        sorted_index = sorted_index + 1
    
    while left_copy_index < len(left_copy):
        array[sorted_index] = left_copy[left_copy_index]
        left_copy_index = left_copy_index + 1
        sorted_index = sorted_index + 1
    while right_copy_index < len(right_copy):
        array[sorted_index] = right_copy[right_copy_index]
        right_copy_index = right_copy_index + 1
        sorted_index = sorted_index + 1
# Adds a New plate to the menu
def add_plate(menu):
    """Adds a new food or drink to the menu

    Args:
        menu ([list]): [Contains the data of the food and drinks in the restaurant]

    Returns:
        [list]: [Updated Menu]
    """
    # Asks the user the information for the new plate to add.
    while True:
        plate_name = input('Insert the name of the new plate: ').title()
        while True:
            plate_type = input('''Is it a beverage or food?: 
            1. Food
            2. Beverage
            >> ''')
            # If the plate to add is a Food, the user gets asked its preparation method.
            if plate_type == '1':
                while True:
                    prep = input('''Empaque o Preparacion?: 
                    1. Empaque
                    2. Preparacion
                    >> ''')
                    if prep == '1':
                        prep = 'Empaque'
                        break
                    elif prep == '2':
                        prep = 'Preparacion'
                        break
                    else:
                        print('Please make sure you enter either 1 or 2.')
                plate_type = 'Food'
                break
            # If the plate to add is a drink, the user gets asked the size.
            elif plate_type == '2':
                while True:
                    size = input('''Pequeño, Mediano o Grande?: 
                    1. Pequeño
                    2. Mediano
                    3. Grande
                    >> ''')
                    if size == '1':
                        size = 'Pequeño'
                        break
                    elif size == '2':
                        size = 'Mediano'
                        break
                    elif size == '3':
                        size = 'Grande'
                        break
                    else:
                        print('Please make sure you enter one of the available options(1, 2 or 3).')
                plate_type = 'Beverage'
                break
            else: 
                print('Please make sure you are entering either 1 for (Food) or 2 for (Beverage).')
        # Asks the price of the plate and adds the Taxes (IVA). 
        while True:
            try:
                price = float(input('Enter the price: '))
                price = (price + (price*0.16)) # Precio con el 16% de IVA.
                break
            except:
                print('Please make sure you are entering a valid number.')
        break
    # A new Dictionary is created with the information of the new plate and its added to the menu.  
    new_plate = {}
    new_plate['name'] = plate_name
    new_plate['type'] = plate_type
    if plate_type == 'Food':
        new_plate['prep'] = prep
    elif plate_type == 'Beverage':
        new_plate['size'] = size
    new_plate['price'] = price
    menu.append(new_plate)
    # The user gets notified that the plate was succesfully added.
    print(f'The {plate_type}: {plate_name} has been succesfully added to the menu')
    return menu
# Removes an existing plate from the menu
def remove_plate(menu):
    """Removes an existing item in the menu

    Args:
        menu ([list]): [Contains the data of the food and drinks in the restaurant]

    Returns:
        [list]: [Updated Menu]
    """
    menu = merge_sort(menu, 0, len(menu)-1)
    search = input('Enter the name of the plate you want to remove from the menu: ').title()
    if binary_search(menu, search): #if the plate is in the menu = True
        index = binary_search(menu, search)
        if index == 'cero':
            index = 0
            del menu[index]
        else:
            del menu[index]
        print('Succesfully deleted from the Menu')
    else: # if the plate is not in the menu = False
        print(f'{search} is not in the Menu.')
    return menu
# Modifies an existing plate from the menu
def modify_plate(menu):
    """Modify the already existing data in the menu

    Args:
        menu ([list]): [Contains the data of the food and drinks in the restaurant]

    Returns:
        [list]: [Updated Menu]
    """
    menu = merge_sort(menu, 0, len(menu)-1)
    plate = input('Enter the name of the plate you want to modify from the menu: ').title()
    "succesfully modified from the menu"
    if binary_search(menu, plate): #if the plate is in the menu = int >= 0
        index = binary_search(menu, plate)
        if index == 'cero':
            index = 0
        option = input('''What do you want to modify?:
        1. Name
        2. Type
        3. Prep/Size
        4. Price
        5. None/Back to menu
        >> ''')
        while True:
            # Changes the Name of the Plate, and its key given that The name of the plate is the key in the menu for that plate
            if option == '1':
                new_name = input('Enter the new name of the plate: ').title()
                menu[index]['name'] = new_name
                print('Succesfully modified from the Menu')
                break
            # Changes the type (Food or Beverage) of the plate.
            elif option == '2':
                while True:
                    new_type = input('''Is it a beverage or food?: 
                    1. Food
                    2. Beverage
                    >> ''')
                    # If the plate to add is a Food, the user gets asked its preparation method.
                    if new_type == '1':
                        while True:
                            prep = input('''Empaque o Preparacion?: 
                            1. Empaque
                            2. Preparacion
                            >> ''')
                            if prep == '1':
                                prep = 'Empaque'
                                break
                            elif prep == '2':
                                prep = 'Preparacion'
                                break
                            else:
                                print('Please make sure you enter either 1 or 2.')
                        new_type = 'Food'
                        menu[index]['type'] = new_type
                        menu[index]['prep'] = prep
                        if menu[index].get('size', False):
                            del menu[index]['size']
                        print('Succesfully modified from the Menu')
                        break
                    # If the plate to add is a drink, the user gets asked the size.
                    elif new_type == '2':
                        while True:
                            size = input('''Pequeño, Mediano o Grande?: 
                            1. Pequeño
                            2. Mediano
                            3. Grande
                            >> ''')
                            if size == '1':
                                size = 'Pequeño'
                                break
                            elif size == '2':
                                size = 'Mediano'
                                break
                            elif size == '3':
                                size = 'Grande'
                                break
                            else:
                                print('Please make sure you enter one of the available options(1, 2 or 3).')
                        # Changes the data in menu.
                        new_type = 'Beverage'
                        menu[index]['type'] = new_type
                        menu[index]['size'] = size
                        if menu[index].get('prep', False):
                            del menu[index]['prep']
                        print('Succesfully modified from the Menu')
                        break
                    else: 
                        print('Please make sure you are entering either 1 for (Food) or 2 for (Beverage).')
                    break
                
                break
            # Changes the Preparation or Size of the plate.
            elif option == '3':
                # Changes the Preparation of the plate if the plate's type is Food.
                if menu[index].get('prep', False):
                    while True:
                        new_prep = input('''Empaque o Preparacion?: 
                        1. Empaque
                        2. Preparacion
                        >> ''')
                        if new_prep == '1':
                            new_prep = 'Empaque'
                            break
                        elif new_prep == '2':
                            new_prep = 'Preparacion'
                            break
                        else:
                            print('Please make sure you enter either 1 or 2.')
                    menu[index]['prep'] = new_prep
                    print('Succesfully modified from the Menu')
                    break
                # Changes the Size of the plate if the plate's type is Beverage.
                elif menu[index].get('size', False):
                    while True:
                        new_size = input('''Enter the new size of the Beverage: 
                        1. Pequeño
                        2. Mediano
                        3. Grande
                        >> ''')
                        if new_size == '1':
                            new_size = 'Pequeño'
                            break
                        elif new_size == '2':
                            new_size = 'Mediano'
                            break
                        elif new_size == '3':
                            new_size = 'Grande'
                            break
                        else:
                            print('Please make sure you enter one of the available options(1, 2 or 3).')
                    menu[index]['size'] = new_size
                    print('Succesfully modified from the Menu')
                    break
                else: 
                    print('This plate does not have "preparation" or "size" defined.')
            # Changes the price of the plate and adds the Taxes (IVA).
            elif option == '4':
                while True:
                    try:
                        new_price = float(input('Enter the new price of the plate: '))
                        new_price = (new_price + (new_price*0.16)) # Precio con el 16% de IVA.
                        break
                    except:
                        print('Please enter a valid number.')
                menu[index]['price'] = new_price
                print('Succesfully modified from the Menu')
                break
            elif option == '5':
                break
            else:
                print('Invalid Option. Please make sure you are entering one of the provided options(1, 2, 3 or 4).')
    else: # If the plate is not in the menu then the user can't modify any data.
        print('That plate is not in the Menu.')
    # Returns the updated Menu.
    return menu
# Creates a new combo and adds it to the combos menu
def add_combo(menu_combos, menu):
    """Creates and adds a combo to the Combo Menu

    Args:
        menu_combos ([list]): [Contains the data of the combos in the restaurant]
        menu ([list]): [Contains the data of the food and drinks in the restaurant]

    Returns:
        [list]: [The updated Combo's Menu]
    """
    #Creates a combo.
    combo = []
    while True:
        name_combo = input('Enter the name of the combo: ').title()
        # displays a number next to the plate.
        while True:
            try:
                number_of_plates = int(input('Please enter how many items the combo is going to have(Minimum 2): '))
                if number_of_plates >= 2:
                    break
                else:
                    print("Combo's need a minimum of two elements. Please make sure you enter a number equal or greater than 2.")
            except:
                print('Please enter a valid Number.')
        contador = 0
        while contador != number_of_plates:
            try:
                print(f'Please enter the number of the plate you want to add to the combo {name_combo}.')
                indexes = []
                plates = []
                # Enumerates each plate in the menu. So that it displays a number next to the plate, and the user can input which plate to add to the combo.
                for index, plate in enumerate(menu,1):
                    plate = menu[index-1]['name']
                    print(f'{index}. {plate}')
                    indexes.append(index)
                    plates.append(plate)
                # Registers the selection of the plate.
                while True:
                    try:
                        selection = int(input('>> '))
                        if selection in indexes:
                            combo.append(plates[selection - 1])
                        else:
                            raise Exception
                        break
                    except:
                        print('Please enter a valid number.')
                # Keeps track of the items added to combo
                contador += 1
                
            except:
                print('Please enter one of the options available.')

        # Asks the price of the combo and adds the Taxes (IVA). 
        while True:
            try:
                price = float(input('Enter the price: '))
                price = (price + (price*0.16)) # Precio con el 16% de IVA.
                break
            except:
                print('Please make sure you are entering a valid number.')
        break
    
    # Adds the created combo to the Combo's Menu.
    new_combo = {}
    new_combo['name'] = name_combo
    new_combo['elements'] = combo
    new_combo['price'] = price
    menu_combos.append(new_combo)
    # Returns the updated Menu_Combos
    return menu_combos
# Searches for a Product/Combo based on its name
def product_search(product, menu):
    """Searches in the menu for a product by its name

    Args:
        product ([string]): [item in the menu]
        menu ([list]): [contains the food and drinks data]

    Returns:
        [dict]: [information of the product]
    """
    products = menu
    
    for i in range(len(products)):
        if product == products[i].get('name'):
            return products[i]
    return False
# Searches for a Product/Combo based on its name
def price_search(price, menu):
    """Searches in the menu for a product by its price

    Args:
        product ([string]): [item in the menu]
        menu ([list]): [contains the food and drinks data]

    Returns:
        [dict]: [information of the product]
    """
    products = menu
    prices = []
    for i in range(len(products)):
        if price >= products[i].get('price'):
            prices.append(products[i])
    return prices
# Access the menu, and asks the user what to do with it.
def access_menu(selected_crucero):
    """Access the menu from the crucero and modifies it

    Args:
        selected_crucero ([object]): [crucero]

    Returns:
        [list]: [data of the food and drinks]
    """
    menu = selected_crucero.menu
    menu_combos = selected_crucero.menu_combos
    
    while True:
        option = input('''\nWelcome to The Cruiship Restaurant
        1. Add Plate to Menu
        2. Modify Plate from the menu
        3. Remove Plate From the menu
        4. Add Combo to Menu
        5. Remove Combo from Menu
        6. Search for a product by Name or Price Range
        7. Search for a Combo by Name or Price Range
        8. Finish
        >> ''')
        if option == '1':
            menu = add_plate(menu)
        
        elif option == '2':
            if len(menu) != 0:
                menu = modify_plate(menu)
            else:
                print('The Menu is empty.')
        
        elif option == '3':
            if len(menu) != 0:
                menu =  remove_plate(menu)
            else:
                print('The Menu is empty.') 
        
        elif option == '4':
            menu_combos = add_combo(menu_combos, menu)
        
        elif option == '5':
            if len(menu_combos) != 0:
                menu_combos = remove_plate(menu_combos)
            else:
                print('The Menu is empty.')
        
        elif option == '6':
            search = input('Ingrese el nombre o el rango de precio del producto: ').title()
            # If search is a number, then it will look for that price range.
            try:
                search = float(search)
                if price_search(search, menu) != []:
                        print(price_search(search, menu))
                else:
                    print("We're sorry there are no products in that price range.")
            # if search is a string, then it will look for that product name.
            except:
                if product_search(search, menu) == False:
                    print("We're sorry the product you are looking for does not exists.")
                else:
                    print(product_search(search, menu))
                    
        elif option == '7':
            search = input('Ingrese el nombre o el rango de precio del Combo: ').title()
            # If search is a number, then it will look for that price range.
            try:
                search = float(search)
                if price_search(search, menu_combos) != []:
                        print(price_search(search, menu_combos))
                else:
                    print("We're sorry there are no Combos in that price range.")
            # if search is a string, then it will look for that product name.
            except:
                if product_search(search, menu_combos) == False:
                    print("We're sorry the Combo you are looking for does not exists.")
                else:
                    print(product_search(search, menu_combos))
        elif option == '8':
            print(menu)
            print(menu_combos)
        
        else:
            return menu, menu_combos
            break
# Reads the existing Crucero File, Access the menu, modifies it and saves the updated data into the file.
def main():
    if read_file():
        selected_crucero, cruceros = cruiship_selection()
        menu, menu_combos = access_menu(selected_crucero)
        selected_crucero.menu = menu
        selected_crucero.menu_combos = menu_combos
        cruceros.append(selected_crucero)
        data = open('Cruceros', 'wb')
        pickle.dump(cruceros, data)
        data.close()
    else:
        print('No existen Cruceros.')

main()

