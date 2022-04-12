import sys
import os
import DexUtils as util

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
        self.attack_types = []
        self.defeat_types = []

class user_search:
    def __init__(self):
        self.found_pokemon:str = ""
        self.attacker:pokemon_entry() = None
        self.header = ""

