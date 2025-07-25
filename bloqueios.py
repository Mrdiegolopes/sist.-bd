# funções que realiza as verificações, aplicações, liberação de bloqueio na hierarquia de granularidade

from objetos import Objetos
import transactions

# Aplica bloqueio de leitura e propaga intenção de leitura para os níveis acima
def aplicar_leitura(info):
    trans = info[1].get_transaction()
    alvo = info[2]
    alvo.blocos.append(['RL', trans])

    # Sobe adc IRL para os niveis restantes na hierarquia
    acima = list(alvo.ligacoes.keys())[:alvo.nivel][::-1]
    for tipo in acima:
        irl = ['IRL', trans]
        alvo.ligacoes[tipo][0].blocos.append(irl)

    # aplica RL no alvo,desce na hirearquia adc RL nos demais
    abaixo = list(alvo.ligacoes.keys())[alvo.nivel+1:]
    for tipo in abaixo:
        for obj in alvo.ligacoes[tipo]:
            obj.blocos.append(['RL', trans])


# aplica bloqueio de escrita e sobe intenção de escrita
def aplicar_escrita(info):
    trans = info[1].get_transaction()
    alvo = info[2]
    alvo.blocos.append(['WL', trans])

    acima = list(alvo.ligacoes.keys())[:alvo.nivel][::-1]
    for tipo in acima:
        alvo.ligacoes[tipo][0].blocos.append(['IWL', trans])

    abaixo = list(alvo.ligacoes.keys())[alvo.nivel+1:]
    for tipo in abaixo:
        for obj in alvo.ligacoes[tipo]:
            obj.blocos.append(['WL', trans])


# aplica bloqueio de update e sobe intenção de update
def aplicar_update(info):
    trans = info[1].get_transaction()
    alvo = info[2]
    alvo.blocos.append(['UL', trans])

    acima = list(alvo.ligacoes.keys())[:alvo.nivel][::-1]
    for tipo in acima:
        alvo.ligacoes[tipo][0].blocos.append(['IUL', trans])

    abaixo = list(alvo.ligacoes.keys())[alvo.nivel+1:]
    for tipo in abaixo:
        for obj in alvo.ligacoes[tipo]:
            obj.blocos.append(['UL', trans])


# libera todos os bloqueios de uma transação
def liberar_bloqueios(obj, transacao):
    tid = transacao.get_transaction()

    # remove do proprio objetos
    obj.blocos = [b for b in obj.blocos if b[1] != tid]

    # remove os obj que estão acima 
    acima = list(obj.ligacoes.keys())[:obj.nivel][::-1]
    for tipo in acima:
        obj.ligacoes[tipo][0].blocos = [b for b in obj.ligacoes[tipo][0].blocos if b[1] != tid]

    # remove os que estão abaixo
    abaixo = list(obj.ligacoes.keys())[obj.nivel+1:]
    for tipo in abaixo:
        obj.ligacoes[tipo][0].blocos = [b for b in obj.ligacoes[tipo][0].blocos if b[1] != tid]


# transforma bloqueios WL em CL e propaga ICL para os demais
def aplicar_certify(obj, transacao):
    tid = transacao.get_transaction()

    # atualiza o bloqueio direto
    for b in obj.blocos:
        if b == ['WL', tid]:
            b[0] = 'CL'

    # Atualiza os niveis acima
    acima = list(obj.ligacoes.keys())[:obj.nivel][::-1]
    for tipo in acima:
        for b in obj.ligacoes[tipo][0].blocos:
            if b == ['IWL', tid]:
                b[0] = 'ICL'

    # também os abixo (se existir)
    abaixo = list(obj.ligacoes.keys())[obj.nivel+1:]
    for tipo in abaixo:
        for b in obj.ligacoes[tipo][0].blocos:
            if b == ['IWL', tid]:
                b[0] = 'ICL'


# ver se um bloqueio pode ser concedido
def verificar_conflito(agenda, atual, tipo_req, transacao):
    mesmos_objetos = []

    for op in agenda:
        if len(op) == 3 and op[2].get_id() == atual[2].get_id():
            mesmos_objetos.append(op)

    if not mesmos_objetos:
        return True, None

    obj = mesmos_objetos[0][2]
    tid = transacao.get_transaction()

    # ver conforme o tipo de lock
    for b in obj.blocos:
        dono = b[1]
        cod = b[0]
        if tipo_req == 'RL' and cod in ['CL', 'ICL', 'UL', 'IUL'] and dono != tid: # 
            return False, dono
        if tipo_req == 'WL' and cod in ['CL', 'ICL', 'WL', 'IWL', 'UL', 'IUL'] and dono != tid:
            return False, dono
        if tipo_req == 'UL' and cod in ['WL', 'IWL', 'UL', 'IUL'] and dono != tid:
            return False, dono

    donos = [b[1] for b in obj.blocos]
    return True, donos