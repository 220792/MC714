# Algoritmos implementados

Relógio Lógico de Lamport
Exclusão mútua (baseado em ficha)
Eleição de Líder (valentão)

# Instruções de Execução

Para executar os algoritmos é necessário ter [Docker](https://docs.docker.com/compose/install/) instalado.

## Relógio Lógico de Lamport

1. Entre na pasta correta: `cd lamport`
2. Builde a imagem da aplicação: `docker build . -t lamport`
3. Crie e execute os containers: `docker-compose up`
4. Acompanhe os logs

## Exclusão mútua

1. Entre na pasta do recurso: `cd mutex_resource`
2. Builde a imagem do recurso: `docker build . -t mutex_resource`
3. Entre na pasta da aplicação: `cd ../mutex`
4. Builde a imagem da aplicação: `docker build . -t mutex`
5. Crie os containers: `docker-compose up`
6. Acompanhe os logs

## Eleição de Líder

1. Entre na pasta correta: `cd leader`
2. Builde a imagem da aplicação: `docker build . -t leader-docker`
3. Crie e execute os containers: `docker-compose up`
4. Acompanhe os logs
