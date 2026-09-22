# AniBot - Chatbot de Recomendação de Animes

<!-- O primeiro parágrafo deve sempre resumir o que é o projeto em uma ou duas frases. -->
Um projeto de laboratório e treinamento focado em integrar Python e MySQL para criar um chatbot interativo via terminal que recomenda animes com base nas preferências do usuário.

## Levantamento de Requisitos

<!-- Aqui entramos no que você pediu! É onde declaramos o planejamento do que o bot tem que fazer. -->

### Requisitos Funcionais (O que o sistema faz)
- O sistema deve perguntar ao usuário qual o seu gênero de anime favorito (Ação, Romance, Comédia, etc).
- O sistema deve buscar no banco de dados os animes correspondentes à escolha.
- O bot deve exibir no terminal uma lista com Título, Sinopse e Nota do anime recomendado.
- O bot deve informar caso não encontre nenhum anime para o gênero digitado (Tratamento de erro).

### Requisitos Não Funcionais (Como o sistema opera)
- A lógica principal deve ser escrita em **Python 3**.
- Os dados dos animes devem ser armazenados de forma relacional usando **MySQL**.
- A interação ocorrerá exclusivamente via **Terminal/Linha de Comando**.

---

## Tecnologias Utilizadas

<!-- É importante listar as ferramentas para que outros saibam o que você usou para construir. -->
* **Linguagem:** Python
* **Banco de Dados:** MySQL
* **Bibliotecas:** `mysql-connector-python` (para conectar o código ao banco)
* **Controle de Versão:** Git e GitHub

---

## Estrutura do Banco de Dados

<!-- Mostrar como os dados estão organizados ajuda muito a entender o projeto. -->
A tabela `animes` no MySQL foi estruturada da seguinte forma:

| Coluna | Tipo de Dado | Descrição |
|--------|--------------|-----------|
| `id` | INT | Identificador único do anime (Chave Primária) |
| `titulo` | VARCHAR | O nome do anime |
| `genero` | VARCHAR | O gênero principal (ex: Shounen, Isekai) |
| `nota` | DECIMAL | Nota no MyAnimeList (ex: 8.5) |

---

## Como rodar o projeto na sua máquina

<!-- Essa é a parte mais importante de um README. Um tutorial de como testar o seu código! -->

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SeuUsuario/chatbot-animes.git
   ```

2. **Acesse a pasta do projeto:**
   ```bash
   cd chatbot-animes
   ```

3. **Configure o Banco de Dados:**
   - Abra o seu MySQL e rode o arquivo `banco_de_dados.sql` para criar a tabela.
   - Atualize o arquivo `bot.py` com o seu usuário e senha do MySQL.

4. **Instale as dependências:**
   ```bash
   pip install mysql-connector-python
   ```

5. **Inicie o Chatbot:**
   ```bash
   python bot.py
   ```

---
*Projeto desenvolvido para fins de estudo e prática de conceitos básicos de programação.*