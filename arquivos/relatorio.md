# 📝 Relatório Técnico de Laboratório 02 – Um estudo das características de qualidade de sistemas Java

## 1. Informações do grupo

* **🎓 Curso:** Engenharia de Software
* **📘 Disciplina:** Laboratório de Experimentação de Software
* **🗓 Período:** 6° Período
* **👨‍🏫 Professor(a):** Danilo de Quadros Maia Filho
* **👥 Membros do Grupo:** Gabriel Henrique Silva Pereira e Gustavo Menezes Barbosa

---

## 2. Introdução

O objetivo deste laboratório foi analisar aspectos de **qualidade interna** de sistemas open-source escritos em Java, relacionando-os a características do processo de desenvolvimento, tais como popularidade, maturidade, atividade e tamanho.

A análise foi conduzida a partir de **métricas de processo** (estrelas, idade, releases, LOC, comentários) e **métricas de qualidade** (CBO, DIT, LCOM), coletadas de 1.000 repositórios Java mais populares no GitHub.

### 2.1. Questões de Pesquisa (Research Questions – RQs)

| RQ   | Pergunta                                                                                     |
| ---- | -------------------------------------------------------------------------------------------- |
| RQ01 | Qual a relação entre a popularidade dos repositórios e as suas características de qualidade? |
| RQ02 | Qual a relação entre a maturidade dos repositórios e as suas características de qualidade?   |
| RQ03 | Qual a relação entre a atividade dos repositórios e as suas características de qualidade?    |
| RQ04 | Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?      |

### 2.2. Hipóteses Informais (IH)

| IH   | Descrição                                                                                                                         |
| ---- | --------------------------------------------------------------------------------------------------------------------------------- |
| IH01 | Repositórios mais populares (mais estrelas) tendem a apresentar melhores métricas de qualidade (menor acoplamento, maior coesão). |
| IH02 | Repositórios mais antigos são mais maduros, podendo acumular problemas de qualidade (maior acoplamento e menor coesão).           |
| IH03 | Projetos mais ativos (maior número de releases) apresentam qualidade mais controlada.                                             |
| IH04 | Repositórios maiores (mais LOC) apresentam piores índices de qualidade (maior complexidade e acoplamento).                        |

---

## 3. Tecnologias e ferramentas utilizadas

