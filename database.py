import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
        host="localhost",     # Endereço
        user="root",          # Usuário
        password="senai",     # Senha
        database="estodolist" # Database criado
        )
        cursor =  conexao.cursor(dictionary=True) # Devolve no formato Dict
        # Retorna duas informações: Conexão e cursor
        return conexao, cursor
    
    except Error as erro:
        print(f"ERRO! Falha ao se conectar com o banco de dados: {erro}")
        return None, None 



# ---- Função Inserir tarefa
def inserir_tarefa(nome_tarefa,descricao,categoria,data_prazo,prioridade):
    conexao, cursor = conectar() # Se conectar com BD

    # Verifica se a conexão funcionou
    if conexao is None:
        return False

    try:
        # %s SQL Parametrizado para evitar SQL Injection
        sql = "INSERT INTO tarefa (nomeTarefa,descricao,categoria,dataPrazo,prioridade) VALUES (%s, %s, %s, %s, %s)"
        # Executa o SQL Parametrizado e passa os parâmetros da função via TUPLA
        cursor.execute(sql,(nome_tarefa,descricao,categoria,data_prazo,prioridade))
        # Confirma as alterações
        conexao.commit()     
        # Retornar TRUE para função principal
        return True
    
    except Error as erro:
        print(f"ERRO! Falha ao inserir a tarefa: {erro}")
        return False
    finally:
        cursor.close()
        conexao.close()

# ------------------------------------------------------------
# Retorna todas as tarefas cadastradas no Banco de Dados
def consultar_tarefas():

    # Chama a função Conectar
    conexao, cursor = conectar()

    # Verificar se a conexão falhou
    if conexao is None:
        return [] # Lista Vazia

    try: # Tente executar o comando SQL
        # Selecione todas as colunas da(origem) tabela tarefa;
        sql = """
              SELECT
                idTarefa AS idtarefa,
                dataPrazo AS data_prazo,
                nomeTarefa AS nome_tarefa,
                status,
                descricao,
                categoria,
                prioridade
              FROM tarefa
              """
        # Executa o comando da variável SQL
        cursor.execute(sql)

        # Buscar todas as linhas da consulta executada
        tarefas = cursor.fetchall()

        # Retorna para a programação principal as tarefas
        return tarefas # Lista de Dicionários (DICT)

    except Error as erro: # Se der erro
        print(f"ERRO! Falha ao listar as tarefas: {erro}")
        return [] # Retorna lista vazia em caso de erro

    finally: # Executa sempre dando certo ou não
        cursor.close()  # Encerra o cursor
        conexao.close() # Encerra o conexão

# ------------------------------------------------------
# Essa função marca como Concluída a tarefa indicada
def concluir_tarefa(idtarefa):

    conexao, cursor = conectar()

    if conexao is None:
        return False

    try:
        sql = "UPDATE tarefa SET status = 'Concluída' WHERE idTarefa = %s"
        cursor.execute(sql,(idtarefa,))
        
        conexao.commit() # Confirma a alteração nos dados

        return True

    except Error as erro:
        print(f"ERRO! Falha ao concluir a tarefa: {erro}")
        return False # Retorna Falso em caso de erro
    finally:
        cursor.close()
        conexao.close()


# ---------------------------------------------------------------------------------------------
# Essa função irá editar as informações da tarefa
def alterar_tarefa(idtarefa,nome_tarefa,descricao,categoria,data_prazo,prioridade):

    conexao, cursor = conectar()

    if conexao is None:
        return False

    try:
        sql = """
        UPDATE tarefa 
        SET 
        nomeTarefa = %s,
        descricao = %s,
        categoria = %s,
        dataPrazo = %s,
        prioridade = %s
        WHERE idTarefa = %s
        """

        cursor.execute(sql,(nome_tarefa, descricao, categoria, data_prazo, prioridade, idtarefa))
        
        conexao.commit() # Confirma a alteração nos dados

        return True

    except Error as erro:
        print(f"ERRO! Falha ao editar a tarefa: {erro}")
        return False # Retorna Falso em caso de erro
    finally:
        cursor.close()
        conexao.close()

#-----------------------------------------------------------------------------------------------------------------
#APAGAR TAREFA 
def apagar_tarefa(idtarefa):

    conexao, cursor = conectar()

    if conexao is None:
        return False

    try:
        sql = """
        DELETE FROM tarefa WHERE idTarefa = %s
        """

        cursor.execute(sql,(idtarefa,))
        
        conexao.commit() # Confirma a exclusão nos dados

        return True

    except Error as erro:
        print(f"ERRO! Falha ao excluír a tarefa: {erro}")
        return False # Retorna Falso em caso de erro
    finally:
        cursor.close()
        conexao.close()