import json
import os
import sys

TASKS_FILE = "tasks.json"

def carregar_tarefas():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        try: 
            return json.load(f)
        except json.JSONDecodeError:
            return []   
        
def salvar_tarefas(tarefas):
    with open(TASKS_FILE, "w") as f:
        json.dump(tarefas, f, indent=4)

def adicionar_tarefas(description):
    tarefas = carregar_tarefas()
    task = {"id": len(tarefas) + 1, "description": description, "status": "pendente"}
    tarefas.append(task)
    salvar_tarefas(tarefas)
    print(f"Tarefa adicionada: {task['description']}")

def atualizar_tarefas(id, new_description):
    tasks = carregar_tarefas()
    for task in tasks:
        if task["id"] == id:
            task["description"] = new_description
            salvar_tarefas(tasks)
            print(f"Tarefa atualizada: {task['description']}")
            return
    print(f"Tarefa não encontrada")

def deletar_tarefas(id):
    tasks = carregar_tarefas()
    tasks = [task for task in tasks if task["id"] != id]
    salvar_tarefas(tasks)
    print(f"Tarefa com id {id} deletada")

def mudar_status(id, status):
    valid_status = ["pendente", "fazendo", "feito"]
    if status not in valid_status:
        print(f"Status inválido. Use um dos seguintes: {valid_status}")
        return
    tasks = carregar_tarefas()
    for task in tasks:
        if task["id"] == id:
            task["status"] = status
            salvar_tarefas(tasks)
            print(f"Tarefa {task['id']} agora está marcada como {task['status']}")
            return
    print(f"Tarefa não encontrada")

def listar_tarefas(filter_status=None):
    tasks = carregar_tarefas()
    if filter_status:
        tasks = [task for task in tasks if task["status"] == filter_status]
    if not tasks:
        print("Nenhuma tarefa encontrada")
        return
    for task in tasks:
        print(f"{task['id']}: {task['description']} - {task['status']}")
        
def main():
    if len(sys.argv) < 2:
        print("Uso: python Task_Tracker.py <comando> [opcoes]")
        return
    command = sys.argv[1]

    if command == "adicionar" and len(sys.argv) > 2:
        adicionar_tarefas(" ".join(sys.argv[2:]))
    elif command == "atualizar" and len(sys.argv) > 3:
        atualizar_tarefas(int(sys.argv[2]), " ".join(sys.argv[3:]))
    elif command == "deletar" and len(sys.argv) > 2:
        deletar_tarefas(int(sys.argv[2]))
    elif command == "status" and len(sys.argv) > 3:
         mudar_status(int(sys.argv[2]), sys.argv[3])
    elif command == "listar":
        listar_tarefas()
    elif command == "listar_concluida":
        listar_tarefas("feito")
    elif command == "listar_pendente":
        listar_tarefas("pendente")
    elif command == "listar_fazendo":
        listar_tarefas("fazendo")
    else:
        print("Comando inválido")
        print("adicionar <descricao> - Adiciona uma nova tarefa")
        print("atualizar <id> <nova descricao> - Atualiza a descrição de uma tarefa")
        print("deletar <id> - Deleta uma tarefa")
        print("status <id> <status> - Atualiza o status de uma tarefa")
        print("listar - Lista todas as tarefas")
        print("listar_concluida - Lista todas as tarefas concluídas")
        print("listar_pendente - Lista todas as tarefas pendentes")
        print("listar_fazendo - Lista todas as tarefas em andamento")

if __name__ == "__main__":
    main()