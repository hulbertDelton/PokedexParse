import sys
import os
import os.path as path
import csv

class dex_entry:
    def __init__(self):
        self.condition_description = ""
        self.condition_value = 0
        self.condition_type = ""
        self.attack_name = ""

class pokemon_entry:
    def __init__(self):
        self.dex_number = 0
        self.name = ""
        self.entries = [dex_entry()]
        self.defeat_types = [str()]
        self.attack_types = [str()]

class user_search:
    def __init__(self):
        self.header:str = ""
        self.pokemon_data = pokemon_entry()

#utilities
def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True

def is_aggro(entry:str):
    attack = "seen it use"
    found = entry.find(attack)

    if found == -1:
        return False
    else:
        return True

def entry_contains(entry:str,query:str):
    found = entry.find(query)
    if found == -1:
        return False
    else:
        return True

#running the show
def restart_program():
    pyt = sys.executable
    os.execl(pyt, pyt, * sys.argv)

#FORMATTING OUTPUT UTILITIES
def row_add(row_in:int):
    if row_in % 2 == 0:
        return row_in + 1
    else:
        return row_in

#CSV shit
def get_list(listname:str,condition_comparison:str):
    datapath = path.dirname(__file__)
    filename = path.join(datapath,"data/" + listname)
    
    if path.exists(filename):
        return filename
    else:
        write_new_data_file(filename, condition_comparison)
        get_list(listname, condition_comparison)

def write_new_data_file(to_path:str,comparison:str):
    dir = path.dirname(__file__)
    csv_file = path.join(dir,"ArceusPokedexData.csv")
    item_list = []
    new_header = []

    with open(csv_file,'r') as file:
        csvr = csv.DictReader(file)
        new_header = csvr.fieldnames
        
        condition_counter = 1
        for row in csvr:
            while condition_counter < 10:
                condition_name = "DexCondition" + str(condition_counter)
                if entry_contains(row[condition_name].lower(),comparison.lower()):
                    item_list.append(row)
                    break
                condition_counter += 1
            condition_counter = 1
    
    with open(to_path,'w', newline = '') as outfile:
        writer = csv.DictWriter(outfile, fieldnames = new_header)
        writer.writeheader()
        writer.writerows(item_list)

def create_attack_list():
    dir = path.dirname(__file__)
    data_file = path.join(dir,"data/AtkData.csv")
    csv_file = path.join(dir,"ArceusPokedexData.csv")
    item_list = []
    new_header = []

    with open(csv_file,'r') as file:
        csvr = csv.DictReader(file)
        new_header = csvr.fieldnames
        
        counter = 2
        for row in csvr:
            while counter < 10:
                name = "DexCondition" + str(counter)
                if "Times you've seen it use " in row[name] and not "Times you've seen it use a " in row[name]:
                    item_list.append(row)
                    break
                counter += 1
            counter = 2
    
    with open(data_file,'w', newline = '') as outfile:
        writer = csv.DictWriter(outfile, fieldnames = new_header)
        writer.writeheader()
        writer.writerows(item_list)

def get_attack_name(entry:dex_entry):
    condition = entry.condition_description
    attack_strip = "Times you've seen it use "
    attack_name = ""

    if (entry.condition_type != "" and entry_contains(condition, attack_strip)):
        attack_name = condition[len(attack_strip):len(condition)]
    if (len(attack_name) > 0):
        return attack_name
    else:
        return ""

