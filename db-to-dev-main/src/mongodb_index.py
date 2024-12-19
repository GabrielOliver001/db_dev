# Criação do MongoDB

import docker
import secrets
import string
import argparse
import time

# Inicializar cliente Docker
con = docker.from_env()

def gerar_senha():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))

def exibir_banco(container):
    porta_info = container.ports.get("27017/tcp")
    if not porta_info:
        print(f"ID: {container.id}")
        print("Porta ainda não mapeada. Aguarde ou verifique o status do container.")
        return

    porta_acesso = porta_info[0].get("HostPort")
    env_vars = container.attrs.get("Config").get("Env")
    root_pwd = next((var.split("=")[1] for var in env_vars if var.startswith("MONGO_INITDB_ROOT_PASSWORD")), "")
    root_user = next((var.split("=")[1] for var in env_vars if var.startswith("MONGO_INITDB_ROOT_USERNAME")), "root")

    print(f"ID: {container.id}")
    print(f"Porta de Acesso: {porta_acesso}")
    print(f"Usuário: {root_user}")
    print(f"Senha: {root_pwd}")

def criar_banco(senha_root='', usuario='', porta=27017):
    if not senha_root:
        senha_root = gerar_senha()
    if not usuario:
        usuario = "root"

    container = con.containers.run(
        "mongo:5.0",
        detach=True,
        publish_all_ports=True,
        environment={
            "MONGO_INITDB_ROOT_USERNAME": usuario,
            "MONGO_INITDB_ROOT_PASSWORD": senha_root
        },
        labels={"gerador.banco": "true"}
    )

    # Aguardar mapeamento da porta
    for _ in range(5):
        container.reload()
        if container.ports.get("27017/tcp"):
            break
        time.sleep(1)

    print("Banco MongoDB criado:")
    print("----------------------------")
    exibir_banco(container)
    print("----------------------------")

def listar_bancos():
    containers = con.containers.list(filters={"label": "gerador.banco=true"})
    print("Bancos MongoDB criados:")
    for container in containers:
        print("----------------------------")
        exibir_banco(container)
    print("----------------------------")

def remover_banco(container_id):
    container = con.containers.get(container_id)
    container.remove(force=True)
    print(f"Container {container_id} removido com sucesso.")

# Parser de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('operacao', help='Operação a ser realizada: criar, listar, remover.')
parser.add_argument('--root-pwd', default="", help='Senha do root (opcional).')
parser.add_argument('--user', default="", help='Usuário root (opcional).')
parser.add_argument('--porta', default=27017, type=int, help='Porta de acesso (opcional).')
parser.add_argument('--id', default="", help='ID do container para remoção.')

args = parser.parse_args()

# Execução com base na operação
if args.operacao == "criar":
    criar_banco(senha_root=args.root_pwd, usuario=args.user, porta=args.porta)
elif args.operacao == "listar":
    listar_bancos()
elif args.operacao == "remover":
    if not args.id:
        print("Erro: O parâmetro --id é necessário para remover um banco.")
    else:
        remover_banco(args.id)
else:
    print("Operação inválida. Use criar, listar ou remover.")
