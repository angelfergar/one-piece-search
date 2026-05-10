import requests
import random
import deepl

main_url = "https://api.api-onepiece.com/v2/"
api_options = {"fruits": "fruits/en", "swords": "swords/en", "characters": "characters/en"}

auth_key = "6515076f-f36a-48d4-9dcd-79171ba0a51a:fx"
deepl_client = deepl.DeepLClient(auth_key)

def get_op_data(endpoint):
    try:
        response = requests.get(main_url+endpoint, timeout=5)
        return response.json()
    except:
        return None

def get_fruit_info(fruit):
    name = fruit.get("roman_name", "name")
    type = fruit.get("type")
    description = fruit.get("description")
    if description:
        description = deepl_client.translate_text(description, target_lang="ES")
    else:
        description = ""
    message = "¿Sabías que...?\n"
    message += f"Hay una fruta llamada {name}. Esta fruta es del tipo {type}.\n{description.text}"
    return message

def get_sword_info(sword):
    name = sword.get("name")
    description = sword.get("description")
    if description:
        description = deepl_client.translate_text(description, target_lang="ES")
    else:
        description = ""
    message = "¿Sabías que...?\n"
    message += f"Hay una espada llamada {name}.\n{description.text}"
    return message
def get_character_info(character):
    name = character.get("name")
    size = character.get("size")
    age = character.get("age")
    if size and age:
        age = age.replace("ans", "años")
        message = "¿Sabías que...?\n"
        message += f"{name} mide {size} y tiene {age}.\n"
        bounty = character.get("bounty")
        if bounty:
            bounty = bounty + "₿"
            message += f" Tiene una recompensa de {bounty}."

        fruit = character.get("fruit")
        if fruit:
            fruit = fruit.get("name")
            message += f" Y posee la fruta {fruit}"

        return message
    else:
        return get_op_fact()

def get_op_fact():
    random_key = random.choice(list(api_options.keys()))
    endpoint = api_options[random_key]

    data = get_op_data(endpoint)
    random_data = random.choice(data)

    message = ""

    if api_options["fruits"] in endpoint:
        message = get_fruit_info(random_data)
    elif api_options["swords"] in endpoint:
        message = get_sword_info(random_data)
    elif api_options["characters"] in endpoint:
        message = get_character_info(random_data)
    return message