def fill_pokedex(subdex_classification:str):
    dex = [pokemon_entry()]
    dex.clear()

    classification = ""
    check_string = ""
    if subdex_classification.lower() == "attack":
        classification = "AtkData.csv"
        check_string = "Seen it use"
    elif subdex_classification.lower() == "defeat":
        classification = "DftData.csv"
        check_string = "defeated with"

    file_path = get_list(classification, check_string)
    
    with open(file_path,'r') as file:
        csvr = csv.DictReader(file)
        for row in csvr:
            pokemon = pokemon_entry()            
            pokemon.name = row['Name']
            pokemon.dex_number = row['DexNum']
            
            first_dex = dex_entry()
            first_dex.condition_description = row['DexCondition1']
            first_dex.condition_value = row['NumToComplete1']

            pokemon.entries.clear()
            pokemon.entries.append(first_dex)

            counter = 2
            while counter < 10:
                condition_name = "DexCondition" + str(counter)

                if row[condition_name] == "":
                    break

                number_to_complete = "NumToComplete" + str(counter)
                move_type = "TypeQualifier" + str(counter)

                entry = dex_entry()
                entry.condition_description = row[condition_name]
                entry.condition_value = row[number_to_complete]
                entry.condition_type = row[move_type]
                entry.attack_name = get_attack_name(entry)

                if entry.condition_type != "":
                    if entry.attack_name == "":
                        pokemon.defeat_types.append(entry.condition_type)
                    else:
                        pokemon.attack_types.append(entry.condition_type)

                counter += 1
                pokemon.entries.append(entry)
            counter = 2
            dex.append(pokemon)
        return dex

dir = path.dirname(__file__)
data_file = path.join(dir,"data/AtkData.csv")
if not path.exists(data_file):
    create_attack_list()

pokemon_with_attacks = fill_pokedex("attack")
pokemon_with_defeat_conditions = fill_pokedex("defeat")
#--------------------------------------------------------------------------------------
def get_user_input():
    search_object = user_search()
    found = False

    inp = input("Enter the name of a pokemon, or enter 'xx' to quit: ").lower()
    if inp == "xx":
        sys.exit()

    for pokemon in pokemon_with_attacks:
        if pokemon.name.lower() == inp:
            search_object.pokemon_data = pokemon
            found = True
    for pokemon in pokemon_with_defeat_conditions:
        if pokemon.name.lower() == inp:
            search_object.pokemon_data = pokemon
            found = True

    if found:
        nameout = search_object.pokemon_data.name[0].upper() + search_object.pokemon_data.name[1:len(search_object.pokemon_data.name)]
        search_object.header = "\nOptimized data for " + nameout + ":"
        return search_object
    else:
        print(inp + " has no data that needs to be optimized")
        sys.exit()

pokemon_query = user_search()
pokemon_query = get_user_input()
print(pokemon_query.header)

x = 2
divider = ""
while(x < (len(pokemon_query.header))):
    if (x % 2 == 0):
        divider += "+"
    else:
        divider += "-"
    x += 1
print(divider)

print("Pokemon to attack with " + pokemon_query.pokemon_data.name + ":")
if len(pokemon_query.pokemon_data.attack_types) > 0:
    #compare the pokemon's attacks to the defeat types of the dex
    
    for attack_type in set(pokemon_query.pokemon_data.attack_types):
            if (attack_type != ""):
                strout = attack_type.upper() + ": "
                for entry in pokemon_query.pokemon_data.entries:
                    if entry.condition_type == attack_type:
                        strout += entry.attack_name + " / "
                print(strout[:-3])
                for poke in pokemon_with_defeat_conditions:
                    for dft in poke.defeat_types:
                        if attack_type == dft:
                            print("    - " + poke.name)

if len(pokemon_query.pokemon_data.defeat_types) > 0:
    print("\nPokemon to defeat " + pokemon_query.pokemon_data.name + " with: ")
    for defeat_type in pokemon_query.pokemon_data.defeat_types:
        if defeat_type != "":
            print(defeat_type.upper() + ": ")
            for pok in pokemon_with_defeat_conditions:
                for attack in set(pok.attack_types):
                    if attack == defeat_type:
                        newline = "    -" + pok.name + " ("
                        for e in pok.entries:
                            if e.condition_type == attack:
                                newline += e.attack_name + " / "
                        newline = newline[:-3]
                        newline += ")"
                        print(newline)
