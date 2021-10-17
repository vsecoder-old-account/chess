#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import chess
import os

board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

sock = socket.socket()
port = int(os.environ.get("PORT", 5050))
print(f"{socket.gethostname()}:{port}")
sock.bind((socket.gethostname(), port))

while True:
    sock.listen(1)
    conn, addr = sock.accept()

    print('connected: ', addr)
    data = conn.recv(1024)
    if data:
        try:
            d = chess.Move.from_uci(str(data.decode("utf-8")))
            board.push(d)
            conn.send(bytes(str(board.fen()), encoding = 'UTF-8'))
        except Exception as e:
            conn.send(bytes(str(board.fen()), encoding = 'UTF-8'))
            print(e)
    else:
        conn.send(bytes(str(board.fen()), encoding = 'UTF-8'))

conn.close()