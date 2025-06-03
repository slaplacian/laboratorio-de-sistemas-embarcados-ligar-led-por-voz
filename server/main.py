import socket
import json
from vosk import Model, KaldiRecognizer

model = Model("small-model")
recognizer = KaldiRecognizer(model, 16000, '["on", "off"]')

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 256

def recv_all(sock, size):
    data = b""
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Aguardando conexão do ESP32...")
        conn, addr = s.accept()
        with conn:
            print("Conectado por", addr)

            while True:

                data = recv_all(conn, BUFFER_SIZE)
                if data is None:
                    print("Desconectado.")
                    break

                with open("amostra.raw", "ab") as f:
                    f.write(data)

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    comando = result.get("text", "").lower()
                    print("Reconhecido:", comando)


                    if "on" in comando:
                        conn.sendall(b'ON\n')
                    elif "off" in comando:
                        conn.sendall(b'OFF\n')
                    else:
                        conn.sendall(b'IGN\n')
                else:
                    print("Parcial:", recognizer.PartialResult())

except KeyboardInterrupt:
    print("Servidor encerrado.")
