import mcrcon
import logging
import os
import json

# Set up logging
logging.basicConfig(filename='rcon.log', level=logging.INFO)

# Get user input for server details
server_ip = input("Enter server IP: ") or "localhost"
rcon_port = input("Enter RCON port: ") or "25575"
rcon_password = input("Enter RCON password: ")

# Get user input for client name
client_name = input("Enter client name: ") or "Rcon"

# Create a new Rcon instance and connect to the server
client = mcrcon.MCRcon(server_ip, rcon_password, int(rcon_port))
try:
    client.connect()
    print(f"Connected to server {server_ip}:{rcon_port}")
    logging.info(f"Connected to server {server_ip}:{rcon_port}")
    # Set the program title to show the mc server it is connected to
    os.system(f"title Connected to {server_ip}:{rcon_port}")
except Exception as e:
    print(f"Failed to connect to server: {e}")
    logging.error(f"Failed to connect to server: {e}")
    exit()

# Set the client name
try:
    client.command(f"/minecraft:client rename {client_name}")
    print(f"Client name set to {client_name}")
    logging.info(f"Client name set to {client_name}")
except Exception as e:
    print(f"Failed to set client name: {e}")
    logging.error(f"Failed to set client name: {e}")

# Function to handle the rename command
def rename_client(new_name):
    try:
        client.command(f"/minecraft:client rename {new_name}")
        print(f"Client name set to {new_name}")
        logging.info(f"Client name set to {new_name}")
    except Exception as e:
        print(f"Failed to set client name: {e}")
        logging.error(f"Failed to set client name: {e}")

# Function to handle custom commands
def custom_commands(command):
    if command.lower() == "rhelp":
        print("Custom commands:")
        print("rename <name> - Rename the RCON client")
        print("say <message> - Send a message to all players")
        print("serverinfo - Get server information")
        print("playerinfo <player_name> - Get player information")
    elif command.lower().startswith("say"):
        message = " ".join(command.split()[1:])
        tellraw_command = f'tellraw @a {json.dumps({"text": f"[{client_name}] {message}"})}'
        response = client.command(tellraw_command)
        logging.info(f"Executed command: {command}")
    elif command.lower().startswith("rename"):
        new_name = " ".join(command.split()[1:])
        rename_client(new_name)
    elif command.lower() == "serverinfo":
        response = client.command("list")
        print(f"Player Count: {response}")
        response = client.command("plugins")
        print(f"Plugins: {response}")
        response = client.command("datapack list")
        print(f"Datapacks: {response}")
        response = client.command("seed")
        print(f"Seed: {response}")
        response = client.command("version")
        print(f"Server Version: {response}")
        logging.info(f"Executed serverinfo command")
    elif command.lower().startswith("playerinfo"):
        player_name = command.split()[1]
        response = client.command(f"data get entity {player_name} Health")
        print(f"{player_name}'s Health: {response}")
        response = client.command(f"data get entity {player_name} foodLevel")
        print(f"{player_name}'s Food Level: {response}")
        response = client.command(f"data get entity {player_name} ArmorItems")
        print(f"{player_name}'s Armor: {response}")
        response = client.command(f"data get entity {player_name} xp")
        print(f"{player_name}'s Experience Points: {response}")
        gamemodes = ["survival", "creative", "adventure", "spectator"]
        for gamemode in gamemodes:
            response = client.command(f"/execute if entity @a[name={player_name},gamemode={gamemode}] run say")
            if response:
                print(f"{player_name}'s Gamemode: {gamemode}")
                break
        logging.info(f"Executed playerinfo command for {player_name}")
    else:
        try:
            response = client.command(command)
            print(response)
            logging.info(f"Executed command: {command}")
        except Exception as e:
            print(f"Failed to execute command: {e}")
            logging.error(f"Failed to execute command: {e}")

# Loop until the user quits
while True:
    # Get input from the user
    command = input("> ")
    
    # Process the user's command
    custom_commands(command)
