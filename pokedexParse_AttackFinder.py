import sys
import os
import csv
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import DexUtils

class pokemon_entry:
    def __init__(self):
        self.dex_num = 0
        self.name = ""
        self.entries = [] #this will be a container of DexItems
        self.has_attack_data = False
        self.has_defeat_data = False
        self.attack_types = []
        self.defeat_type = ""

    class dex_item:
        def __init__(self):
            self.condition_to_complete = ""
            self.num_to_complete = 0
            self.is_attack_condition = False
            self.attack_type = ""
            self.is_aggro = False

all_pokemon = []
defeated_pokemon = []
attacking_pokemon = []
hunted_pkmn = ""
defeated = ""

def get_all_attacks():
    script_dir = os.path.dirname(__file__)
    dex_data = os.path.join(script_dir,"ArceusPokedexData.csv")
    with open(dex_data,'r') as file:
        csvr = csv.reader(file)

        for row in csvr:
            p = pokemon_entry()
            p.dex_num = int(row[0])
            p.name = row[1]
            
            firstDex = p.dex_item()
            firstDex.condition_to_complete = row[2]
            firstDex.num_to_complete = row[3]

            p.entries.append(firstDex)

            i = 4
            while i < 36:
                if row[i] == '':
                    break
                else:
                    d = p.dex_item()
                    d.condition_to_complete = row[i]
                    i += 1
                    if is_int(row[i]):
                        d.num_to_complete = int(row[i])
                    else:
                        print("ERROR PARSING " + str(p.dex_num) + " - " + p.name + " dex entry '" + d.condition_to_complete + "'")
                        break
                    i += 1
                    if row[i] != '':
                        d.attack_type = row[i]
                        d.is_attack_condition = True
                    #i += 1
                        if row[i + 1] == 'TRUE':
                            d.is_aggro = True
                            p.has_attack_data = True
                            p.attack_types.append(row[i])
                        else:
                            if p.has_defeat_data == False:
                                p.has_defeat_data = True
                                p.defeat_type = row[i]
                    i += 1
                    p.entries.append(d)
                i += 1

            all_pokemon.append(p)

        for pkmn in all_pokemon:
            #Get list of pokemon that have "Times you've seen it use X"
            if pkmn.has_attack_data == True:
                attacking_pokemon.append(pkmn)
            #Get list of pokemon that have "Defeated with X-type moves"
            if pkmn.has_defeat_data == True:
                defeated_pokemon.append(pkmn)
            
def restart_program():
    pyt = sys.executable
    os.execl(pyt,pyt, * sys.argv)

#runtime program

get_all_attacks()

#Compare the typing of all moves in the Defeated list with the items in the Use list
hunted_pkmn = input("Pokemon you are hunting (or 'xx' to quit): ")

if hunted_pkmn == "xx":
    sys.exit()

for n in defeated_pokemon:
    if(hunted_pkmn.lower() == n.name.lower()):
        defeated = n
        break

if defeated == "":
    print("No condition for " + hunted_pkmn)
    restart_program()

#Output list of pokemon that match up
label = "Optimized fight list for " + n.name + ", who needs to be defeated by " + defeated.defeat_type + ":"

root = Tk()
frm = ttk.Frame(root, padding = 10)
frm.grid()
ttk.Label(frm, text = label).grid(column = 0, row = 0)

n = 1

for m in attacking_pokemon:
    for t in m.attack_types:
        if defeated.defeat_type == t:
            ttk.Label(frm, text = m.name).grid(column = 0, row = n)
            n += 1
            
            print(m.name)
            break

ttk.Button(frm, text = "Okay thanks", command = lambda:[root.destroy,restart_program()]).grid(column = 0, row = n)
root.mainloop()