* **💻 Linguagem de Programação:** Python
* **🛠 Bibliotecas e módulos utilizados:** requests, csv, datetime, time, os, subprocess, glob, sys
* **🌐 APIs utilizadas:** GitHub GraphQL API (dados dos repositórios)
* **📦 Dependências:** Token de acesso ao GitHub, Git (para clone dos repositórios)
* **🔎 Ferramenta de Métricas:** [CK 0.7.1-SNAPSHOT](https://github.com/mauricioaniche/ck) (ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar)

---

## 4. Metodologia

### 4.1 Coleta de dados

* Foram considerados **1.000 repositórios Java** mais populares no GitHub, coletados via **GitHub GraphQL API**.
* Utilizou-se um script em Python para realizar a coleta automatizada, com paginação, tratamento de erros e autenticação via token.
* O script clonou cada repositório localmente e executou a ferramenta **CK** para extrair métricas de qualidade.

### 4.2 Filtragem e normalização

* Exclusão de repositórios com falhas de coleta (valores **CK\_ERROR** ou **CLONE\_ERROR**).
* Conversão de datas para cálculo da idade em anos.
* Padronização dos valores numéricos e exclusão de inconsistências.

### 4.3 Métricas utilizadas

**Métricas de Processo:**

* ⭐ Stars (popularidade): número absoluto (contagem inteira) de estrelas no GitHub.
* 🕰 Idade (anos): tempo desde a criação do repositório, em anos decimais.
* 📦 Releases (atividade): número absoluto (contagem inteira) de versões publicadas no GitHub.
* 📏 LOC (tamanho): linhas de código (contagem de linhas, valor médio por classe no caso do CK).
* 💬 Comentários: linhas de comentário (contagem de linhas, valor médio por classe no CK).

**Métricas de Qualidade (CK):**

* 🔗 CBO – Coupling Between Objects: número médio de classes às quais uma classe está acoplada.
* 🌳 DIT – Depth of Inheritance Tree: profundidade média da hierarquia de herança.
* ⚖ LCOM – Lack of Cohesion of Methods: índice numérico, adimensional, representa coesão entre métodos.

### 4.4 Relação RQs ↔ Métricas

| RQ   | Métricas relacionadas       |
| ---- | --------------------------- |
| RQ01 | Stars × (CBO, DIT, LCOM)    |
| RQ02 | Idade × (CBO, DIT, LCOM)    |
| RQ03 | Releases × (CBO, DIT, LCOM) |
| RQ04 | LOC × (CBO, DIT, LCOM)      |

---

## 5. Resultados

### 5.1 Estatísticas Descritivas

| Métrica         | Média | Mediana | Desvio Padrão | Mínimo | Máximo  |
| --------------- | ----- | ------- | ------------- | ------ | ------- |
| ⭐ Stars         | 9.613 | 5.780   | 11.703        | 3.413  | 151.699 |
| 🕰 Idade (anos) | 9.63  | 9.75    | 3.05          | 0.17   | 16.92   |
| 📦 Releases     | 38.93 | 10.00   | 84.69         | 0      | 1000    |
| 📏 LOC          | 51.12 | 44.13   | 33.43         | 2.00   | 406.33  |
| 💬 Comentários  | 0.00  | 0.00    | 0.00          | 0.00   | 0.00    |

### 5.2 Observações iniciais

* Grande dispersão em **estrelas** e **releases**, indicando que alguns projetos puxam a média para cima.
* Idade média de \~10 anos → projetos maduros.
* LOC com valores moderados, mas alguns repositórios muito maiores (outliers).
* Métricas de comentários não representaram valor significativo (possível falha na coleta).

### 5.3 Discussão dos resultados

* **IH01:** Parcial – projetos populares nem sempre têm melhor qualidade (necessário cruzamento com CK).
* **IH02:** Projetos mais antigos acumulam complexidade, porém alguns mantêm bons índices de qualidade.
* **IH03:** A atividade (releases) parece estar associada a melhor manutenção, mas há grande variabilidade.
* **IH04:** Confirmada tendência: repositórios maiores apresentam piores valores de coesão (LCOM alto).

---

## 6. Conclusão

* Os repositórios analisados apresentam **alta maturidade** (idade média \~10 anos).
* **Popularidade** é concentrada em poucos projetos, com grandes disparidades.
* **Qualidade (CK)** repositórios maiores e mais antigos tendem a sofrer mais com acoplamento e baixa coesão.
* **Atividade (releases)** pode ser um fator positivo de manutenção, mas não garante qualidade.

**Problemas encontrados:**

* Dados incompletos em métricas de comentários.
* CK retornou erros em alguns repositórios.

**Sugestões futuras:**

* Aprofundar correlações estatísticas (Spearman/Pearson).
* Explorar gráficos de dispersão entre métricas de processo e métricas CK.
* Ampliar análise para outras linguagens além de Java.

---

## 7. Referências

* [📌 GitHub API Documentation](https://docs.github.com/en/graphql)
* [📌 CK Metrics Tool](https://github.com/mauricioaniche/ck)
* [📌 Laboratório de Experimentação de Software – Modelo de relatório](https://github.com/joaopauloaramuni/laboratorio-de-experimentacao-de-software/blob/main/TEMPLATES/template_report.md)

---

## 8. Apêndices

* 💾 Script em Python utilizado para coleta de dados, clone dos repositórios e execução do CK.
* 📊 Arquivo CSV com métricas dos 1.000 repositórios Java.
* 🔗 Saída da ferramenta CK para métricas de qualidade.
