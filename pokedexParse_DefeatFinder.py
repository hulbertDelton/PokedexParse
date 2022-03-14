import sys
import os
import csv
from tkinter import *
from tkinter import ttk
import DexUtils

class pokemon_entry:
    def __init__(self) -> None:
        self.dex_num = 0
        self.name = ""
        self.entries = [] #this is the pokedex entries for this pokemon
        self.has_atk_data = False #does this pokemon even have conditions for attacking?
        self.has_dft_data = False #does this pokemon even have conditions for defeat with ___ type?
        self.atk_types = [] #the list of attacks this pokemon must be seen using
        self.dft_types = [] #the list of types of moves this pokemon must be defeated by

    class dex_item:
        def __init__(self) -> None:
            self.condition_to_complete = "" #this is the sentence used in the dex entry. We aren't explicitly using it right now but we HAVE it so... why not
            self.num_to_complete = 0 #how many times you have to DO the thing
            self.is_type_condition = False #is this dex entry an attack or 
            self.is_aggro = False
            self.attack_type #this is the type of the attack, the most critical piece of information

#global variables
all_pokemon = []
defeated_pokemon = []
attacking_pokemon = []
attack_pkmn = ""
attacker = ""



