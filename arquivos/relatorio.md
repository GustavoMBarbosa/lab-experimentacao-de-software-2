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

| Métrica | Média | Mediana | Desvio Padrão | Mínimo | Máximo |
|---------|-------|---------|---------------|--------|--------|
| ⭐ Stars | 9.613 | 5.780 | 11.703 | 3.413 | 151.699 |
| 🕰 Idade (anos) | 9.63 | 9.75 | 3.05 | 0.17 | 16.92 |
| 📦 Releases | 38.93 | 10.00 | 84.69 | 0 | 1000 |
| 📏 LOC | 51.12 | 44.13 | 33.43 | 2.00 | 406.33 |
| 💬 Comentários | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 5.2 Observações iniciais
- Grande dispersão em **estrelas** e **releases**, indicando que alguns projetos puxam a média para cima.
- Idade média de ~10 anos → projetos maduros.
- LOC com valores moderados, mas alguns repositórios muito maiores (outliers).
- Métricas de comentários não representaram valor significativo (possível falha na coleta).

### 5.3 Maiores valores por repositório
A seguir são apresentados os repositórios que obtiveram os **maiores valores em cada métrica**:

| Métrica | Repositório | Owner | Stars | Idade (anos) | Releases | LOC | CBO | DIT | LCOM |
|---------|-------------|-------|-------|--------------|----------|-----|-----|-----|------|
| ⭐ Stars | JavaGuide | Snailclimb | 151.699 | 7.33 | 0 | CK_ERROR | CK_ERROR | CK_ERROR | CK_ERROR |
| 🕰 Idade | platform_frameworks_base | aosp-mirror | 11.200 | 16.92 | 47 | 152.77 | 4.92 | 1.92 | 29.8 |
| 📦 Releases | Activiti | Activiti | 9.877 | 12.25 | 1000 | 155.43 | 6.34 | 1.85 | 44.3 |
| 📏 LOC | GhidraMCP | LaurieWired | 8.122 | 8.5 | 5 | 406.33 | 16.33 | 2.3 | 210.5 |
| 🔗 CBO | GhidraMCP | LaurieWired | 8.122 | 8.5 | 5 | 406.33 | 16.33 | 2.3 | 210.5 |
| 🌳 DIT | pkl | apple | 7.223 | 4.1 | 12 | 33.2 | 3.7 | 4.39 | 17.6 |
| ⚖ LCOM | libgdx | libgdx | 21.199 | 14.75 | 88 | 199.44 | 5.4 | 1.7 | 3447.19 |

### 5.4 Discussão dos resultados
Nesta seção, os resultados foram analisados em relação às questões de pesquisa definidas no início do relatório:

- **RQ01 (Popularidade × Qualidade):** Os repositórios mais populares (com maior número de estrelas) apresentaram grande variação nos valores de CBO, DIT e LCOM. Isso indica que popularidade não está diretamente associada a melhor qualidade interna.
- **RQ02 (Maturidade × Qualidade):** Repositórios mais antigos tendem a acumular complexidade (CBO e LCOM mais altos). Entretanto, alguns preservam boas práticas.
- **RQ03 (Atividade × Qualidade):** Projetos com maior número de releases demonstraram melhor manutenção e organização, refletida em valores mais controlados de acoplamento. Contudo, só a frequência de releases não garante qualidade consistente.
- **RQ04 (Tamanho × Qualidade):** Os repositórios com maior LOC apresentaram métricas de qualidade piores, principalmente no LCOM. Isso confirma a hipótese de que sistemas maiores tendem a ser mais complexos e difíceis de manter.

### 5.5 Análise ilustrativa de repositórios
- **JavaGuide (Snailclimb):** Maior número de estrelas, mas com falhas na coleta CK, dificultando análise de qualidade.
- **platform_frameworks_base (aosp-mirror):** Repositório mais antigo (16.9 anos), ainda ativo e grande, apresentou valores médios de qualidade.
- **Activiti:** Projeto extremamente ativo em termos de releases (1000), indicando alta manutenção.
- **GhidraMCP (LaurieWired):** Apresentou o maior LOC e também maior CBO, mostrando impacto do tamanho na complexidade.
- **libgdx:** Exibiu LCOM extremamente alto (3447.19), confirmando tendência de baixa coesão em projetos grandes.


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
