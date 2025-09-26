# MotoTrack: Sistema de Rastreamento de Motos com RFID

Este repositório contém os componentes da simulação de Internet das Coisas (IoT) para o projeto **MotoTrack**.O objetivo principal do projeto é desenvolver uma aplicação com um **mapa digital interativo** para rastrear e localizar motocicletas em tempo real dentro dos pátios da Mottu, utilizando a tecnologia RFID.

### Visão Geral do Projeto

O problema enfrentado pela Mottu é a ineficiência e a falta de rastreabilidade na organização manual de sua frota de motos em mais de 100 filiais. A solução MotoTrack propõe um sistema onde cada moto recebe uma tag RFID passiva com um ID único. Leitores RFID instalados em zonas estratégicas do pátio (como entrada, saída e áreas de estacionamento) detectam as motos e enviam os dados para um backend desenvolvido em Java com Spring Boot.

A principal forma de visualização desses dados é um **mapa digital interativo** que exibe a localização da moto por zona e seu status (em movimento ou estacionada), permitindo uma gestão eficiente e em tempo real do pátio.

Adicionalmente, o projeto inclui um **dashboard analítico** para a visualização de métricas gerenciais sobre a frota, como a distribuição de motos por ala e o status geral.

### Estrutura da Simulação

Os arquivos nesta entrega representam os diferentes componentes da simulação de IoT:

* `mottu_iot.ino`: O código para o microcontrolador (Arduino) que simula o leitor RFID, responsável por gerar e enviar os dados de localização que alimentariam o mapa.
* `script.py`: Script em Python que atua como uma "ponte", recebendo os dados do microcontrolador (via porta serial) e enviando-os para o backend da aplicação através de requisições HTTP.
* `dashboard_json.py`: O script em Python que gera o **dashboard analítico**. Ele é construído com a biblioteca `Streamlit`.
* `registro-database.json`: Um arquivo JSON exportado do banco de dados usado na entrega para visualizar no dashboard.

### Como Executar o Dashboard Analítico

Enquanto o mapa interativo é a funcionalidade principal da aplicação completa, este repositório permite executar o dashboard analítico de forma independente para demonstração.

**Passo 1: Instale as dependências**

Abra o terminal na pasta do projeto e instale as bibliotecas Python necessárias:

```sh
pip install streamlit pandas seaborn matplotlib
```

### Passo 2: Execute o script do dashboard

No mesmo terminal, utilize o comando `streamlit run`:

```sh
streamlit run dashboard_json.py
