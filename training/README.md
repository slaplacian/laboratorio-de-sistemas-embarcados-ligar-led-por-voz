# Treinamento de Modelo de Reconhecimento de Voz

Este diretório contém os scripts e recursos utilizados para treinar um modelo de reconhecimento de voz capaz de identificar os comandos "on" e "off". O objetivo é gerar um modelo que possa ser integrado ao sistema embarcado para controlar um LED via comandos de voz.

## Dataset Utilizado

O modelo é treinado utilizando o [Google Speech Commands Dataset v0.02](https://www.kaggle.com/datasets/yashdogra/speech-commands/code), que contém milhares de gravações de palavras faladas por diferentes pessoas.

## Como Baixar o Dataset do Kaggle

1. **Crie uma conta no Kaggle**: Acesse [https://www.kaggle.com](https://www.kaggle.com) e registre-se.

2. **Obtenha seu token de API**:
   - Vá para [https://www.kaggle.com/account](https://www.kaggle.com/account).
   - Role até a seção "API" e clique em **"Create New API Token"**.
   - Um arquivo chamado `kaggle.json` será baixado. Guarde-o em um local seguro.

3. **Configure o ambiente local**:
   - Instale a biblioteca do Kaggle:
     ```bash
     pip install kaggle
     ```
   - Mova o arquivo `kaggle.json` para o diretório apropriado:
     - **Linux/Mac**:
       ```bash
       mkdir -p ~/.kaggle
       mv /caminho/para/kaggle.json ~/.kaggle/
       chmod 600 ~/.kaggle/kaggle.json
       ```
     - **Windows**:
       - Crie a pasta `C:\Users\<SeuUsuário>\.kaggle\` e mova o `kaggle.json` para lá.

4. **Baixe o dataset**:
   - Execute o seguinte comando:
     ```bash
     kaggle datasets download -d yashdogra/speech-commands
     ```
   - Extraia o conteúdo:
     ```bash
     unzip speech-commands.zip -d speech_commands
     ```

## Preparação dos Dados

1. **Seleção de Palavras**:
   - O foco é nas palavras **"on"** e **"off"**.
   - Cada uma possui aproximadamente 2.300 gravações.

2. **Adição de Ruído de Fundo**:
   - Para melhorar a robustez do modelo, é recomendável incluir amostras de ruído de fundo.
   - O dataset contém uma pasta `_background_noise_` com arquivos de ruído que podem ser utilizados para essa finalidade.

## Treinamento do Modelo

1. **Pré-processamento**:
   - Os arquivos de áudio são convertidos em representações de espectrograma ou MFCC (Mel-Frequency Cepstral Coefficients) para serem utilizados como entrada do modelo.

2. **Arquitetura do Modelo**:
   - Utiliza-se uma rede neural simples com camadas densas e/ou convolucionais.
   - A saída é uma camada softmax com três classes: "on", "off" e "background".

3. **Treinamento**:
   - O treinamento é realizado utilizando o TensorFlow ou outra biblioteca de aprendizado de máquina.
   - Após o treinamento, o modelo é convertido para um formato compatível com o sistema embarcado, como o TensorFlow Lite.

## 📁 Estrutura dos Arquivos

- `main.py`: Script principal para treinamento do modelo.
- `conversor.py`: Script para converter o modelo treinado para TensorFlow Lite (`.tflite`).
- `runtime.py`: Script para executar e testar localmente a inferência com o modelo `.tflite`.
