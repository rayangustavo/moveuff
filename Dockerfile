FROM debian:bullseye-slim

## Dependências Base ##
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    git \
    jq \
    lsof \
    procps \
    vim \
    build-essential \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

## NodeJS ##
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*
RUN node -v && npm -v

## Foundry ##
RUN curl -L https://foundry.paradigm.xyz | bash && \
    /root/.foundry/bin/foundryup
ENV PATH="/root/.foundry/bin:$PATH"

## Nonodo ##
RUN npm install -g nonodo

## Diretório de trabalho ##
WORKDIR /app
COPY . .

## Instala bibliotecas do Python ##
RUN pip3 install -r requirements.txt

## Inicializa Nonodo ##
RUN chmod +x downloads_nonodo.sh
RUN ./downloads_nonodo.sh

## Expõe porta para conexão com a blockchain ##
EXPOSE 8545

## RUN ##
RUN chmod +x run-dapp.sh
CMD ["./run-dapp.sh"]