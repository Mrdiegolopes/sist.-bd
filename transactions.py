class Transaction:
    def __init__(self, num: str):
        # guarda a transação no formato padrão T1
        self.nome = f'T{num}'
        self.indice = num

    def get_transaction(self) -> str:
        # retorna como T1
        return self.nome

    def get_index(self) -> str:
        # retorna só o número da transação (ex: 1)
        return self.indice

    def get_tipo(self) -> str: 
        # retorna o identificador 
        return 'T'

    def __repr__(self) -> str: # representação da transação
        return self.nome
