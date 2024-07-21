import sys
from five_cards.server import Server
from five_cards.client import Client

if sys.argv[1] == "server":
    server = Server(2)
    server.run_server()
elif sys.argv[1] == "client":
    client = Client()
    client.run_client()