# Database to Devs
O Database to Devs é uma ferramenta CLI que cria e gerencia bancos de dados (Hoje apenas MYSQL) usando Docker.
O objetivo é ser uma aplicação de demonstração dos recursos do uso do Docker SDK e a interação via programação com o Docker e faz parte dos exemplos da [Formação DevOps](https://www.devopspro.com.br) Pro e do [KubeDev](https://kubedev.io).

---

# Docker Database Manager

Este repositório fornece um script Python para facilitar a criação, listagem e remoção de bancos de dados PostgreSQL e MySQL em containers Docker para ambientes de desenvolvimento.

## Requisitos

- **Docker**: Certifique-se de que o Docker esteja instalado e em execução em seu sistema. [Clique aqui para instalar o Docker](https://docs.docker.com/get-docker/).
- **Python 3.10 ou superior**: O script foi desenvolvido para funcionar com Python 3.10 ou superior.
- **Virtualenv**: Para criar um ambiente virtual em Python e instalar as dependências de forma isolada.

## Instalação


### 1. Criação do Ambiente Virtual

Se você ainda não possui o `virtualenv` instalado, instale-o com:

```bash
pip install virtualenv
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

### 2. Instale as dependências

Após ativar o ambiente virtual, instale as dependências necessárias:

```bash
pip install -r requirements.txt
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

## Dockerfile

Este repositório inclui um `Dockerfile` para construir uma imagem Docker personalizada para rodar o script Python dentro de um container. O `Dockerfile` instala as dependências e configura o ambiente para rodar o script `index.py`.

### Para construir e rodar o container Docker:

1. Construa a imagem:

```bash
docker build -t docker-database-manager .
```

2. Execute o container:

```bash
docker run -it docker-database-manager python3 index.py criar --banco curso_docker --user docker_usr --pwd docker_pwd --root-pwd root_pwd
```

## Exemplo de Saída

Após a execução do comando de criação de banco, a saída esperada será algo como:

```bash
Criando um novo Banco de Dados PostgreSQL.....
Banco de Dados criado:
---------------------------------
ID: <container_id>
Nome do Banco: curso_docker
Porta de Acesso: 5432
Usuário: docker_usr
Senha do Usuário: docker_pwd
---------------------------------
```



