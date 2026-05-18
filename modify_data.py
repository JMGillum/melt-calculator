import treasure.prompt
from coinData import CoinData

def Add(db, command=None):
    prompt = "add"
    if not command:
        command = treasure.prompt.Prompt(prompt).lower().split()
    if command:
        print(command)


def Root(db):
    prompt = "root"
    command = treasure.prompt.Prompt(prompt).lower().split()
    print(command)
    if command:
        if command[0] == "add":
            Add(db, command[1:])


def FetchCommand(prompt):
    command = treasure.prompt.Prompt(prompt).lower().split()
    command = [x.strip() for x in command]
    return command


def ExecuteCommand(menus, current_menu, command):
    if command:
        for c in current_menu.get("commands",[]):
            if command[0] in ["exit", "quit"]:
                return (None,[])
            if command[0] in c.get("keywords",[]):
                action = c.get("action",{})
                if action.get("type") == "menu":
                    return (menus[action.get("dest")], command[1:])
                else:
                    return (current_menu, [])

    return (current_menu,[])



def EditCoin(coin):
    country_id = None
    denomination_id = None
    value_id = None

    command = None
    while True:
        if not command:
            command = FetchCommand("edit coin")
        if command:
            if command[0] in ["exit", "quit", "back", "root"]:
                break
            if command[0] == "set":
                if len(command) <= 1:
                    value = command[1]
                    if value == "country_id":
                        pass
                    elif value == "denomination_id":
                        pass
                    elif value == "value_id":
                        pass
                    elif value == "metal":
                        pass
                    elif value == "gross-weight":
                        pass
                    elif value == "fineness":
                        pass
                    elif value == "precious-weight":
                        pass
                    elif value == "years":
                        pass
                    elif value == "nickname":
                        pass
            command = None






def ModifyDataInteractive(db):

    menus = {
        "root": {
            "prompt": "root",
            "commands": [
                {
                    "keywords": ["add"],
                    "action": {
                        "type": "menu",
                        "dest": "add"
                    },
                },
                {
                    "keywords": ["remove", "rm", "del"],
                    "action": {
                        "type": "menu",
                        "dest": "rm"
                        },
                    },
                {
                    "keywords": ["edit"],
                    "action": {
                        "type": "menu",
                        "dest": "edit"
                        },
                    },
                {
                    "keywords": ["back","root","/"],
                    "action": {
                        "type": "menu",
                        "dest": "root"
                        }
                    }
            ],
            "help_msg": {"preamble": "...", "epilogue": "..."},
        },
        "add": {
            "prompt": "add",
            "commands": [
                {"keywords": ["coin"]},
                {"keywords": ["face_value"]},
                {"keywords": ["denomination"]},
                {"keywords": ["country"]},
                {
                    "keywords": ["back", "root", "/"],
                    "action": {
                        "type": "menu",
                        "dest": "root"
                        }
                    }
            ],
            "help_msg": {"preamble": "...", "epilogue": "..."},
        },
        "rm": {
            "prompt": "rm",
            "commands": [
                {"keywords": ["coin"]},
                {"keywords": ["face_value"]},
                {"keywords": ["denomination"]},
                {"keywords": ["country"]},
                {
                    "keywords": ["back", "root", "/"],
                    "action": {
                        "type": "menu",
                        "dest": "root"
                        }
                    }
            ],
            "help_msg": {"preamble": "...", "epilogue": "..."},
        },
        "edit": {
            "prompt": "edit",
            "commands": [
                {"keywords": ["coin"]},
                {"keywords": ["face_value"]},
                {"keywords": ["denomination"]},
                {"keywords": ["country"]},
                {
                    "keywords": ["back", "root", "/"],
                    "action": {
                        "type": "menu",
                        "dest": "root"
                        }
                    }
            ],
            "help_msg": {"preamble": "...", "epilogue": "..."},
        },
    }

    current_menu = menus["root"]
    command = None
    while current_menu:
        if not command:
            command = FetchCommand(current_menu.get("prompt",""))
        current_menu, command = ExecuteCommand(menus,current_menu,command)
