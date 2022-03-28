import sys
import os
import csv
from tkinter import *
from tkinter import ttk
import DexUtils as util

class pokemon_entry:
    def __init__(self):
        self.dex_num = 0
        self.name = ""
        self.entries = [] #this is the pokedex entries for this pokemon
        self.has_atk_data = False #does this pokemon even have conditions for attacking?
        self.has_dft_data = False #does this pokemon even have conditions for defeat with ___ type?
        self.atk_types = [] #the list of attacks this pokemon must be seen using
        self.dft_types = [] #the list of types of moves this pokemon must be defeated by
    class dex_item:
        def __init__(self):
            self.condition_to_complete = "" #this is the sentence used in the dex entry. We aren't explicitly using it right now but we HAVE it so... why not
            self.num_to_complete = 0 #how many times you have to DO the thing
            self.is_aggro = False
            self.attack_type = "" #this is the type of the attack, the most critical piece of information

class search_entry:
    def __init__(self):
        self.found_pkmn:str = ""
        self.attacker:pokemon_entry() = None
        self.header = ""
    
#setup variables
all_pokemon = [pokemon_entry()]
defeated_pokemon = [pokemon_entry()]
attacking_pokemon = [pokemon_entry()]

def get_all_attacks():
    script_dir = os.path.dirname(__file__)
    dex_data = os.path.join(script_dir, "ArceusPokedexData.csv")

    with open(dex_data, 'r') as file:
        csvr = csv.reader(file)
        for row in csvr:
            pkmn = pokemon_entry()
            pkmn.dex_num = int(row[0])
            pkmn.name = row[1]

            #the first dex entry is always "number caught" so we'll just fill this in
            first_dex_entry = pkmn.dex_item()
            first_dex_entry.condition_to_complete = row[2]
            first_dex_entry.num_to_complete = int(row[3])
            pkmn.entries.append(first_dex_entry) #add it to the pokemon's list of entries

            i = 4 #we're starting after the first entry
            while i < 36: #there are a maximum of 9 entries
                if row[i] == "": #if there is no condition, we want to assume that we've captured all the entries for the pokemon
                    break
                else:
                    entry = pkmn.dex_item()
                    entry.condition_to_complete = row[i] #the condition string
                    i += 1 #next column
                    if util.is_int(row[i]): #make sure we're actually reading an int here, otherwise we're fucked
                        entry.num_to_complete = int(row[i])
                    else:
                        print("PARSE ERROR: " + str(pkmn.dex_num) + " - " + pkmn.name + " // '" + entry.condition_to_complete + "'")
                        break
                    i += 1 #next column
                    if row[i] != '': #if it isn't blank, then we've got an attack on our hands
                        entry.attack_type = row[i] #the type of the attack
                        entry.is_aggro = util.is_aggro(entry.condition_to_complete) #is it an ATTACK, or a DEFEAT condition?

                        if entry.is_aggro:
                            pkmn.has_atk_data = True
                            pkmn.atk_types.append(row[i])
                        else:
                            pkmn.has_dft_data = True
                            pkmn.dft_types.append(row[i])
                    i += 1
                    pkmn.entries.append(entry) #add the entry to the dex
                i += 1 #next column in preparation for the next entry
            all_pokemon.append(pkmn) #add the pokemon to the dataset of all pokemon
        for p in all_pokemon: #we're going to create our Defeat and Attack datasets now
            if p.has_atk_data:
                attacking_pokemon.append(p)
            if p.has_dft_data:
                defeated_pokemon.append(p)

def restart_program():
    pyt = sys.executable
    os.execl(pyt, pyt, * sys.argv)

def get_attack_name(pokemon:pokemon_entry(),typ:str):
    atk_name = ""
    delim = len("Times you've seen it use ")

    for entry in pokemon.entries:
        if typ.lower() == entry.attack_type.lower():
            if atk_name != "":
                atk_name += "/"
            atk_name += entry.condition_to_complete[delim:len(entry.condition_to_complete)]
    return atk_name

def list_all_attacks(pokemon:pokemon_entry()):
    atks:str = ""
    for a in set(pokemon.atk_types):
        if atks != "":
            atks += " and "
        atks += get_attack_name(pokemon,a) + " (" + a + ")"
    return atks

def get_user_input():
    inp = input("Pokemon you are trying to attack with (or 'xx' to quit): ")
    if inp.lower() == "xx":
        sys.exit()
    for n in attacking_pokemon:
        if (inp.lower() == n.name.lower()):
            poke = n
            break
    try: poke
    except AttributeError: lambda:[print("No condition for " + inp), get_user_input()]
    else: return(poke)

#runtime leggoooo
get_all_attacks()

found_pokemon = search_entry()

found_pokemon.found_pkmn = get_user_input()
found_pokemon.header = "Hitlist for " + found_pokemon.found_pkmn.name + ", who must attack with " + list_all_attacks(found_pokemon.found_pkmn) + ":"

root = Tk()
frm = ttk.Frame(root, padding = 10)
frm.grid()
ttk.Label(frm, text = found_pokemon.header).grid(column = 0, row = 0)

print(found_pokemon.header)
x = 2
divider = ""
while(x < (len(found_pokemon.header))):
    if (x % 2 == 0):
        divider += "+"
    else:
        divider += "-"
    x += 1
print(divider)

ro = 1 #we're going to append the list of pokemon to the popup starting after the header
col = 0
for poke in defeated_pokemon: #for each pokemon in the DEFEAT list
    for dft in poke.dft_types: #for each defeat type in that pokemon's list of DEFEAT_TYPES
        for atk in set(found_pokemon.found_pkmn.atk_types):
            if atk == dft:         
                ttk.Label(frm, text = poke.name + " (" + dft + ")").grid(column = (ro + 1) % 2, row = util.row_add(ro + 1))
                ro += 1
                print(poke.name + " (" + dft + ")")
ttk.Button(frm, text = "Okay thanks", command = lambda:[root.destroy,restart_program()]).grid(column = 0, row = ro + 2)
root.mainloop()