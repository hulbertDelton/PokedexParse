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

gen_data_out = ""

for entry in pokemon_query.pokemon_data.entries:
    if "number defeated" in entry.condition_description.lower():
        gen_data_out += (f"    Need to defeat: {entry.condition_value}\n")
    if "agile" in entry.condition_description.lower():
        gen_data_out += (f"    Use agile-style moves: {entry.condition_value} times\n")
    if "strong" in entry.condition_description.lower():
        gen_data_out += (f"    Use strong-style moves: {entry.condition_value} times\n")

if len(gen_data_out) > 0:
    print("General data:")
    print(gen_data_out)

if len(pokemon_query.pokemon_data.attack_types) > 1:
    print(f"Pokemon to attack with {pokemon_query.pokemon_data.name}:")
    for attack_type in set(pokemon_query.pokemon_data.attack_types):
        if (attack_type != ""):
            strout = f"- {attack_type.upper()} ("
            for entry in pokemon_query.pokemon_data.entries:
                if entry.condition_type == attack_type:
                    strout += f"{entry.attack_name} / "
            print(f"{strout[:-3]})")
            for poke in pokemon_with_defeat_conditions:
                for dft in poke.defeat_types:
                    if attack_type == dft:
                        o = f"    - {poke.name}"
                        if poke.name == pokemon_query.pokemon_data.name:
                            o += " (lol)"
                        print(o)

if len(pokemon_query.pokemon_data.defeat_types) > 1:
    print(f"\nPokemon to defeat {pokemon_query.pokemon_data.name} with: ")
    for defeat_type in pokemon_query.pokemon_data.defeat_types:
        if defeat_type != "":
            print(f"- {defeat_type.upper()}: ")
            for pok in pokemon_with_defeat_conditions:
                for attack in set(pok.attack_types):
                    if attack == defeat_type:
                        newline = f"    - {pok.name} ("
                        for e in pok.entries:
                            if e.condition_type == attack:
                                newline += e.attack_name + " / "
                        newline = newline[:-3]+ ")"
                        print(newline)

print(f"For a complete pokedex, or to make your own CSV where you can remove entries as you complete them, visit {util.link('https://docs.google.com/spreadsheets/d/1oiLOZ0ATixPaJJ3P6xD37BDkUBCd6KWqwbt9QRTulm4/edit?usp=sharing')}\n")