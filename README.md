# aprender-java-do-zero

> Repositório de aprendizagem. Todo o código aqui foi escrito de raiz, sem copiar.

<!-- ESCREVE TU: duas ou três linhas. Quem és, quando começaste, e qual é o
     objetivo (vaga júnior de Java backend). Escreve como se fosse um
     recrutador a ler — porque vai ser. -->

---

## Ambiente

| | |
|---|---|
| Sistema | Ubuntu |
| JDK | 25 |
| Editor | nano |
| Compilação e execução | terminal |

<!-- ESCREVE TU: uma frase a explicar porque estás em nano e não em IDE.
     A razão é boa — di-la por palavras tuas. -->

---

## Como compilar e correr

Dentro da pasta do exercício:

```bash
javac Ola.java
java Ola
```

Compilar para uma pasta separada, sem sujar a pasta do código-fonte:

```bash
javac -d out Ola.java
java -cp out Ola
```

Quando são dois ficheiros que dependem um do outro:

```bash
javac Pessoa.java Programa.java
java Programa
```

Ver a versão instalada:

```bash
java -version
javac -version
```

---

## Estrutura

```
aprender-java-do-zero/
├── 01-fundamentos/
│   ├── Ola.java
│   ├── Tipos.java
│   ├── Iva.java
│   └── Saudacao.java
├── 02-ciclos/
│   ├── Contagem.java
│   ├── ContagemR.java
│   ├── Tabuada.java
│   ├── Pares.java
│   └── Pares2.java
├── 03-metodos-poo/
│   ├── Metodos.java
│   ├── Pessoa.java
│   └── Programa.java
├── 04-reforco/
│   ├── aquecimento1.java
│   ├── exContagem.java
│   ├── somaPares.java
│   └── somaIntervalo.java
├── java-bancada.html
├── ROADMAP.md
└── README.md
```

---

## O que há em cada pasta

### `01-fundamentos`
<!-- ESCREVE TU: uma linha por ficheiro. O que faz e que conceito treina.
     Exemplo do formato: `Iva.java` — calcula o IVA a partir de um preço;
     treina tipos primitivos e casts. -->

### `02-ciclos`
<!-- ESCREVE TU: idem. Diz porque existem `Pares` e `Pares2` — a diferença
     entre os dois é o interessante. -->

### `03-metodos-poo`
<!-- ESCREVE TU: idem. `Pessoa` e `Programa` funcionam em conjunto — explica
     a divisão: uma classe guarda dados, a outra corre. -->

### `04-reforco`
<!-- ESCREVE TU: idem. Diz que esta pasta é reescrita de coisas já feitas,
     sem consultar o ficheiro antigo. -->

---

## Bancada — `java-bancada.html`

Ficheiro único, abre no browser, sem instalar nada.

```bash
xdg-open java-bancada.html
```

<!-- ESCREVE TU: explica o que a bancada tem. Menciona o simulador linha a
     linha e o painel de variáveis — é a parte que te desbloqueou o
     `somaIntervalo`. Três ou quatro linhas chegam. -->

---

## Método

<!-- ESCREVE TU: esta secção é a que distingue este repo de um repo de
     tutorial copiado. Escreve as tuas regras por palavras tuas. Sugestão do
     que cobrir, sem ser por tópicos — escreve em prosa:

     - um passo só fecha quando o exercício de reforço sai sem consultar nada
     - validar é recalcular por outro caminho, não olhar e concordar
     - os bloqueios desfazem-se a executar, não a ler
-->

---

## Registo de erros

Erros reais, o que os causou e como se resolveram.

| Data | Ficheiro | Erro | Causa | Como se resolveu |
|---|---|---|---|---|
| 13–14 set | `somaIntervalo.java` | <!-- ESCREVE TU --> | <!-- ESCREVE TU --> | <!-- ESCREVE TU --> |
| <!-- data --> | `somaPares.java` | Soma dos pares de 200 a 300 dada como 12550 | <!-- ESCREVE TU --> | <!-- ESCREVE TU --> |

<!-- ESCREVE TU: acrescenta uma linha a cada erro novo. Cinco minutos a
     seguir ao exercício, nunca em bloco. -->

**Valores de controlo do `somaIntervalo`:**

| Intervalo | Resultado |
|---|---|
| 2 → 6 | 12 |
| 3 → 6 | 10 |
| 4 → 6 | 10 |
| 5 → 6 | 6 |
| 200 → 300 | 12750 |

---

## Estado

**Fase 1** — <!-- ESCREVE TU: percentagem -->
**Fase 2** — <!-- ESCREVE TU: percentagem -->

Plano completo em [`ROADMAP.md`](ROADMAP.md).

### Sólido
<!-- ESCREVE TU: lista curta. Só o que consegues escrever sem consultar. -->

### Compreendido, ainda não automático
<!-- ESCREVE TU -->

### Por tocar
<!-- ESCREVE TU -->

---

## A seguir

1. Arrays — `int[]`, `.length`, `for` com índice, `for-each`
2. `switch`
3. `do-while`
4. `List<Pessoa>`

<!-- ESCREVE TU: uma linha por cima desta lista a dizer qual é o exercício
     de reforço de cada passo. -->
