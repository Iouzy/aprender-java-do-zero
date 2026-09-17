# Roadmap Java — contexto, método e plano

> Documento para colar no início de uma conversa com um assistente de IA, para
> retomar a aprendizagem de Java sem perder contexto.

---

## 1. Contexto

- Objetivo: vaga júnior de **Java backend em Portugal** (consultoras, banca, seguros).
- Disponibilidade: 10–20h por semana.
- Sem licenciatura. 12.º ano, curso técnico de Informática de Gestão.
- Ambiente: Ubuntu, JDK 25, terminal + nano (ainda sem IDE).
- Histórico relevante: já comecei e abandonei cursos de programação várias vezes.
  Sempre que o formato foi "seguir instruções", não ficou nada.

---

## 2. Como quero ser ensinado

**Regra principal: nunca me dês o código feito.** Nem quando insisto.

- Dá-me o objetivo, as peças e pistas. Eu escrevo.
- Corrige por cima do que eu colar: aponta o erro e a razão, não a linha corrigida.
- Explica os conceitos com analogias.
- Quando a sintaxe é nova, marca as peças visualmente (setas, numeração) em vez
  de texto corrido. Aprendo melhor assim.
- Quando eu travar, empurra-me para **correr o programa**, não para mais uma
  explicação. O padrão comprovado: os bloqueios desfazem-se a executar, não a ler.
- Diz-me quando eu estiver em loop — a fazer a décima pergunta sobre o mesmo
  assunto sem ter escrito uma linha. Isso acontece e é a minha forma de adiar a
  parte difícil.
- Não avances de tema só porque eu disse que percebi. Pede-me para escrever.
- Sê direto. Prefiro avaliação honesta a encorajamento.
- **Decide tu o próximo passo.** Não me perguntes por onde quero começar —
  lê o estado, escolhe um exercício só e dá-mo. Escolher a matéria é trabalho
  teu; se for meu, escolho sempre o que já sei fazer.

Português de Portugal.

---

## 3. Onde estou

O estado detalhado vive na **bancada** (`java-bancada.html`, separador "Agora").
Isto é o resumo. **Atualizar no fim de cada sessão** — desatualizado não vale nada.

**Fase 1 — Fundamentos.**
Sólido: tipos e casts · `if`/`else if` · `for` · `while` · Scanner · métodos com
parâmetros e retorno · classe, construtor, `this`, `private`, setter com validação.
Por tocar: `switch` · `do-while` · `break`/`continue` · arrays.

Últimos ficheiros (`exercicios/04-reforco/`): `aquecimento1`, `exContagem`,
`somaPares`, `somaIntervalo` — validação com `while` e acumuladores.

### Fraquezas conhecidas, para trabalhares em cima delas

Não são tarefas para eu despachar. São a matéria que ainda não assentou —
mete-as nos exercícios que me deres, quando fizer sentido.

- **Limites de ciclos.** Decidir sozinho se o início e o fim do intervalo entram
  na conta. No `somaPares` o próprio número entra na soma e não sei se foi de
  propósito. Já dei 12550 como certo quando a resposta era 12750.
- **Validação a meio.** No `somaIntervalo`, o `while` só volta a pedir o número
  inicial; se o erro foi no final, fico preso.
- **Encapsulamento furado.** No `Pessoa`, o construtor escreve direto nos campos
  em vez de passar pelo `setIdade()`, por isso aceita uma idade negativa que o
  setter recusaria.
- **`equals()` e `null`.** `genero.equals("M")` rebenta com `null` e devolve a
  resposta errada em silêncio com `"m"` minúsculo.
- **Buffer do Scanner.** `nextInt()` seguido de `nextLine()` ainda me apanha.
- **`this` e âmbito de variáveis.** Percebo quando vejo, não escrevo sem pensar.

### Regras de trabalho

- Um commit por ideia. Mensagem com o **porquê**, não o quê — o quê vê-se no diff.
- Nada de `git add .` Nomear os ficheiros um a um.
- Nenhum commit na bancada sem um commit em `exercicios/` no mesmo dia.
- Um exercício só fica marcado como feito depois de acertar dez previsões
  seguidas no simulador. Ter commit não é saber.
- Erro plantado só em código meu, já commitado. Num ficheiro novo que nunca
  vi, o exercício passa a ser decifrar código estranho.
- Compilar sempre com `jc`, nunca com `javac` à mão — é o que grava as
  versões e os erros (ver `ferramentas/README.md`).

---

## 4. Roadmap

Estimativas para 10–20h/semana. Contam com o tempo de esquecer e reaprender.

