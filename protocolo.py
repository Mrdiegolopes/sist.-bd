# Implementa o controle de concorrência usando o protocolo 2V2PL com múltiplas granularidades. 
# O protocolo mantém versões diferentes dos objetos para leituras e escritas

import bloqueios
import operations
import transactions
import networkx as nx
import copy


# Imprime o grafo de espera usado para mostrar deadlocks
def mostrar_grafo(g):
    print("\n Grafo de espera:")
    for origem, destino in g.edges():
        print(f"{origem} -> {destino}")
    print("")


# Cria os nós (transações) no grafo de espera
def preparar_nos(grafo, operacoes):
    ja_adicionados = set()
    for op in operacoes:
        nome_transacao = op[1].get_transaction()
        if nome_transacao not in ja_adicionados:
            grafo.add_node(nome_transacao)
            ja_adicionados.add(nome_transacao)


# Verifica se o grafo possui ciclos ou seja, se tem deadlock
def tem_deadlock(grafo):
    return not nx.is_directed_acyclic_graph(grafo)


# Verifica se a transação já escreveu nesse objeto
def ja_escreveu(trans, obj):
    for b in obj.blocos:
        if b[1] == trans.get_transaction() and b[0] == 'WL':
            return True
    return False


# Verifica se alguém tá lendo algo que a transação quer commitar
def leitura_em_andamento(lista, trans):
    objetos_usados = [
        op[2] for op in lista
        if op[0].get_operation() != 'Commit' and op[1].get_transaction() == trans.get_transaction() and op[0].get_operation() == 'Write'
    ]
    for obj in objetos_usados:
        for b in obj.blocos:
            if b[0] in ['RL', 'IRL'] and b[1] != trans.get_transaction():
                return True, b[1]
    return False, None


# Verifica se a transação ainda tem operações pendentes
def ainda_na_fila(pendentes, trans):
    return any(op[1].get_transaction() == trans.get_transaction() for op in pendentes)


# Libera bloqueios após commit
def liberar_tudo(lista, trans):
    for op in lista:
        if op[0].get_operation() != 'Commit':
            bloqueios.liberar_bloqueios(op[2], trans)


# Se tiver deadlock, remove a transação mais recente
def abortar_ultima(executadas, fila):
    historico = []
    for op in executadas:
        if op[1].get_transaction() not in historico:
            historico.append(op[1].get_transaction())
    ultima = historico[-1]
    fila[:] = [op for op in fila if op[1].get_transaction() != ultima]
    return fila, ultima


# Converte bloqueios de escrita em Certify (CL) no commit
def travar_certify(operacoes, trans, k):
    objetos_escritos = [
        op[2] for op in operacoes
        if op[0].get_operation() == 'Write' and op[1].get_transaction() == trans.get_transaction()
    ]
    prontos_para_certify = []
    for obj in objetos_escritos:
        pode_converter = all(
            b[0] not in ['RL', 'IRL'] or b[1] == trans.get_transaction()
            for b in obj.blocos
        )
        if pode_converter:
            prontos_para_certify.append(obj)
    for obj in prontos_para_certify:
        bloqueios.aplicar_certify(obj, trans)


# Se a transação usou update, transforma depois em escrita
def atualizar_para_escrita(obj, trans):
    tid = trans.get_transaction()
    for b in obj.blocos:
        if b == ['UL', tid]:
            b[0] = 'WL'


# Função principal: executa o protocolo
def executar_protocolo(fila_operacoes):
    grafo = nx.DiGraph()
    preparar_nos(grafo, fila_operacoes)
    executadas = []

    while True:
        fila_nova = []

        for idx, op in enumerate(fila_operacoes):
            tipo_op = op[0].get_operation()

            if tipo_op == 'Write':
                ok, travas = bloqueios.verificar_conflito(fila_operacoes, op, 'WL', op[1])
                if ok:
                    bloqueios.aplicar_escrita(op)
                    op[2].converte_version(op[1])
                    executadas.append(copy.deepcopy(op))
                    op[2].version_normal()
                    atualizar_para_escrita(op[2], op[1])
                else:
                    grafo.add_edge(travas, op[1].get_transaction())
                    print(f" Aresta adicionada: {travas} -> {op[1].get_transaction()}")
                    mostrar_grafo(grafo)
                    if tem_deadlock(grafo):
                        print(" Deadlock detectado! Abortar...")
                        fila_operacoes, abortada = abortar_ultima(executadas, fila_operacoes)
                        grafo.remove_node(abortada)
                        return f"{abortada} se meteu num deadlock e foi abortada!"
                    fila_nova.append(op)

            elif tipo_op == 'Read':
                ok, travas = bloqueios.verificar_conflito(fila_operacoes, op, 'RL', op[1])
                if ok:
                    bloqueios.aplicar_leitura(op)
                    if ja_escreveu(op[1], op[2]):
                        op[2].converte_version(op[1])
                        executadas.append(copy.deepcopy(op))
                        op[2].version_normal()
                    else:
                        executadas.append(op)
                else:
                    grafo.add_edge(travas, op[1].get_transaction())
                    if tem_deadlock(grafo):
                        fila_operacoes, abortada = abortar_ultima(executadas, fila_operacoes)
                        grafo.remove_node(abortada)
                        return f"{abortada} se meteu num deadlock e foi abortada!"
                    fila_nova.append(op)

            elif tipo_op == 'Update':
                ok, travas = bloqueios.verificar_conflito(fila_operacoes, op, 'UL', op[1])
                if ok:
                    bloqueios.aplicar_update(op)
                    executadas.append(op)
                else:
                    fila_nova.append(op)

            elif tipo_op == 'Commit':
                leitura_bloqueada, quem = leitura_em_andamento(fila_operacoes, op[1])
                travar_certify(fila_operacoes, op[1], idx)

                if leitura_bloqueada:
                    fila_nova.append(op)
                    grafo.add_edge(quem, op[1].get_transaction())
                    if tem_deadlock(grafo):
                        fila_operacoes, abortada = abortar_ultima(executadas, fila_operacoes)
                        grafo.remove_node(abortada)
                        return f"{abortada} se meteu num deadlock e foi abortada!"
                elif ainda_na_fila(fila_nova, op[1]):
                    if op not in fila_nova:
                        fila_nova.append(op)
                else:
                    liberar_tudo(fila_operacoes, op[1])
                    liberar_tudo(executadas, op[1])
                    grafo.remove_node(op[1].get_transaction())
                    executadas.append(op)

        fila_operacoes = fila_nova
        if not fila_operacoes:
            break

    return executadas