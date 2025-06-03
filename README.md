# Laboratório de Sistemas Embarcados – Controle de LED por Voz

Este projeto foi desenvolvido como parte da disciplina de Laboratório de Sistemas Embarcados. O objetivo principal foi implementar um sistema capaz de **ligar e desligar um LED** com comandos de voz ("on" e "off") utilizando o microcontrolador **ESP32** e um servidor externo para processamento de áudio.

## Visão Geral

O sistema é dividido em três partes principais:

1. **ESP32 (`esp32ino/`)**
   Responsável pela **captura do áudio** através do microfone **INMP441** e **controle do LED** conectado à porta GPIO 5. A comunicação com o servidor é feita via **socket TCP**.

2. **Servidor Web (`server/`)**
   Executado em um computador local, esse componente **recebe o áudio capturado pelo ESP32**, processa os dados utilizando a biblioteca **Vosk** para reconhecimento de voz e **retorna comandos** de controle para o microcontrolador.

3. **Treinamento (`training/`)**
   Contém o código e scripts utilizados para explorar o treinamento de modelos personalizados com dados de voz do dataset [Google Speech Commands](https://research.google.com/audioset/download.html). Embora o modelo embarcado não tenha sido utilizado na versão final, esse diretório registra as tentativas de abordagem local com TensorFlow.

## Estrutura do Projeto

	.
	├── esp32ino/ # Código final que roda no ESP32
	├── server/ # Código do servidor que processa os áudios e envia comandos
	└── training/ # Código de treinamento com dados de voz do Google

## Componentes Utilizados

- **ESP32 DevKit v1**
- **Microfone digital INMP441**
- **LED comum**
- **Servidor local com Python 3**
- **Biblioteca Vosk para reconhecimento de voz**

## Funcionamento

1. O ESP32 captura áudio do microfone via protocolo **I²S**.
2. Os dados são enviados via socket para o servidor local.
3. O servidor reconhece os comandos de voz ("on" ou "off") e envia a resposta ao ESP32.
4. O ESP32 aciona ou desliga o LED com base no comando recebido.


## Observações

Durante o desenvolvimento, diferentes abordagens foram testadas, incluindo o uso do **TensorFlow micro_speech** diretamente no ESP32. Devido a limitações de hardware e problemas de compatibilidade, a arquitetura foi modificada para delegar o reconhecimento de voz ao computador, garantindo maior precisão e flexibilidade.
