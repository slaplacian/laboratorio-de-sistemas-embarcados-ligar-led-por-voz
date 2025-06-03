# Captura de Áudio e Controle de LED via Reconhecimento de Voz

Este código é responsável pela **captura de áudio usando o microfone INMP441** e envio dos dados via **socket TCP** para um servidor. O servidor processa os dados de áudio e retorna comandos de voz reconhecidos ("ON" ou "OFF"), que são utilizados para controlar o estado de um **LED conectado à GPIO 5** do ESP32.

## Funcionalidades

- Conecta-se a uma rede Wi-Fi.
- Inicializa a comunicação I²S com o microfone digital **INMP441**.
- Captura amostras de áudio e envia ao servidor por socket.
- Recebe comandos do servidor e **liga/desliga o LED** conforme o reconhecimento de voz.

## Hardware Utilizado

- **ESP32 DevKit v1**
- **Microfone digital INMP441** (conectado nas GPIOs 25, 26, 33)
- **LED** (conectado na GPIO 5 com resistor)

### Mapeamento de Pinos

| Função             | GPIO |
|--------------------|------|
| I2S WS (word select) | 25   |
| I2S SCK (clock)      | 26   |
| I2S SD (data in)     | 33   |
| LED                 | 5    |


## Estrutura do Código

- **WiFi**: Conexão com a rede local.
- **I2S**: Comunicação com o INMP441 para aquisição de áudio.
- **TCP Socket**: Comunicação com o servidor para envio de dados de áudio e recepção de comandos.
- **LED Control**: Interpretação de comandos recebidos e controle do LED.

## Dependências

Nenhuma biblioteca externa é necessária além das nativas do **Arduino para ESP32** (`WiFi`, `WiFiClient`, `driver/i2s.h`).

## Configurações

Antes de carregar o código no ESP32, edite os seguintes valores:

```cpp
const char* ssid = "SSID";         // Nome da rede Wi-Fi
const char* password = "PASSOWRD"; // Senha da rede
const char* server_ip = "IP";      // IP do servidor (ex: "192.168.0.100")
const uint16_t server_port = 5000; // Porta do servidor
```

##  Funcionamento

Ao inicializar, o ESP32 conecta-se à rede Wi-Fi. Em seguida, tenta se conectar ao servidor TCP especificado. A cada iteração do loop(), ele:

- Captura 1 segundo de áudio via I²S.

- Envia o buffer de áudio para o servidor.

- Aguarda uma resposta do tipo "ON" ou "OFF".

- Liga ou desliga o LED conforme o comando.

