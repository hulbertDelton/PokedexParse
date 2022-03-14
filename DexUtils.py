import sys
import os
import csv

def parse_dex_entry(p):
    print("\n" + str(p.dex_num) + " - " + p.name)
    print("DEFEATED - " + p.defeat_type + "\nAttacks:")
    for a in p.attack_types:
        print(a)

def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True

def is_aggro(entry):
    attack = "seen it use"
    found = entry.find(attack)

    if found == -1:
        return True
    else:
        return False

def all_attacks(pokemon):
    atks = ""
    
