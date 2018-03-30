"""
war card game client and server
"""
import asyncio
from collections import namedtuple
from enum import Enum
import logging
import random
import socket
import socketserver
import threading
import sys

"""
Namedtuples work like classes, but are much more lightweight so they end
up being faster. It would be a good idea to keep objects in each of these
for each game which contain the game's state, for instance things like the
socket, the cards given, the cards still available, etc.
"""
Game = namedtuple("Game", ["p1","p1hand", "p2", "p2hand"])

class Command(Enum):
    """
    The byte values sent as the first byte of any message in the war protocol.
    """
    WANTGAME = 0
    GAMESTART = 1
    PLAYCARD = 2
    PLAYRESULT = 3

class Result(Enum):
    """
    The byte values sent as the payload byte of a PLAYRESULT message.
    """
    WIN = 0
    DRAW = 1
    LOSE = 2

def readexactly(sock, numbytes):
    """
    Accumulate exactly `numbytes` from `sock` and return those. If EOF is found
    before numbytes have been received, be sure to account for that here or in
    the caller.
    """
    ret_bytes = b''
    for x in range(numbytes):
        try:
            read_byte = sock.recv(1)
            ret_bytes += read_byte
        except EOFError:
            ret_bytes = b''
            break
    return ret_bytes

def kill_game(game):
    """
    TODO: If either client sends a bad message, immediately nuke the game.
    """
    game[0][0].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#game[0][0].shutdown(socket.SHUT_RDWR)
    game[0][0].close()
    game[2][0].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#game[2][0].shutdown(socket.SHUT_RDWR)
    game[2][0].close()
    return

def compare_cards(card1, card2):
    """
    TODO: Given an integer card representation, return -1 for card1 < card2,
    0 for card1 = card2, and 1 for card1 > card2
    """
    if card1%13 < card2%13:
        return -1

    if card1%13 == card2%13:
        return 0

    if card1%13 > card2%13:
        return 1

def deal_cards():
    """
    TODO: Randomize a deck of cards (list of ints 0..51), and return two
    26 card "hands."
    """
    cards = []
    for x in range(52): 
        cards.append(x)
    random.shuffle(cards)
    ret_list = [cards[0:26], cards[26:]]
    return ret_list

def play_game (game):
    sock1 = game[0][0]
    hand1 = game[1]
    sock2 = game[2][0]
    hand2 = game[3]
#    sock1.setblocking(True)
#    sock2.setblocking(True)


#logging.info (hand1)
#logging.info (hand2)

    data_read = readexactly(sock1, 2)
    if (data_read != bytes([Command.WANTGAME.value, Command.WANTGAME.value])):
        kill_game(game)
        return
    data_read = readexactly(sock2, 2)
    if (data_read != bytes([Command.WANTGAME.value, Command.WANTGAME.value])):
        kill_game(game)
        return
    
    data = [Command.GAMESTART.value] + hand1
#logging.info(data)
    data_send = bytearray()
    for e in data:
        data_send.append(e)
    sock1.send(data_send)
   
    data = [Command.GAMESTART.value] + hand2
#logging.info(data)
    data_send = bytearray()
    for e in data:
        data_send.append(e)
    sock2.send(data_send)

    while (True):
        p1 = readexactly(sock1, 2)
        p2 = readexactly(sock2, 2)
        if len(p1) == 0 or len(p2) == 0:
            kill_game(game)
            break
        if bytes(p1[0]) != bytes(Command.PLAYCARD.value) or bytes(p2[0]) != bytes(Command.PLAYCARD.value):
            kill_game(game)
            break
        result = compare_cards(p1[1], p2[1])
        if result == 1:
            sock1.send(bytes([Command.PLAYRESULT.value, Result.WIN.value]))
            sock2.send(bytes([Command.PLAYRESULT.value, Result.LOSE.value]))
            continue
        if result == 0:
            sock1.send(bytes([Command.PLAYRESULT.value, Result.DRAW.value]))
            sock2.send(bytes([Command.PLAYRESULT.value, Result.DRAW.value]))
            continue
        if result == -1:
            sock1.send(bytes([Command.PLAYRESULT.value, Result.LOSE.value]))
            sock2.send(bytes([Command.PLAYRESULT.value, Result.WIN.value]))
            continue
    return

