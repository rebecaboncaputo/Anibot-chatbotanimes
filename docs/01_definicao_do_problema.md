# Etapa 1: Definição do Problema

**Projeto:** Recomendador de Animes (chatbot com RAG)
**Autora:** Rebeca Bontempo
**Versão:** 1.0 | **Data:** 26/10/2026 | **Status:** rascunho

> Como usar este documento: os trechos marcados com `[PREENCHER]` são para você completar. Os trechos marcados com *(sugestão)* são rascunhos para você revisar e ajustar. Apague as instruções em citação (`>`) quando terminar cada seção.

---

## Sumário

1. [Contexto e motivação](#1-contexto-e-motivação)
2. [Objetivos e escopo](#2-objetivos-e-escopo)
3. [Público-alvo e contexto de uso](#3-público-alvo-e-contexto-de-uso)
4. [Entradas e saídas](#4-entradas-e-saídas)
5. [Abordagem técnica](#5-abordagem-técnica)
6. [Levantamento de requisitos](#6-levantamento-de-requisitos)
7. [Dados necessários](#7-dados-necessários)
8. [Critérios de sucesso](#8-critérios-de-sucesso)
9. [Premissas, restrições e riscos](#9-premissas-restrições-e-riscos)
10. [Perguntas para a EDA](#10-perguntas-para-a-eda)
11. [Checklist de revisão](#11-checklist-de-revisão)
12. [Histórico de versões](#12-histórico-de-versões)

---

## 1. Contexto e motivação

Quem termina uma série de anime muitas vezes não sabe o que assistir em seguida. O catálogo é enorme, e listas genéricas de "mais populares" não consideram o gosto individual nem permitem pedir algo em palavras próprias. Este projeto propõe um assistente conversacional que recebe um pedido em português, como "quero algo sombrio com protagonista inteligente", e recomenda animes adequados, explicando o motivo de cada indicação.

## 2. Objetivos e escopo

### 2.1 Objetivo geral

Recomendar animes a partir de pedidos em linguagem natural, justificando cada indicação com base nas informações do anime.

### 2.2 Objetivos específicos

1. Processar e higienizar uma base de dados estática de animes contendo sinopses e metadados estruturados.
2. Implementar uma busca por similaridade de significado entre o pedido do usuário e as sinopses.
3. Permitir filtros por gênero, formato e nota.
4. Gerar respostas conversacionais com justificativa.
4. Avaliar a qualidade das recomendações com um conjunto de consultas de teste

### 2.3 Dentro do escopo (versão 1)

1. Ingestão e limpeza de dataset estático em formato .csv (MyAnimeList 2023 via Kaggle).
2. Vetorização de sinopses e mecanismo de busca por similaridade semântica (vetorial).
3. Geração de resposta e justificativa via LLM utilizando contexto recuperado (arquitetura RAG).
4. Retorno padronizado de exatamente 5 recomendações por consulta válida.
5. Aplicação rigorosa das regras de negócio RN01 (excluir notas nulas/não lançados), RN03 (não recomendar o próprio anime citado) e RN04 (filtro NSFW por padrão).

### 2.4 Escopo futuro (Versão 2)

1. Ingestão incremental e automatizada via API REST viva (ex.: API Jikan) para atualização de novos lançamentos.
2. Refinamento iterativo de busca no fluxo da conversa (ex.: "gostei, mas quero um mais curto") — Requisito RF07 realocado para a V2 para proteger o prazo da V1.
3. Agrupamento avançado de franquias por grafo de relacionamentos/IDs da API (RN02 avançada).
4. Memória de contexto de longo prazo e perfil de preferências do usuário.

### 2.5 Fora do escopo (versão 1)

1. Sistema de autenticação, contas de usuário ou login.
2. Recomendação de mídias que não sejam animes (ex.: mangás, manhwasa, doramas, live-actions).
3. Treinamento ou fine-tuning de modelos de linguagem do zero.
4. Interface mobile nativa (iOS/Android).

## 3. Público-alvo e contexto de uso

| Item | Descrição |
|---|---|
| **Usuário principal** | Fãs de animes e entusiastas da cultura pop asiática que buscam novas recomendações |
| **Nível de conhecimento em anime** | Intermediário a experiente (já assistiu aos títulos mais populares e busca obras específicas)|
| **Canal de uso** | `[PREENCHER: site, aplicativo, Discord, terminal...]` |
| **Natureza do projeto** | acadêmico, pessoal|

**Persona:**
 ```text
 Lucas, 22 anos, assiste animes há bastante tempo. Já consumiu os títulos mainstream e agora procura obras com dinâmicas muito específicas (ex.: "um anime psicológico com batalhas mentais e sem romance"). Sente dificuldade de achar essas opções nos filtros tradicionais das plataformas de streaming e prefere descrever o que quer em português como se estivesse conversando com um amigo especialista.
```
## 4. Entradas e saídas

> O que o sistema recebe e o que devolve. Aqui nascem os conceitos de *feature* (informação de entrada) e *target* (saída esperada).

| | Descrição |
|---|---|
| **Entrada** | Texto livre em português descrevendo o tipo de história desejada, com filtros opcionais (gênero, formato, nota mínima) |
| **Saída** | 5 animes recomendados, cada um com uma justificativa curta baseada nos dados |

**Exemplo de uso:**

```text
Entrada: 
  Consulta: "Quero um anime sombrio de viagem no tempo com suspense e mistério"
  Filtro Opcional: Formato = TV | Nota Mínima = 8.0

Saída:
  "Com base no seu pedido por mistério e viagem no tempo, separei 5 recomendações:
   1. Steins;Gate - Acompanha um cientista que descobre como enviar mensagens ao passado, gerando consequências sombrias em uma trama repleta de suspense.
   2. Erased (Boku dake ga Inai Machi) - O protagonista volta no tempo para impedir uma série de crimes em sua infância, unindo mistério e tensão psicológica.
   3. ..."
```
---

## 5. Abordagem técnica

> Registre a escolha **e a justificativa**. Justificar é o que dá valor ao relatório.

**Tipo de tarefa:** recomendação baseada em conteúdo, com busca semântica e geração de resposta por RAG (Retrieval-Augmented Generation).

**Como funciona (visão geral):**

```text
Pedido do usuário → vira vetor (embedding) → busca no banco vetorial
                                                    ↓
              Pedido + animes encontrados → LLM → Resposta justificada
```

**Papel de cada componente (versão 1):**

| Componente | Função |
|---|---|
| Modelo de embedding | Converter texto (pedido e sinopses) em vetores que representam significado |
| Banco vetorial | Encontrar os vetores mais próximos do pedido |
| Filtros por metadados | Restringir resultados por gênero, formato e nota |
| LLM | Escrever a resposta e justificar cada indicação, usando só o que foi recuperado |

**Justificativa da escolha:** A busca vetorial permite capturar a intenção e o significado da consulta, algo impossível via busca por palavras-chave tradicionais. O padrão RAG resolve o problema de alucinação das LLMs, pois o modelo de geração é instruído a usar exclusivamente as sinopses recuperadas do banco de dados para construir a resposta.

**Alternativas descartadas:**

| Alternativa | Motivo do descarte |
|---|---|
| Filtragem colaborativa | Exige avaliações de muitos usuários, que não temos |
| Apenas filtros por gênero | Não atende pedidos em linguagem natural |
| Apenas LLM, sem recuperação | Maior risco de inventar informações |

---

## 6. Levantamento de requisitos

> **Legenda de prioridade:** Alta = o sistema não funciona sem isso. Média = melhora bastante a qualidade. Baixa = desejável.
> Os valores numéricos são pontos de partida e devem ser validados na EDA ou nos testes.

### 6.1 Requisitos funcionais (RF)

| Código | Descrição | Prioridade | Critério de aceitação | Como verificar |
|---|---|---|---|---|
| RF01 | O sistema deve aceitar consultas em linguagem natural, em português, descrevendo o tipo de história que o usuário quer assistir. | Alta | Aceita frases de 3 a 50 palavras e devolve resposta para pelo menos 95% das consultas válidas. | Bateria de 20 consultas de teste |
| RF02 | O sistema deve recuperar os animes semanticamente mais próximos da consulta. | Alta | Em 10 consultas de teste, ao menos 7 retornam 3 ou mais animes considerados coerentes. | Avaliação manual por você e 3 colegas |
| RF03 | O sistema deve permitir filtros estruturados por metadados (gênero, formato, nota mínima). | Média | Com filtro ativo, 100% dos resultados respeitam o filtro. | Teste automático |
| RF04 | O sistema deve usar uma LLM com RAG para gerar uma resposta conversacional que justifique cada indicação. | Alta | Cada recomendação traz uma justificativa baseada nos dados do anime recuperado. | Revisão manual de 10 respostas |
| RF05 | O sistema deve retornar exatamente 5 recomendações por pedido (ou informar quando houver menos). | Alta | Resposta com 5 itens, ou aviso explícito. | Teste automático |
| RF06 | O sistema deve tratar consultas sem resultado relevante, vazias ou fora do tema, respondendo de forma clara em vez de inventar. | Média | Em consultas fora do escopo, nenhum anime é recomendado e há uma explicação. | Teste com 5 consultas fora do tema |
| RF07 | O sistema deve permitir refinar a busca na conversa (ex.: "mais curto", "sem romance"). | Baixa | A nova resposta reflete o ajuste pedido. | Teste manual |

### 6.2 Requisitos não funcionais (RNF)

| Código | Descrição | Prioridade | Critério de aceitação | Como verificar |
|---|---|---|---|---|
| RNF01 | O modelo de embedding deve interpretar consultas em português e relacioná-las a sinopses em inglês (suporte multilíngue). | Alta | Consultas em português recuperam animes coerentes, no mesmo nível das consultas em inglês. | Comparar 10 consultas em PT e em EN |
| RNF02 | O pipeline de dados deve remover sinopses nulas, duplicadas e muito curtas. **O limite de 20 palavras é uma hipótese**, a confirmar na EDA. | Alta | Base final sem sinopses nulas ou duplicadas; limite justificado por dados. | EDA: nulos, duplicatas e histograma de tamanho |
| RNF03 | A busca vetorial deve responder com baixa latência (meta inicial: menos de 500 ms). | Média | 95% das buscas abaixo de 500 ms, sem contar a geração da LLM. | Medir tempo em 100 consultas |
| RNF04 | As justificativas da LLM devem se basear apenas nas informações recuperadas, sem inventar fatos. | Alta | Nenhum fato da justificativa contradiz ou extrapola os dados do anime. | Revisão manual de 10 respostas |
| RNF05 | O tempo total de resposta (busca + geração) deve ser aceitável para uma conversa. | Média | Meta inicial: menos de 10 s na maioria das respostas. | Medir tempo ponta a ponta |
| RNF06 | O projeto deve usar apenas dados com licença que permita uso acadêmico e registrar fonte, data e licença. | Alta | Registro de coleta preenchido; licença verificada. | Revisão do documento de coleta |
| RNF07 | O pipeline deve ser reproduzível: dados brutos preservados e tratamentos registrados em código. | Média | Rodar o pipeline do zero gera a mesma base final. | Executar em ambiente limpo |

### 6.3 Regras de negócio (RN)

| Código | Descrição | Prioridade | Critério de aceitação | Como verificar |
|---|---|---|---|---|
| RN01 | Animes sem nota definida ou com status "não lançado" não devem aparecer nas recomendações principais. | Média | 0% dos Top-5 com nota nula ou status "não lançado". | Teste automático |
| RN02 | Os resultados devem ser diversificados para evitar múltiplas temporadas da mesma franquia no mesmo Top-5. | Média | Máximo de 1 item por franquia em cada Top-5. | Teste automático (exige identificar a franquia) |
| RN03 | O anime citado na consulta não deve ser recomendado a si mesmo. | Alta | O título citado nunca aparece no Top-5. | Teste automático |
| RN04 | Conteúdo adulto só deve aparecer se o usuário pedir explicitamente. | Média | Sem pedido explícito, nenhum item adulto no Top-5. | Teste automático, se o dataset tiver classificação indicativa |

## 7. Dados necessários

### 7.1 Colunas necessárias

| Dado | Para que serve | Requisitos ligados | Prioridade |
|---|---|---|---|
| Título (e ID único) | Identificar o anime | RF05, RN03 | Obrigatório |
| Sinopse | Busca por significado | RF02, RNF01, RNF02 | Obrigatório |
| Gêneros | Filtros e justificativa | RF03 | Obrigatório |
| Formato (série, filme...) | Filtro | RF03 | Desejável |
| Nota média | Filtro e regra de exibição | RF03, RN01 | Desejável |
| Status de exibição | Ocultar não lançados | RN01 | Desejável |
| Identificador de franquia | Diversificar resultados | RN02 | Desejável |
| Classificação indicativa | Controle de conteúdo adulto | RN04 | Desejável |

### 7.2 Requisitos de qualidade e quantidade

> Os números abaixo são exemplos. Ajuste conforme a realidade do que encontrar.

| Critério | Meta |
|---|---|
| Quantidade mínima de animes | ≥5.000 animes válidos após limpeza |
| Sinopses preenchidas | 100% de preenchimento na base final (após remoção de nulos) |
| Atualidade | Lançamentos até pelo menos 2023|
| Cobertura | Vários gêneros e formatos, não só animes famosos |
| Licença | Permite uso acadêmico |

### 7.3 Viabilidade
A viabilidade foi confirmada pelo uso do dataset público MyAnimeList Dataset (2023) do Kaggle, que supre todas as colunas obrigatórias e desejáveis identificadas na Seção 7.1.

## 8. Critérios de sucesso

| Critério | Meta | Método |
|---|---|---|
| Qualidade das recomendações | Pelo menos 7 de 10 consultas de teste com 3 ou mais recomendações coerentes | Avaliação manual por você e 3 colegas |
| Fidelidade das justificativas | Nenhuma informação inventada nas 10 respostas revisadas | Conferir com a base de dados |
| Desempenho | Busca abaixo de 500 ms e resposta completa abaixo de 10 s | Medição de tempo |
| Regras de negócio | 0 violações em testes automáticos | Testes de RN01, RN03 e RF05 |

`[PREENCHER: ajuste as metas ao que você considera aceitável]`

---

## 9. Premissas, restrições e riscos

### 9.1 Premissas

> O que você assume ser verdade. A EDA serve para testar cada uma.

| Código | Premissa | Como será testada |
|---|---|---|
| P1 | A sinopse e os gêneros bastam para medir semelhança entre animes | EDA + avaliação das recomendações |
| P2 | O dataset escolhido é representativo e atual | EDA: cobertura por gênero e por ano |
| P3 | Há animes utilizáveis em quantidade suficiente após a limpeza | EDA: contagem após aplicar o RNF02 |
| P4 | O modelo de embedding escolhido lida bem com português e inglês | Teste do RNF01 |

### 9.2 Restrições

| Tipo | Descrição |
|---|---|
| Prazo | `[PREENCHER]` |
| Recursos computacionais | `[PREENCHER: computador, GPU, créditos de API]` |
| Licença dos dados | Apenas dados com uso acadêmico permitido |
| Privacidade | Sem coleta de dados pessoais (LGPD) |

### 9.3 Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Muitas sinopses ausentes ou muito curtas | Menos animes recomendáveis | Escolher outro dataset ou complementar com API |
| Gêneros concentrados em poucas categorias | Recomendações enviesadas | Verificar na EDA e diversificar (RN02) |
| LLM inventa informações | Perda de confiança | Instruir a usar só o contexto e testar (RNF04) |
| Dataset desatualizado | Faltam animes recentes | Registrar a limitação ou usar API |
| Custo ou limite de uso de APIs | Projeto inviável | Usar modelos gratuitos ou locais quando possível |

`[PREENCHER: acrescente riscos que você perceber]`

---

## 10. Perguntas para a EDA

> Ligue cada requisito, premissa ou risco a uma pergunta que a EDA vai responder. Esta é a ponte entre a Etapa 1 e a Etapa 3.

| Origem | Pergunta para a EDA | Como verificar no pandas |
|---|---|---|
| RNF02 | Quantas sinopses são nulas, duplicadas ou têm menos de 20 palavras? | `df["sinopse"].isnull().sum()`, `df["sinopse"].duplicated().sum()`, `df["sinopse"].str.split().str.len().describe()` |
| RNF01 | Em que idioma estão as sinopses? | Amostragem manual e/ou biblioteca de detecção de idioma |
| RN01 | Quantos animes têm nota nula ou status "não lançado"? | `df["nota"].isnull().sum()`, `df["status"].value_counts()` |
| RN02 | É possível identificar temporadas da mesma franquia? | Inspecionar títulos e colunas de relação |
| RF03 | Gêneros e formatos estão bem preenchidos e padronizados? | `df["genero"].value_counts()`, `df["tipo"].value_counts()` |
| RN04 | Existe coluna de classificação indicativa? | `df.columns`, `df["classificacao"].value_counts()` |
| P2 | Qual o ano mais recente e como os animes se distribuem por ano? | `df["ano"].max()`, `df["ano"].value_counts().sort_index()` |
| P3 | Quantos animes sobram após aplicar a limpeza do RNF02? | Contagem após filtros (apenas simulação, sem alterar os dados) |

*(Ajuste os nomes das colunas aos do dataset escolhido.)*

---

## 11. Checklist de revisão

Antes de dar a etapa por concluída, confirme:

- [ ] Uma pessoa de fora entende o objetivo?
- [ ] Entradas e saídas estão claras, com um exemplo?
- [ ] A abordagem está justificada e as alternativas registradas?
- [ ] Cada requisito tem prioridade, critério de aceitação e forma de verificação?
- [ ] Os dados necessários foram derivados dos requisitos?
- [ ] A viabilidade dos dados foi verificada?
- [ ] Há uma forma concreta de medir o sucesso?
- [ ] O que está fora do escopo está explícito?
- [ ] Premissas e riscos estão listados?
- [ ] Cada premissa tem uma pergunta correspondente na EDA?
- [ ] Versão e data estão no topo do documento?

---

## 12. Histórico de versões

> Quando algo mudar (por exemplo, após a coleta ou a EDA), crie uma nova versão e registre o motivo. Isso mostra o caráter iterativo do projeto e rende bom material para o relatório.

| Versão | Data | O que mudou | Motivo |
|---|---|---|---|
| 1.0 | 26/10/2026 | Versão inicial | Início do projeto |