### Fase 1 — Fundamentos · 2-3 semanas
Tipos, operadores, casting. `if`/`else if`, **`switch`**. `for`, **`while`**,
**`do-while`**, `break`, `continue`. Métodos: parâmetros, retorno, `void`,
âmbito, sobrecarga. **Arrays** e iteração.


### Fase 2 — POO · 4-6 semanas
Classes, objetos, campos, métodos de instância, `this`, construtores,
`private`, encapsulamento · sobrecarga de construtores · `static` · `final` · herança (`extends`,
`super`, `@Override`) · classes abstratas · interfaces · polimorfismo ·
composição vs. herança · `equals()` + `hashCode()` + `toString()` · enums ·
packages · records.

**Prioridade máxima em entrevista:** interface vs. classe abstrata, e composição
vs. herança. São perguntas quase garantidas.

Projeto da fase: sistema bancário simples — `Conta` como base, `ContaPoupanca` e
`ContaCorrente` a herdar, `Cliente` a compor.

### Fase 3 — Core Java · 3-4 semanas
`List` / `ArrayList` / `LinkedList` · `Set` / `HashSet` / `TreeSet` ·
`Map` / `HashMap` / `TreeMap` · `Queue`, `Deque` · `Iterator` · generics ·
`Comparable` / `Comparator`.

Exceções: `try`/`catch`/`finally`, `throw`, `throws`, checked vs. unchecked,
exceções próprias.

Java moderno: lambdas · interfaces funcionais · **Streams** (`filter`, `map`,
`collect`, `reduce`) · `Optional` · method references · API de datas.

Streams aparecem em todo o código atual. Não é opcional.

### Fase 4 — Git, Maven, IntelliJ · 1-2 semanas
Git: clone, add, commit, push, pull, branch, merge, conflitos, `.gitignore`,
mensagens de commit decentes, pull requests.
Maven: `pom.xml`, dependências, ciclo de build, `mvn clean/test/package`, gerar `.jar`.
IntelliJ a sério: debugger, refactor, atalhos.

É aqui que largo o `javac` e o nano.

### Fase 5 — Testes · 1-2 semanas
JUnit 5: testes unitários, assertions, ciclo de vida, testes parametrizados.
Mockito: mock, stub, verify. Noções de testes de integração.

### Fase 6 — Clean Code e SOLID · 1-2 semanas
Nomes, métodos curtos, responsabilidade única, evitar duplicação, separação de
responsabilidades. SOLID — reconhecer os problemas no meu próprio código, não
decorar as definições.

### Fase 7 — SQL e PostgreSQL · 3-4 semanas
`SELECT`, `INSERT`, `UPDATE`, `DELETE` · `WHERE`, `ORDER BY`, `GROUP BY`,
`HAVING` · `JOIN` · subqueries.
Conceitos: tabelas, chaves primárias e estrangeiras, constraints, relações,
índices, transações, normalização.
PostgreSQL instalado e a correr. JDBC para ver a ligação crua antes do JPA.

Quase todas as vagas pedem SQL. Muitas empresas portuguesas correm Oracle, mas
o que se aprende em PostgreSQL transfere-se.

### Fase 8 — Spring Boot · 3-4 semanas
IoC e injeção de dependências · beans · application context · configuração.
Estrutura de um projeto Spring Boot · `application.properties` · perfis.
`@Component`, `@Service`, `@Repository`, `@Configuration`, `@Bean`, `@Autowired`
— **preferir injeção por construtor**.

### Fase 9 — REST APIs · 2-3 semanas
HTTP: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
Status codes: 200, 201, 204, 400, 401, 403, 404, 409, 500.
`@RestController`, mapeamentos, `@PathVariable`, `@RequestParam`, `@RequestBody`.
**DTOs** — e porque não se expõem entidades diretamente.
Validação: `@NotNull`, `@NotBlank`, `@Size`, `@Email`, `@Min`, `@Max`.
Tratamento global de erros, respostas de erro consistentes.
Documentação com OpenAPI/Swagger.

### Fase 10 — JPA e Hibernate · 2-3 semanas
Entidades, IDs, repositórios, queries, transações.
Relações: `@OneToOne`, `@OneToMany`, `@ManyToOne`, `@ManyToMany`.
Hibernate: persistence context, lazy vs. eager, dirty checking, **problema N+1**.
Spring Data JPA: `JpaRepository`, query methods, `@Query`, paginação, ordenação.

O N+1 é *a* pergunta de entrevista sobre JPA.

### Fase 11 — Spring Security · 2 semanas
Hashing de passwords · autenticação vs. autorização · roles e permissões · JWT ·
filtros de segurança · CORS · CSRF.
Fluxo: registar → login → token → pedidos autenticados.

### Fase 12 — Arquitetura · 1-2 semanas
Camadas: controller → service → repository → base de dados.
Separação de responsabilidades · padrão DTO · inversão de dependências.
Padrões úteis (poucos): Factory, Strategy, Builder. E saber **quando não usar** um.

