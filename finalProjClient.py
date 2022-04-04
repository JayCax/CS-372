"""
# Name: John-Francis Caccamo


# Class: CS 372
# Date: 3 / 13 / 22
# Description: The client side of the final socket server-client chat utilzing the Pokemon class from
# Pokemon.
"""

"""
README 

The program was done in Python3 (Python 3.8 , specifically) on PyCharm. 
finalProjectServer, finalProjectClient, Pokemon and commonFunctions need to all be in the same directory. 
Afterwards, all that is needed is to simply run finalProjectServer to create the socket, 
then subsequently finalProjectClient and switch terminals 
between them back and forth in order to proceed with the socket communication via the Pokemon battle between them.  

"""

import socket
from pokemon import Pokemon
import commonFunctions

"""
# Citation for the following Socket Creation code inspiration
# Date: 3 / 10 / 22
# derived and built from
# Source URL: https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
# Author of socket / host creation article: João Ventura
"""

"""
# Secondary citation to socket creation:
# Date: 3 / 10 / 22
# inspired from
# Source URL: https://docs.python.org/3/howto/sockets.html
# Author: Gordon McMillan
"""

"""
# Furthermore, socket theory and respective coding understanding were facilitated by 
# Ch. 2.7 Socket Programming: Creating Network Application
# Ch. 3.2 Multiplexing and Demultiplexing
# of the Kurose and Ross - Computer Networking: A Top Down Approach
# Dates: 3 / 3 / 22 - 3 / 12 / 22 
"""


# The Client Side Socket Connection Function
def clientPokemonSocket():
    # host / local machine
    host = socket.gethostname()

    # socket client port number
    port = 7000

    # create client-side socket
    client_socket = socket.socket()

    # connect to the server / socket
    client_socket.connect((host, port))

    print("Enter /q into the input to quit the Pokemon battle at any time\n")

    # take input for client_trainer_name, reminding user of the char limit
    client_trainer_name = input("Please enter your name -aka the Client Pokemon Trainer's Name! \nDo note that input "
                                "will be truncated to 1024 chars - the maximum transmissible size across the socket\n"
                                "  -> ")

    """
    Citation for string truncation
    Source: https://stackoverflow.com/questions/2872512/python-truncate-a-long-string
    Date: 3 / 13 / 22 
    Name: Marcelo Cantos 
    """
    # NOTE: this truncation only applies to the name since the rest of the inputs have validation procedures
    # and this is the only input that can reach max send capacity of 1024 bytes
    client_trainer_name = client_trainer_name[:1024] if len(client_trainer_name) > 1024 else client_trainer_name

    # send the client name
    client_socket.send(client_trainer_name.encode())

    if client_trainer_name == '/q':
        print("Client chooses not to declare their name and proceed with battle...")
        client_socket.close()
        return

    clientWait()

    # receive the server name - truncate at 1024 bytes
    server_trainer_name = client_socket.recv(1024).decode()

    # "/q" has been entered
    if server_trainer_name == '/q':
        print(
            "Server chooses not to declare their name and proceed with battle, Client is automatically the champion!!")
        client_socket.close()
        return

    # publish the connected server_trainer_name
    print("Connected Server Pokemon Trainer name is: " + server_trainer_name)

    # present the client with the Pokemon options
    commonFunctions.printPokemonOptions(client_trainer_name)

    client_choice = commonFunctions.pokemonAttackDecision(" Please enter your Pokemon Choice -> ", "not an integer "
                                                                                                   "for valid Pokemon "
                                                                                                   "choice", 1, 3)

    # exit key entered
    if client_choice == '/q':
        print("Client Chooses not to pick a Pokemon and proceed with Battle...")
        client_socket.send(client_choice.encode())
        client_socket.close()
        return

    # instantiate the Pokemon
    client_pokemon = Pokemon(client_choice)

    # publish the client Pokemon's stats
    client_pokemon.info_and_stats_publisher()

    # send the Pokemon name
    pokemon_msg = client_pokemon.get_name()
    client_socket.send(pokemon_msg.encode())

    clientWait()

    # receive the server's Pokemon choice
    server_pokemon_data = client_socket.recv(1024).decode()

    # quit key
    if server_pokemon_data == '/q':
        print("Server chooses not to pick a Pokemon, Client is automatically the champion!!")
        client_socket.close()
        return

    # publish the server Pokemon data
    print("Connected server user chooses: " + server_pokemon_data)

    print("\nTime for BATTTTTLEEEEEEE!!!!\n")

    # The battle loop
    while client_pokemon.get_health() > 0:

        print("Press 1 to use " + client_pokemon.get_moves()[0])
        print("Press 2 to use " + client_pokemon.get_moves()[1])

        # call pokemonAttackDecision from commonFunctions file to get attack_choice
        attack_choice = commonFunctions.pokemonAttackDecision("  Choose your Pokemon's move -> ", "not an integer for "
                                                                                                 "valid attack "
                                                                                                 "choice", 1, 2)

        # exit / quit command
        if attack_choice == '/q':
            print("Client Chooses not to proceed with Battle...")
            client_socket.send(attack_choice.encode())
            break

        # Get Pokemon attack string associated with their attack choice
        attack_data = commonFunctions.assignAttackData(client_pokemon, attack_choice)

        # send the Pokemon attack string
        client_socket.send(attack_data.encode())

        clientWait()

        # receive the attack data from the client
        server_attack_data = client_socket.recv(1024).decode()

        # quit command received
        if server_attack_data == '/q':
            print("The Server forfeits the battle, the Client is the Pokemon Champion automatically!")
            break

        # if the server's Pokemon has no more health
        if server_attack_data == "Server Defeated":
            print("The Server has been defeated! The Client and " + client_pokemon.get_name() + " are the Pokemon "
                                                                                                "Champions!")
            break

        # publish the server's Pokemon attack
        print("\nPokemon attack from server is " + server_attack_data)
        client_pokemon.perform_attack(server_attack_data)

        # client's Pokemon has run out of health
        if client_pokemon.get_health() <= 0:
            print("Client's " + client_pokemon.get_name() + " has been defeated !")
            client_socket.send("Client Defeated".encode())
            break

        print("The Client's Pokemon now has a health of " + str(client_pokemon.get_health()), "\n")

    # close the connection
    client_socket.close()

    return


def clientWait():
    print("\nWaiting for Server Response..........\n")


if __name__ == "__main__":
    clientPokemonSocket()