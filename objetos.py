# classe representando BD, área, tabela, pag, tupla.

tipos_de_objeto = ['Banco', 'Area', 'Tabela', 'Pagina', 'Tupla']  

class Objetos:
    def __init__(self, tipo, nome):
        # se o tipo venha como string tupla, converte pro índice da lista
        if not str(tipo).isnumeric():
            tipo = tipos_de_objeto.index(tipo)

        self.nome = nome    # objeto como:TP1, PG2...
        self.tipo = tipos_de_objeto[tipo] #nome do tipo textual
        self.nivel = tipo       # posicao na hierarquia 
        self.ligacoes = {t: [] for t in tipos_de_objeto} 
        self.blocos = []       #lista de bloqueios ativos
        self.versao = 'Antiga'    # estado atual 

    def converte_version(self, transacao):
        self.versao = transacao

    def version_normal(self):
        self.versao = 'Antiga'

    def get_id(self):
        return self.nome

    def get_tipo(self):
        return 'OB'

    def get_index(self):
        return self.nivel

    def __repr__(self):
        return f"{self.nome} - versão {self.versao}"

    def __str__(self):
        return f"{self.nome} - versão {self.versao}"


# conecta um objeto com superiores na hierarquia
def conectar_objetos(pai: Objetos, filho: Objetos):
    pai.ligacoes[filho.tipo].append(filho)
    filho.ligacoes[pai.tipo].append(pai)

    if pai.nivel > 0:
        return conectar_objetos(pai.ligacoes[tipos_de_objeto[pai.nivel - 1]][0], filho)


# monta banco completo de acordo nas quantidades informadas
def montar_estrutura(banco: Objetos, qtd_tuplas, qtd_paginas, qtd_tabelas, qtd_areas):
    estrutura = {banco.nome: banco}

    # Criação das áreas
    for i in range(qtd_areas):
        area = Objetos('Area', f'AA{i+1}') # cria area
        conectar_objetos(banco, area) # conecta area ao banco
        estrutura[area.nome] = area

    # tabelas por area
    t_id = 1 # contador de tabelas
    for area in banco.ligacoes['Area']:
        for _ in range(qtd_tabelas):
            tabela = Objetos('Tabela', f'TB{t_id}') # cria tabela
            conectar_objetos(area, tabela)
            estrutura[tabela.nome] = tabela
            t_id += 1 # incrementa contador de tabelas

    # paginas por tabela
    p_id = 1
    for area in banco.ligacoes['Area']:
        for tabela in area.ligacoes['Tabela']:
            for _ in range(qtd_paginas):
                pagina = Objetos('Pagina', f'PG{p_id}') # cria pagina
                conectar_objetos(tabela, pagina)
                estrutura[pagina.nome] = pagina
                p_id += 1 # incrementa contador de paginas

    # Tuplas por página
    tupla_id = 1 
    for area in banco.ligacoes['Area']:
        for tabela in area.ligacoes['Tabela']:
            for pagina in tabela.ligacoes['Pagina']:
                for _ in range(qtd_tuplas):
                    tupla = Objetos('Tupla', f'TP{tupla_id}') # cria tupla
                    conectar_objetos(pagina, tupla) # conecta tupla a pagina
                    estrutura[tupla.nome] = tupla
                    tupla_id += 1 # incrementa contador de tuplas

    return estrutura