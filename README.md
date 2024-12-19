---

# Docker Database Manager

Este repositório fornece um script Python para facilitar a criação, listagem e remoção de bancos de dados PostgreSQL e MySQL (Descomentar código INDEX.PY) em containers Docker para ambientes de desenvolvimento. Há duas formas de executar o script, diretamente na máquina ou usando container.


### SCRIPT EXECUTADO DIRETO NA MÁQUINA
## Requisitos

- **Docker**: Certifique-se de que o Docker esteja instalado e em execução em seu sistema. [Clique aqui para instalar o Docker](https://docs.docker.com/get-docker/).
- **Python 3.10 ou superior**: O script foi desenvolvido para funcionar com Python 3.10 ou superior.
- **Virtualenv**: Para criar um ambiente virtual em Python e instalar as dependências de forma isolada.

## Instalação Virtualenv
https://virtualenv.pypa.io/en/latest/index.html

### 1. Instalação da biblioteca Docker:

```bash
pip install docker
```

Crie o ambiente virtual:

```bash
virtualenv dockerenv
```

Ative o ambiente virtual:

```bash
source dockerenv/bin/activate  # Para Linux/macOS
dockerenv\Scripts\activate     # Para Windows
```

## Utilização

O script Python fornece três operações principais:

1. **Criar banco de dados**: Cria um novo banco de dados PostgreSQL ou MySQL em um container Docker.
2. **Listar bancos de dados**: Exibe todos os bancos de dados criados no ambiente.
3. **Remover banco de dados**: Remove um banco de dados existente.

### 1. Criar banco de dados

Use o comando abaixo para criar um novo banco de dados:

```bash
python3 index.py criar --banco curso_docker --user docker_usr --pwd docker_pwd --root-pwd root_pwd
```

- `--banco`: Nome do banco de dados (ex: `curso_docker`).
- `--user`: Nome do usuário para o banco de dados (ex: `docker_usr`).
- `--pwd`: Senha do usuário (ex: `docker_pwd`).
- `--root-pwd`: Senha do usuário root do banco de dados (ex: `root_pwd`).

![image](https://github.com/user-attachments/assets/c7aa3ed1-2adc-4e36-9437-afc6aa5885e1)

![image](https://github.com/user-attachments/assets/6552598e-9650-45f4-b5dc-7ede4458a972)

![image](https://github.com/user-attachments/assets/fd016348-44bb-4fbb-9ef0-e70406991c95)



### 2. Listar bancos de dados

Para listar os bancos de dados criados:

```bash
python3 index.py listar
```

Isso exibirá todos os containers com a label `gerador.banco=true`.

### 3. Remover banco de dados

Para remover um banco de dados, você precisa do `ID` do container. Use o comando `listar` para obter o `ID` e, em seguida, execute:

```bash
python3 index.py remover --id <container_id>
```

Substitua `<container_id>` pelo ID do container que deseja remover.



### SCRIPT EXECUTADO NO CONTAINER
## Dockerfile

Este repositório inclui um `Dockerfile` para construir uma imagem Docker personalizada para rodar o script Python dentro de um container. O `Dockerfile` instala as dependências e configura o ambiente para rodar o script `index.py`.

### Para construir e rodar o container Docker:

1. Construção da imagem:

```bash
docker build -t docker-database-manager .
```

2. Execute o container: O docker precisa ter comunicação com do Docker Daemon para realizar a criação do container do DB

```bash
docker run -it -v /var/run/docker.sock:/var/run/docker.sock docker-database-manager:latest criar --banco curso_docker --user docker_usr --pwd docker_pwd --root-pwd root_pwd
```

## Exemplo de Saída

Após a execução do comando de criação de banco, a saída esperada será algo como:


![image](https://github.com/user-attachments/assets/42331798-e65e-4fdc-9e5d-f1019e375e83)



Segue o link da Documentação:
https://docker-py.readthedocs.io/en/stable/


