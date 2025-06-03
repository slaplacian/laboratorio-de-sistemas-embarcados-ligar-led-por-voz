# Servidor de Reconhecimento de Voz com Vosk

Este diretório contém o código do **servidor local** que realiza o reconhecimento de voz em tempo real a partir de dados enviados por um ESP32 via socket. O servidor utiliza a biblioteca [Vosk](https://alphacephei.com/vosk/) para identificar comandos de voz simples como **"on"** e **"off"** e retornar a resposta ao dispositivo embarcado.

## Funcionamento

1. O ESP32 envia dados de áudio capturados via microfone para o servidor, em pequenos blocos.
2. O servidor escreve os dados em um arquivo `.raw` (para debug).
3. O áudio recebido é processado pelo modelo da Vosk.
4. Se um comando reconhecido for "on" ou "off", o servidor responde com `ON\n` ou `OFF\n` respectivamente.
5. Caso não reconheça nenhum comando, responde com `IGN\n`.


## Estrutura

- `main.py`: Script principal que inicia o servidor socket, recebe áudio do ESP32, faz o reconhecimento de voz e envia comandos de volta.

## Requisitos

- Python 3.7+
- [Vosk](https://pypi.org/project/vosk/)
- Um modelo Vosk já baixado (usamos o `small-model`)

### Instalar dependências

```bash
pip install vosk
```

## Baixar o Modelo Vosk

1. Acesse: https://alphacephei.com/vosk/models
2. Recomendado: **vosk-model-small-en-us-0.15** (ou outro modelo pequeno)
3. Extraia e renomeie a pasta como `small-model` (ou ajuste o nome no código)

Exemplo:

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 small-model
```

---

## Executar o Servidor

No diretório `server/`, execute:

```bash
python main.py
```

Você verá a mensagem:

```
Aguardando conexão do ESP32...
```

Assim que o ESP32 se conectar, o servidor começará a receber os dados de áudio e processá-los.

## 🔄 Comunicação

- O ESP32 envia áudio como `int16_t` via socket.
- O servidor processa o áudio e retorna:
  - `"ON\n"` → Acende o LED
  - `"OFF\n"` → Apaga o LED
  - `"IGN\n"` → Ignora/sem comando reconhecido
