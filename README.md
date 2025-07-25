# 2V2PL
Implementação do protocolo 2V2PL 

 Objetivo do trabalho: O trabalho prático representará a implementação do protocolo conservador 2V2PL, para controle
de concorrência, com suporte à múltipla granulosidade de bloqueio, detecção e resolução de
deadlocks. Na implementação do protocolo, a entrada deverá ser uma sequencia de operações
de transações distintas. A saída deve mostrar a sincronização correta das operações do
escalonamento fornecido. A detecção de deadlocks deverá utilizar a estratégia do grafo de
espera.

Nosso sistema simula um controle de concorrencia em sistemas de bando de dados que utiliza o protocolo 2V2PL (Conservador de bloqueios de duas fases com multiplas granularidade).  suportando
*  Multiplas granularidade de bloqueio
*  Encontra e resolve deadlocks por grafo de espera com networkx
*  Analisa escalabilidade e serializabilidade

# Conceitos envolvidos
## Protocolo 2V2PL
O protocolo 2V2PL garante serializabilidade ao impor duas fases nas transações:
Fase de Crescimento: a transação pode solicitar locks.
Fase de Encolhimento: após liberar um lock, não pode mais adquirir novos.
## Multipla granualaridade
 A hierarquia de objetos controlados é composta por niveis de granularidade 
 - BD
 - área
 - tabela
 - pagina
 - tupla
 Bloqueios aplicados em um nível afetam os objetos ascendentes e descendentes na hierarquia.

## Funcionalidades por arquivo
2V2PL/
- **`main.py`**: Lê o escalonamento digitado pelo usuário, transforma em operações, executa o protocolo e exibe o resultado final.
- **`protocolo.py`**: Aplica as regras do 2V2PL, gerencia o grafo de espera, identifica ciclos (deadlocks) e resolve conflitos abortando a transação mais recente.
- **`bloqueios.py`**: Implementa todos os tipos de bloqueio (RL, WL, UL, CL, IRL, IWL), além das funções de propagação para níveis hierárquicos e liberação de bloqueios.
- **`objetos.py`**: Cria a estrutura hierárquica do banco com múltiplos níveis. Também controla os bloqueios associados a cada objeto.
- **`operations.py`**: Define as operações do escalonador (leitura, escrita, atualização e commit) com mapeamento simbólico (R → Read, W → Write, etc).
- **`transactions.py`**: Define a estrutura e métodos associados às transações (como `T1`, `T2`, etc), incluindo identificadores e índices de controle.

# Requisitos

Biblioteca Networkx (pip install networkx)

# Funcionamento interno
* hierarquia do objetos
<img width="8954" height="1458" alt="grafo" src="https://github.com/user-attachments/assets/e4e75cba-dce0-4153-a473-f833c3269960" />



# Fluxo de protocolo
- Parser converte schedule em operações #

- Protocolo tenta adquirir bloqueios

em caso de conflito:

- Adiciona aresta no grafo de espera

- Verifica ciclos (deadlock)

- Se deadlock detectado, aborta transação mais recente

- Commit converte bloqueios para Certify Locks

# Tipos de bloqueio 
|Bloqueio	| Descrição | Nivel |
|---------|-----------|--------|
| RL	| Read Lock | Objeto |
| WL |	Write Lock | Objeto |
| UL |	Update Lock | Objeto |
| CL |	Certify Lock | Objeto |
| IRL |	Intention Read Lock | hierarquico |
|IWL |	Intention Write Lock | hierarquico |

# Saida do Sistema

- Objetos disponíveis no esquema: ['BD', 'AA1', 'AA2', 'TB1', 'TB2', 'TB3', 'TB4', 'PG1', 'PG2', 'PG3', 'PG4', 'PG5', 'PG6', 'PG7', 'PG8', 'TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'TP6', 'TP7', 'TP8', 'TP9', 'TP10', 'TP11', 'TP12', 'TP13', 'TP14', 'TP15', 'TP16']

- Digite o schedule:

caso for correto
Schedule correto

caso não o escalonamento se meter em um deadlock
Por exemplo

 Aresta adicionada: T2 -> T1

 Grafo de espera:
    T2 -> T1

 Aresta adicionada: T1 -> T2

 Grafo de espera:
    T1 -> T2
    T2 -> T1

 Deadlock detectado! Abortar...

 Resultado: T2 se meteu num deadlock e foi abortada!

# Autores
- Diego Lopes, UFC (Universidade Federal do Ceará) @Mrdiegolopes 
- Jardel Araujo, UFC (Universidade Federal do Ceará) @Araujojardel
