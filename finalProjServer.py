"""
# Name: John-Francis Caccamo
# Class: CS 372
# Date: 3 / 13 / 22
# Description: The server side of the final socket server-client chat utilizing the Pokemon class from
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


# The Server Side Socket Creation & Connection Function
def serverPokemonSocket():
    # get the hostname
    host = socket.gethostname()

    # where the client can access the socket
    port = 7000

    # create server-side socket
    server_socket = socket.socket()

    # socket will be established by binding the host and port #
    server_socket.bind((host, port))

    # establish how many clients that can listen to the server
    server_socket.listen(2)

    # new connection from the client
    server_connection, address = server_socket.accept()
    print("Connection from: " + str(address))
    print("\nwaiting for Pokemon Trainer to declare their name and choose their Pokemon ...")
    print("Enter /q into the input to quit the Pokemon Battle at anytime")

    serverWait()

    # receive client's name
    client_trainer_name = server_connection.recv(1024).decode()

    # quit command
    if client_trainer_name == '/q':
        print("Client chooses not to declare their name, Server is automatically the champion!!")
        server_connection.close()
        return

    # publish client_trainer_name
    print("Connected Client Pokemon Trainer name is: " + client_trainer_name)

    # take input for server_trainer_name, reminding user of the char limit
    server_trainer_name = input("\nPlease enter your name -aka the Server Pokemon Trainer's Name! \nDo note that input "
                                "will be truncated to 1024 chars - the maximum transmissible size across the socket\n"
                                "   -> ")

    """
    Citation for string truncation
    Source: https://stackoverflow.com/questions/2872512/python-truncate-a-long-string
    Date: 3 / 13 / 22 
    Name: Marcelo Cantos 
    """
    # NOTE: this truncation only applies to the name since the rest of the inputs have validation procedures
    # and this is the only input that can reach max send capacity of 1024 bytes
    server_trainer_name = server_trainer_name[:1024] if len(server_trainer_name) > 1024 else server_trainer_name

    # send the server trainer's name
    server_connection.send(server_trainer_name.encode())

    # server_trainer_name == 'q' the quit command
    if server_trainer_name == '/q':
        print("Server chooses not to declare their name and proceed with battle...")
        server_connection.close()
        return

    serverWait()

    # commonFunctions.bufferflusher(server_connection)

    # receive client pokemon data
    client_pokemon_data = server_connection.recv(1024).decode()

    # quit command
    if client_pokemon_data == '/q':
        print("Client chooses not to pick a Pokemon, Server is automatically the champion!!")
        server_connection.close()
        return

    # publish the client's Pokemon choice
    print("Connected client user chooses: " + client_pokemon_data)

    # prompt the server user for their choice
    commonFunctions.printPokemonOptions(server_trainer_name)

    # call the loop function in commonFunction in order to perform input validation for appropriate Pokemon choice
    server_choice = commonFunctions.pokemonAttackDecision(" Please enter your Pokemon Choice -> ", "not an integer "
                                                                                                   "for valid Pokemon"
                                                                                                   " choice", 1, 3)

    # exit key entered
    if server_choice == '/q':
        print("Server Chooses not to pick a Pokemon and proceed with Battle...")
        server_connection.send(server_choice.encode())
        server_connection.close()
        return

    # instantiate the server's Pokemon
    server_pokemon = Pokemon(server_choice)

    # publish the server's Pokemon stats
    server_pokemon.info_and_stats_publisher()

    # send the server's Pokemon name to the client
    pokemon_name = server_pokemon.get_name()
    server_connection.send(pokemon_name.encode())

    print("\nTime for BATTTTTLEEEEEEE!!!! ")

    # Pokemon battle loop
    while server_pokemon.get_health() > 0:

        serverWait()

        # receive client_pokemon_data stream. it won't accept client_pokemon_data packet greater than 1024 bytes
        client_attack_data = server_connection.recv(1024).decode()

        # quit command received
        if client_attack_data == '/q':
            print("The Client forfeits the battle, the Server is the Pokemon Champion automatically!")
            break

        if client_attack_data == "Client Defeated":
            print("The Client has been defeated! The Server and " + server_pokemon.get_name() + " are the Pokemon "
                                                                                                "Champions!")
            break

        # carry out attack from client's Pokemon to server's Pokemon
        print("Pokemon attack from client is " + client_attack_data)
        server_pokemon.perform_attack(client_attack_data)

        # server's Pokemon has run out of health
        if server_pokemon.get_health() <= 0:
            print("Server's " + server_pokemon.get_name() + " has been defeated !")
            server_connection.send("Server Defeated".encode())
            break

        print("The Server's Pokemon now has a health of " + str(server_pokemon.get_health()), "\n")

        print("Press 1 to use " + server_pokemon.get_moves()[0])
        print("Press 2 to use " + server_pokemon.get_moves()[1])

        # call pokemonAttackDecision from commonFunctions file to get attack_choice
        attack_choice = commonFunctions.pokemonAttackDecision("  Choose your Pokemon's move -> ", "not an integer for "
                                                                                                 "valid attack "
                                                                                                 "choice", 1, 2)

        # exit / quit command
        if attack_choice == '/q':
            print("Server Chooses not to proceed with Battle...")
            server_connection.send(attack_choice.encode())
            break

        # obtain the attack move's string
        attack_data = commonFunctions.assignAttackData(server_pokemon, attack_choice)

        # send Pokemon attack data to the client
        server_connection.send(attack_data.encode())

    # close the connection
    server_connection.close()

    return


def serverWait():
    print("\nWaiting for Client Response..........\n")


if __name__ == "__main__":
    print("Creating socket for SERVER VS CLIENT POKEMON DUEL!!!....")
    serverPokemonSocket()