class MyTCPServer (socketserver.TCPServer, socketserver.BaseRequestHandler):
    allow_reuse_address = True
    request_queue_size = 1000


def serve_game(host, port):
    """
    TODO: Open a socket for listening for new connections on host:port, and
    perform the war protocol to serve a game of war between each client.
    This function should run forever, continually serving clients.
    """
#    server_socket = MyServer((host,port))
    
    server_socket = MyTCPServer ((host,port), socketserver.BaseRequestHandler)

#server_socket.handle_timeout(10) 
    while True:
        howManyConnections = 0
        temp_list = []
        numthread = 0;
        while True:
            try:
                (clientsocket, address) = server_socket.get_request()
                temp_list.append((clientsocket, address))
                howManyConnections = howManyConnections + 1
                                    
                if (howManyConnections == 2):
                    deck = deal_cards()
                    hand1 = deck[0]
                    random.shuffle(hand1)
                    hand2 = deck[1]
                    random.shuffle(hand2)

                    g = Game(temp_list[0], hand1, temp_list[1], hand2)
                    temp_list.clear()
                    thread = threading.Thread(target = play_game, args = (g,))
                    thread.start()
                    howManyConnections = 0
                    temp_list.clear()
#                server_socket.socket
            except KeyboardInterrupt:
                 break
        break   
    server_socket.shutdown()
    server_socket.server_close()
#thread.join()
    return

async def limit_client(host, port, loop, sem):
    """
    Limit the number of clients currently executing.
    You do not need to change this function.
    """
    async with sem:
        return await client(host, port, loop)

async def client(host, port, loop):
    """
    Run an individual client on a given event loop.
    You do not need to change this function.
    """
    try:
        reader, writer = await asyncio.open_connection(host, port, loop=loop)
        # send want game
        writer.write(b"\0\0")
        card_msg = await reader.readexactly(27)
        myscore = 0
        turn = 0
        for card in card_msg[1:]:
            turn = turn + 1
            writer.write(bytes([Command.PLAYCARD.value, card]))
            result = await reader.readexactly(2)
            if result[1] == Result.WIN.value:
                myscore += 1
            elif result[1] == Result.LOSE.value:
                myscore -= 1
        if myscore > 0:
            result = "won"
        elif myscore < 0:
            result = "lost"
        else:
            result = "drew"
        logging.debug("Game complete, I %s", result)
        writer.close()
        return 1
    except ConnectionResetError:
        logging.error("ConnectionResetError")
        return 0
    except asyncio.streams.IncompleteReadError:
        logging.error("asyncio.streams.IncompleteReadError")
        return 0
    except OSError:
        logging.error("OSError")
        return 0

def main(args):
    """
    launch a client/server
    """
    host = args[1]
    port = int(args[2])
    if args[0] == "server":
        try:
            # your server should serve clients until the user presses ctrl+c
            serve_game(host, port)
        except KeyboardInterrupt:
            pass
        return
    else:
        loop = asyncio.get_event_loop()

    if args[0] == "client":
        loop.run_until_complete(client(host, port, loop))
    elif args[0] == "clients":
        sem = asyncio.Semaphore(1000)
        num_clients = int(args[3])
        clients = [limit_client(host, port, loop, sem)
                   for x in range(num_clients)]
        async def run_all_clients():
            """
            use `as_completed` to spawn all clients simultaneously
            and collect their results in arbitrary order.
            """
            completed_clients = 0
            for client_result in asyncio.as_completed(clients):
                completed_clients += await client_result
            return completed_clients
        res = loop.run_until_complete(
            asyncio.Task(run_all_clients(), loop=loop))
        logging.info("%d completed clients", res)

    loop.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1:])
