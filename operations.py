# classe que define as operações basicas ser realizado no escalonador
class Operation:
    def __init__(self, tipo: str):
        self.operation = self._definir_operacao(tipo)

    def _definir_operacao(self, tipo: str) -> str:

        # letras da op basicas .
        tipos_op = {
            'R': 'Read',  # leitura
            'W': 'Write',  # escrita
            'U': 'Update',  # atualização
            'C': 'Commit'  # commit
        }

        return tipos_op.get(tipo.upper(), 'Operação Inválida')

    def get_operation(self) -> str:
        # retorna o tipo da operação como string
        
        return self.operation

    def get_tipo(self) -> str:

        # retorno o identificador do tipo de classe 
        return 'OP'

    def __str__(self) -> str:
        return f'Operação = {self.operation}'

    def __repr__(self) -> str:
        return f'Operação = {self.operation}'