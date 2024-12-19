# # CRIAÇÃO DB POSTGRE

import docker
import secrets
import string
import argparse

# Inicializar cliente Docker
con = docker.from_env()

def gerar_senha():
    secure_str = ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(8)))
    return secure_str

def obter_variavel(lista, chave):
    variaveis = list(filter(lambda x: chave in x, lista))
    if len(variaveis) > 0:
        retorno = variaveis[0]
        return retorno.replace(f"{chave}=","")
    return ''

def exibir_banco(container):
    lista = container.attrs.get("Config").get("Env")
    database_string = obter_variavel(lista, "POSTGRES_DB")
    user_string = obter_variavel(lista, "POSTGRES_USER")
    password_string = obter_variavel(lista, "POSTGRES_PASSWORD")  # Corrigido aqui
    porta_acesso = container.ports.get("5432/tcp")[0].get("HostPort")

    print(f"ID: {container.id}")
    if database_string:
        print(f"Nome do Banco: {database_string}")
    else:
        print(f"Nome do Banco: ")
    print(f"Porta de Acesso: {porta_acesso}")
    if user_string:
        print(f"Usuário: {user_string}")
    if password_string:
        print(f"Senha do Usuário: {password_string}")

def criar_banco(senha_root='', usuario='', senha_usuario='', nome_banco=''):
    print("Criando um novo Banco de Dados PostgreSQL.....")
    parametros = []

    if senha_root == '':
        senha_root = gerar_senha()

    parametros.append(f"POSTGRES_PASSWORD={senha_root}")

    if senha_usuario != '':
        parametros.append(f"POSTGRES_PASSWORD={senha_usuario}")  # Isso deve ser `POSTGRES_USER` e `POSTGRES_PASSWORD` para senha do usuário, mas neste caso, estamos repetindo a senha de root.

    if usuario != '':
        parametros.append(f"POSTGRES_USER={usuario}")  # Aqui é onde o nome do usuário é definido

    if nome_banco != '':
        parametros.append(f"POSTGRES_DB={nome_banco}")

    # Criando o container
    container = con.containers.run("postgres:14.15-alpine3.21", 
        detach=True, 
        publish_all_ports=True, 
        environment=parametros, 
        labels={"gerador.banco": "true"})

    container = con.containers.get(container.id)

    print("Banco de Dados criado:")
    print("---------------------------------")
    exibir_banco(container)
    print("---------------------------------")

def listar_bancos():
    lista_containers = con.containers.list(filters={"label": ["gerador.banco=true"]})

    print("Bancos de Dados criados PostgreSQL:")
    print("---------------------------------")
    for item in lista_containers:
        exibir_banco(item)
        print("---------------------------------")

def remover_banco(id):
    meu_container = con.containers.get(id)
    meu_container.remove(force=True)

# Parser de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('operacao', help='Operação a ser realizada: criar, listar, remover.')
parser.add_argument('--banco', default="", help='Nome do banco de dados.')
parser.add_argument('--root-pwd', default="", help='Senha do root do banco de dados.')
parser.add_argument('--user', default="", help='Nome do usuário.')
parser.add_argument('--pwd', default="", help='Senha do usuário do banco de dados.')
parser.add_argument('--id', default="", help='ID do contêiner para remoção.')

args = parser.parse_args()

# Switch case para operações
match args.operacao:
    case "criar":
        criar_banco(nome_banco=args.banco, senha_root=args.root_pwd, usuario=args.user, senha_usuario=args.pwd)
    case "listar":
        listar_bancos()
    case "remover":
        remover_banco(args.id)
    case _:
        print("Operação desconhecida. Use: criar, listar ou remover.")
