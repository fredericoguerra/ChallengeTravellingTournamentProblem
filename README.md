## Descrição do Problema de Otimização Combinatório (POC)
Os campeonatos esportivos de longo duração em que os clubes cuprem uma tabela extensa com jogos em vários locais diferentes causa muitos interesses da mídia e telespectadores durante a ocorrência desses eventos devido a alta competitividade entre os times e dificuldade de soberania de um time frente aos demais. Além disso, esses campeonatos movimentam altíssimos valores devido aos custos de deslocamento e logística dos times no cumprimento da tabela de jogos. Essa, por sua vez, se mal escalonada pode gerar uma série de desigualdades entre as equipes, como ,por exemplo, o maior deslocamento de um time em relação aos demais ou a ocorrência de uma sequência de jogos em seu território ou longe dele.

Esse problema de organização de jogos em um intervalo de datas e diferentes locais é conhecido na literatura como um problema de otimização combinatório chamado de Problema de Programação de Jogos (PPF) ou Traveling Tournament Problema (TTP). O objetivo principal na resolução desse problema é minimizar a distância total percorrida ou o tempo de deslocamento pelos times envolvidos, ao mesmo tempo que as restrições do campeonato são satisfeitas. 

[Concilio (2000)](https://www.scielo.br/j/ca/a/4TVYGSpTByRqbHzxpHWjTqR/?lang=pt) definiu a expressão para o número de combinações a partir de $n$ times participantes:

$(n-1)!(n-3)!(n-5)!...(n-(n-1))!2^{(n-1)\times\frac{n}{2}}$

A partir dessa equação e da tabela 1, pode-se perceber como o número de combinações extrapola facilmente. [Easton (2003)](https://link.springer.com/chapter/10.1007/978-3-540-45157-0_6) classificou o problema TTP como NP-completo. [Clemens (2010)](https://reader.elsevier.com/reader/sd/pii/S0304397510005451?token=FC546959CA8285EAFBB9A83CAB795A9BEE9E4F57CBEAFD264E3AFD57CC55CAC77C3289E033C68AFF2CAE8913B042860C&originRegion=us-east-1&originCreation=20220705122102) provou que o problema TTP pode ser reduzido polinomialmente a partir do problema NP-difícil 3-SAT a partir da decomposição de grafos acíclicos.

|Número de Participantes|Número de Combinações|
|-|-|
|$2$|$2$|
|$4$|$384$|
|$6$|$2,36 \times 10^{7}$|
|$8$|$9,7410 \times 10^{14}$|
|$10$|$4,6331 \times 10^{25}$|
|$12$|$3,8785 \times 10^{39}$|
|$14$|$8,1039 \times 10^{56}$|
|$16$|$5,6893 \times 10^{77}$|
|$18$|$1,7383 \times 10^{102}$|
|$20$|$2,9062 \times 10^{130}$|


*Input*. Grupo de $n$ times $T = \{t1, ..., tn\}$; Uma matriz simétrica inteira $n \times n$ representando a distância entre os elementos $d_{ij}$; 

*Output*. Uma matriz $n \times w$ representando os confrontos entre os times ao longo das semanas $w$, onde:

- O maior número de jogos em sequência em casa ou fora de um time é 3.
- A distância total viajada por um time é minimizada.

## Heurística desenvolvida
A seguir, são descritas as funções que compoem a solução da heurística implementada.

### F1. heuristic_solution
Dados a matriz *matches_list* com todos pares de jogos possíveis entre os times, o número de times *number_of_teams*, a quantidade de semanas *number_of_weeks* e a matriz de custos *cost_matrix*, a função **heuristic_solution** cria e popula a matriz *schedule* confrontos *number_of_teams* $\times$ *number_of_weeks*. Cada linha $i$ dessa matriz representa a sequência de jogos do time $i + 1$ ao longo das semanas $j$ representadas pelas colunas da matriz. O valor do elemento $m_{i,j}$ na matriz corresponde ao time que a equipe $i$ enfrentará na semana $j$. O time $i$ jogará em casa, caso o valor desse elemento seja positivo, e competirá fora caso o valor seja negativo.

*input.*
```python
matches_list = [(1,2),(1,3),(1,4),(1,5),(1,6),
                (2,1),(2,3),(2,4),(2,5),(2,6),
                (3,1),(3,2),(3,4),(3,5),(3,6),
                (4,1),(4,2),(4,3),(4,5),(4,6),
                (5,1),(5,2),(5,3),(5,4),(5,6),
                (6,1),(6,2),(6,3),(6,4),(6,5)]

matrix_cost = np.array([[0,745,665,929,605,521],
                        [745,0,80,337,1090,315],
                        [665,80,0,380,1020,257],
                        [929,337,380,0,1380,408],
                        [605,1090,1020,1380,0,1010], 
                        [521,315,257,408,1010,0]])
                        
number_of_teams = matrix_cost.shape[1]
number_of_weeks = int(((2*number_of_teams) - 2)/2)
```
*output.*
```python
schedule = [[ 2.  3.  4.  5.  6.]
            [-1.  4.  3.  6.  5.]
            [ 4. -1. -2. -4. -4.]
            [-3. -2. -1.  3.  3.]
            [ 6. -6. -6. -1. -2.]
            [-5.  5.  5. -2. -1.]]
```
### F2. fix_repeated_matches

Como pode ser visto acima na matriz schedule, é possível haver confrontos repetidos entre dois times, o que não é permitido e compete a um grave não cumprimento da restrição de enfretamente unitário entre dois times em um mesmo turno. Para solucionar isso, a função **fix_repeated_matches** objetiva corrigir ou diminuir a ocorrência de eventos repetidos na tabela de confrontos permutando times dentro de uma mesma semana para os casos de repetição.

*input.*
```python
schedule = [[ 2.  3.  4.  5.  6.]
            [-1.  4.  3.  6.  5.]
            [ 4. -1. -2. -4. -4.]
            [-3. -2. -1.  3.  3.]
            [ 6. -6. -6. -1. -2.]
            [-5.  5.  5. -2. -1.]]
```
*output.*
```python
schedule_ = [[ 2.  3.  4.  5.  6.]
            [-1.  4.  3.  6.  5.]
            [-5. -1. -2. -4. -4.]
            [ 6. -2. -1.  3.  3.]
            [ 4. -6. -6. -1. -2.]
            [-3.  5.  5. -2. -1.]]
```
### F3. add_second_tournament_round

A função **add_second_tournament_round** simplesmente transforma a tabela de turno único de jogos em uma tabela completa de dois turnos, onde os jogos do segundo turno ocorrem na casa do time que foi visitante no primeiro.


*input.*
```python
schedule_ = [[ 2.  3.  4.  5.  6.]
            [-1.  4.  3.  6.  5.]
            [-5. -1. -2. -4. -4.]
            [ 6. -2. -1.  3.  3.]
            [ 4. -6. -6. -1. -2.]
            [-3.  5.  5. -2. -1.]]
```
*output.*
```python
full_heuristic_schedule = [[ 2.  3.  4.  5.  6. -2. -3. -4. -5. -6.]
                           [-1.  4.  3.  6.  5.  1. -4. -3. -6. -5.]
                           [-5. -1. -2. -4. -4.  5.  1.  2.  4.  4.]
                           [ 6. -2. -1.  3.  3. -6.  2.  1. -3. -3.]
                           [ 4. -6. -6. -1. -2. -4.  6.  6.  1.  2.]
                           [-3.  5.  5. -2. -1.  3. -5. -5.  2.  1.]]
```

### F4. Funções de penalidade

Foram desenvolvidas três funções de penalidade para o não atendimento das restrições do problema: (i) *calculate_sequence_matches_penalty*, (ii) *calculate_repeated_matches_penalty* (iii) *calculate_multiple_matches_week_penalty*.

A função (i) calcula o número de occorrências na matriz *full_heuristic_schedule* de sequências de 4 jogos ou mais de um mesmo time em casa ou fora. Essa função retorna um número inteiro *seq_penalty* correspondente ao número de violações da restrição de sequências de jogos em casa/fora de um time. Esse valor é utilizado como penalizador na função de custo $fs$ do problema.

Já a função (ii) computa o número (*repeat_penalty*) de confrontos repetidos entre dois times, mesmo após a aplicação da função F2. Por fim, a função (iii) busca pela frequência de ocorrências em que um mesmo time tem mais de um jogo por rodada, reprensetada pela variável *multiple_penalty*. Ambos os coeficientes de penalidades são utilizados na função de custo $fs$.

### F5. evaluation_function

A função F5, a partir da matriz de custos e dos coeficientes de penalização, calcula o custo total da tabela *full_heuristic_schedule* a partir da seguinte equação:

$$
fs = \sum_{i=1}^{n} c_{i}*(1 + \frac{3 * seq\\_penalty}{2} + 4 * (rep\\_penalty + mult\\_penalty))
$$

### F6. Movimentos de vizinhança

Por fim, na heurística desenvolvida, a função *vnd_explorer* busca em uma iteração de 100 passos uma solução menos custosa $fs'$ através de dois tipos de movimentações: (i) *vnd_swap_homes*: alternando a ordem dos confrontos de casa e fora entre dois times (Tabela 2) e (ii) *vnd_swap_rounds*: alternando duas rodadas da tabela (Tabela 3).

Tabela 02. Exemplo de movimentação de vizinhança utilizando *swap_homes*.
![image](https://user-images.githubusercontent.com/27898822/177353110-21a4db6a-a9d7-4948-8e44-252c5b17afe5.png)

Tabela 03. Exemplo de movimentação de vizinhança utilizando *swap_rounds*.
![image](https://user-images.githubusercontent.com/27898822/177353306-d9cd64f3-eb35-4b60-8530-adab67f3b25a.png)

## Meta-heuristíca aplicada: Iterated Local Search

Foi aplicada a meta-heuristica Iterared Local Search (ILS) no problema a fim de comparar os resultados com a heurística previamente descrita. Abaixo o pseudocódigo do ILS:

```
Algoritmo ILS
  s0 <- SolucaoInicial
  s <- BuscaLocal(s0)
  iter <- 0; {Contador do número de iterações}
  MelhorIter <- Iter; {Iteração em que ocorreu melhora}
  enquanto (iter – MelhorIter < ILSmax)
    iter <- iter + 1
    s’ <- perturbação(s, histórico)
    s” <- BuscaLocal(s’)
    se ( f(s”) < f(s) ) faça
      s <- s”
    fim-se
  fim-enquanto
retorne s
```

### F7. iterated_local_search

A função *iterated_local_search*, a partir da matriz de solução inicial *full_heuristic_schedule* gera uma perturbação na solução utilizando a movimentação de vizinhança *swap_homes* e então faz uma busca local através da função *vnd_explorer* a fim de encontrar alguma melhoria nessa busca local.

## Resultados computacionais

A partir de 10 execuções, foram geradas as médias e desvio-padrão de tempo computacional e dos valores da função de custo, bem como o melhor resultado da heurística e meta-heurística.

Tabela 04. Média e desvio-padrão da função de custo e tempo computacional das soluções para $n$=10.
|$n$|Método|$fs$ ($\mu$)|$fs$ ($\sigma$)|$tempo (\mu)$|$tempo (\sigma)$|
|---|---|---|---|---|---|
|10|Heurística|$9,5788 \times 10^{6}$|$1,8238 \times 10^{6}$|$0,1974$|$0,0109$|
|10|ILS|$5,3740 \times 10^{6}$|$2,3166 \times 10^{6}$|$85,6560$|$1,7109$|

O melhor resultado da função de custo $fs$ encontrado através da Heurística foi $5,3196 \times 10^{6}$, enquanto ao aplicar a meta-heurística ILS o melhor resultado foi $2,8394 \times 10^{6}$.
