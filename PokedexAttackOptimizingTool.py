import DexUtils as util
import os.path as path

dir = path.dirname(__file__)
data_file = path.join(dir,"data/AtkData.csv")
if not path.exists(data_file):
    util.create_attack_list()

pokemon_with_attacks = util.fill_pokedex("attack")
pokemon_with_defeat_conditions = util.fill_pokedex("defeat")

pokemon_query = util.get_user_input(pokemon_with_attacks,pokemon_with_defeat_conditions)
print(pokemon_query.header)

util.draw_divider(pokemon_query)

if len(pokemon_query.pokemon_data.attack_types) > 1:
    print("Pokemon to attack with " + pokemon_query.pokemon_data.name + ":")
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

if len(pokemon_query.pokemon_data.defeat_types) > 1:
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