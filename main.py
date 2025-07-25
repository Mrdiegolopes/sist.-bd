# main de entrada da simulação 2V2PL

import objetos
import operations
import transactions
import protocolo
from bloqueios import (
    aplicar_leitura,
    aplicar_escrita,
    liberar_bloqueios,
    aplicar_certify,
    verificar_conflito,
)

# banco e a estrutura de objetos
banco = objetos.Objetos('Banco', 'BD')
estrutura = objetos.montar_estrutura(banco, 2, 2, 2, 2)

print("\n Objetos disponíveis no esquema:", list(estrutura.keys()))

entrada = input(" Digite o schedule: ").replace(" ", "")


# Interpreta a string de entrada e monta a lista de operações
def montar_operacoes(schedule_str):
    elementos = list(schedule_str)
    fila = []
    
    for i in range(len(elementos)): # 
        if elementos[i] in ['R', 'W', 'U']:
            tipo_op = elementos[i]
            trans_id = elementos[i + 1]
            caminho = []

            if elementos[i + 3] == 'B':
                caminho.append(elementos[i + 3])
                caminho.append(elementos[i + 4])
            else:
                caminho.append(elementos[i + 3])
                caminho.append(elementos[i + 4])
                caminho.append(elementos[i + 5])
                if elementos[i + 6] != ')':
                    caminho.append(elementos[i + 6])

            fila.append([
                operations.Operation(tipo_op),
                transactions.Transaction(trans_id),
                estrutura[''.join(caminho)]
            ])

        elif elementos[i] == 'C':
            trans_id = elementos[i + 1]
            fila.append([
                operations.Operation('C'),
                transactions.Transaction(trans_id)
            ])

    return fila


# converte o resultado para string 
def formatar_saida(resultado):
    texto = []
    for op in resultado:
        acao = op[0].get_operation()
        trans = op[1].get_index()

        if acao in ['Read', 'Write']:
            texto.append(acao[0])  # R ou W
            texto.append(trans)
            texto.append('(')
            texto.append(op[2].get_id())
            texto.append(')')
        elif acao == 'Commit':
            texto.append('C')
            texto.append(trans)

    return ''.join(texto)

operacoes = montar_operacoes(entrada)
resultado = protocolo.executar_protocolo(operacoes)

# resultado
if isinstance(resultado, str):
    print(f"\n Resultado: {resultado}")
else:
    print(f"\n Schedule correto: {formatar_saida(resultado)}") 

