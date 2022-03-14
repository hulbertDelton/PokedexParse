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

def is_aggro(entry:str):
    attack = "seen it use"
    found = entry.find(attack)

    if found == -1:
        return False
    else:
        return True

def row_add(row_in:int):
    if row_in % 2 == 0:
        return row_in + 1
    else:
        return row_in