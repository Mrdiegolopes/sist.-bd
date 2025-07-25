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
<img width="8954" height="1458" alt="grafo" src="https://github.com/user-attachments/assets/7a4110e1-e1c4-451b-b12a-7b3b327183b8" />




# Tipos de bloqueio 
|Bloqueio	| Descrição | Nivel |
|---------|-----------|--------|
| RL	| Read Lock | Objeto |
| WL |	Write Lock | Objeto |
| UL |	Update Lock | Objeto |
| CL |	Certificado Lock | Objeto |
| IRL |	intencional Read Lock| hierarquico |
|IWL |	Intencional Write Lock | hierarquico |




# Autores
- Diego Lopes, UFC (Universidade Federal do Ceará) @Mrdiegolopes 
- Jardel Araujo, UFC (Universidade Federal do Ceará) @Araujojardel