### Fase 13 — Docker e deployment · 2 semanas
Imagens, containers, Dockerfile, Docker Compose, portas, volumes, variáveis de
ambiente. Levantar Spring Boot + PostgreSQL com um comando.
Deployment: variáveis de ambiente, configuração de produção, logs, HTTPS.

Não é preciso aprender AWS. É preciso conseguir dizer: tenho uma app Spring Boot
e uma PostgreSQL, e sei pô-las a correr num servidor.

### Fase 14 — Projeto principal · em paralelo desde a fase 8
Uma API REST completa, com domínio real (encomendas, reservas, inventário,
finanças pessoais). Não uma lista de tarefas.

Stack: Java · Spring Boot · Spring Security · Spring Data JPA · Hibernate ·
PostgreSQL · JUnit · Mockito · Maven · Git · Docker · OpenAPI.

Tem de incluir: autenticação e autorização · JWT · DTOs · validação · tratamento
de exceções · paginação, filtros e ordenação · testes · Docker · documentação da
API · README a sério · histórico de commits legível.

O README com: o que é, funcionalidades, stack, arquitetura, como correr,
documentação da API, variáveis de ambiente, exemplos.

Commits ao longo de meses, não trinta num dia.

### Fase 15 — Algoritmos · contínuo, prioridade baixa
Arrays, strings, HashMap, HashSet, stack, queue, lista ligada, pesquisa binária,
ordenação, recursão, árvores. Complexidade: O(1), O(log n), O(n), O(n log n), O(n²).

**Baixa prioridade para o mercado português.** As consultoras raramente fazem
LeetCode a júniores. Só sobe de prioridade para produto (Farfetch, OutSystems,
Feedzai) ou multinacionais.

### Fase 16 — Preparação de entrevista · 2-3 semanas
Responder sem consultar documentação:

**Java** — `==` vs `.equals()` · `equals()` + `hashCode()` · `ArrayList` vs
`LinkedList` · como funciona um `HashMap` · interface vs. classe abstrata ·
composição vs. herança · exceções checked vs. unchecked · generics · streams ·
`Optional` · objetos imutáveis · records · `final` · `static`.

**JVM** — JDK vs. JRE vs. JVM · heap vs. stack · garbage collector · class loading.

**Spring** — injeção de dependências · IoC · beans · controllers, services,
repositories · REST · DTOs · JPA · Hibernate · transações · lazy vs. eager ·
N+1 · Spring Security · JWT.

Depois: entrevistas simuladas. Perguntas do género *"a tua API está de repente a
fazer 10.000 queries à base de dados — o que pode estar a acontecer?"*

---

## 5. Calendário realista

| Fase | Semanas | Acumulado |
|---|---|---|
| 1. Fundamentos | 2-3 | mês 1 |
| 2. POO | 4-6 | mês 1-2 |
| 3. Core Java | 3-4 | mês 2-3 |
| 4. Git + Maven | 1-2 | mês 3 |
| 5. Testes | 1-2 | mês 3 |
| 6. Clean Code + SOLID | 1-2 | mês 4 |
| 7. SQL | 3-4 | mês 4-5 |
| 8-9. Spring + REST | 5-7 | mês 5-6 |
| 10. JPA | 2-3 | mês 7 |
| 11. Security | 2 | mês 7 |
| 12-13. Arquitetura + Docker | 3-4 | mês 8 |
| 14. Projeto | paralelo | mês 6-9 |
| 16. Entrevistas | 2-3 | mês 9 |

**8 a 10 meses.** Fazer os fundamentos depressa não antecipa o fim — o Spring
Boot demora o que demora.

---

## 6. Mercado

**Consultoras** (contratam mais júniores, porta de entrada mais provável):
Novabase, Noesis, Critical Software, Deloitte, Accenture, Devoteam, Glintt.
**Banca:** Millennium, CGD, Santander, Novo Banco.
**Seguros:** Fidelidade, Ageas.
**Produto:** Farfetch, OutSystems, Feedzai.

As consultoras pagam menos e o trabalho é menos interessante, mas dão dois anos
de experiência que valem mais do que qualquer certificado.

Java 17 e 21 são as versões em produção na maioria das empresas portuguesas.
Spring Boot 3.x.

---

## 7. Nota final

Este documento não me ensina Java. Só a escrita de código o faz.

Um roadmap detalhado dá exatamente a mesma sensação de progresso que ler um
capítulo: zero linhas escritas, e a sensação de ter avançado. Foi assim que
abandonei cursos antes.

Regra: não voltar a este ficheiro para o rever ou melhorar até ao fim da fase 2.
