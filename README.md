# Arquiveiro ClickUp

O Arquiveiro ClickUp é uma aplicação de desktop desenvolvida em Python com uma interface gráfica (GUI) que automatiza o processo de extração e armazenamento de dados de tarefas do ClickUp. A aplicação utiliza o Selenium para navegar no site do ClickUp, extrair dados dos cards de tarefas e, em seguida, armazena as informações em um banco de dados SQLite local.

## Funcionalidades

-   **Extração Automatizada de Dados**: Faz login automaticamente no ClickUp, navega para uma lista especificada e extrai dados dos cards de tarefas.
-   **Análise de Dados**: Utiliza BeautifulSoup e expressões regulares para analisar o HTML e extrair informações específicas como nome da tarefa, etiquetas, responsável e várias datas (criação, início, conclusão, entrega).
-   **Armazenamento Local**: Armazena os dados extraídos em um banco de dados SQLite local, criando um arquivo `viagens.db` no diretório de dados de aplicativos local do usuário.
-   **GUI Amigável**: Fornece uma interface gráfica simples construída com Tkinter e ttkbootstrap para que os usuários insiram suas credenciais, especifiquem a lista de destino e controlem o processo de extração.
-   **Execução Concorrente**: O processo de extração de dados é executado em uma thread separada para manter a GUI responsiva.

## Como Funciona

A aplicação segue estes passos para extrair os dados:

1.  **Entrada do Usuário**: O usuário fornece suas credenciais do ClickUp, o nome da lista de destino e, opcionalmente, o caminho para o Gecko driver do Firefox.
2.  **Automação do Navegador**: A aplicação abre uma janela do navegador Firefox usando Selenium, navega para a página de login do ClickUp e insere as credenciais do usuário.
3.  **Navegação para o Quadro Kanban**: Navega para a lista especificada e muda para a visualização do quadro Kanban.
4.  **Loop de Extração de Dados**: A aplicação itera através dos cards na coluna "Entregue" do quadro Kanban. Para cada card, ela:
    -   Abre o card para ver seus detalhes.
    -   Extrai o conteúdo HTML do nome da tarefa, etiquetas, responsável e histórico da tarefa.
    -   Utiliza BeautifulSoup para analisar o HTML.
    -   Aplica expressões regulares para extrair os pontos de dados necessários.
5.  **Armazenamento no Banco de Dados**: Os dados extraídos são salvos no banco de dados SQLite local.
6.  **Arquivar Card**: Após extrair os dados, a aplicação arquiva o card da tarefa no ClickUp.

## Estrutura do Projeto

O projeto está organizado nos seguintes diretórios e arquivos:

-   `main.py`: O ponto de entrada principal da aplicação. Ele inicializa os diferentes componentes (GUI, banco de dados, navegador, etc.) e inicia a aplicação.
-   `src/controller/sasori.py`: O controlador principal da aplicação. Ele lida com a lógica da aplicação, orquestra as interações entre os modelos e a visão, e gerencia o processo de extração de dados.
-   `src/models/`: Contém os componentes relacionados a dados da aplicação.
    -   `database.py`: Gerencia a conexão com o banco de dados SQLite, criação de tabelas e inserção de dados.
    -   `html_parser.py`: Usa BeautifulSoup para analisar o conteúdo HTML.
    -   `puppet_browser.py`: Controla a automação do navegador usando Selenium.
    -   `regex_engine.py`: Contém a lógica para extrair dados do HTML usando expressões regulares.
-   `src/utils/`: Contém módulos utilitários.
    -   `aux_functions.py`: Fornece funções auxiliares como logging.
    -   `clickup_selectors.py`: Armazena os seletores CSS usados para localizar elementos no site do ClickUp.
    -   `regex_patterns.py`: Define os padrões de expressão regular usados para a extração de dados.
-   `src/view/`: Contém os componentes da GUI da aplicação.
    -   `gui.py`: Define a interface gráfica do usuário usando Tkinter e ttkbootstrap.

## Requisitos

A aplicação requer as seguintes bibliotecas Python:

-   `selenium`
-   `beautifulsoup4`
-   `ttkbootstrap`
-   `pandas`

Elas podem ser instaladas usando o pip:

```bash
pip install -r requirements.txt
```

Além disso, requer que o Mozilla Firefox e o Gecko driver estejam instalados no sistema. O caminho para o Gecko driver pode ser fornecido na GUI.

## Como Usar

1.  Execute `main.py` para iniciar a aplicação.
2.  Preencha seu e-mail e senha do ClickUp.
3.  Digite o nome da lista do ClickUp que você deseja processar.
4.  (Opcional) Forneça o caminho para o seu executável do Gecko driver. Se não for fornecido, o Selenium tentará encontrá-lo no PATH do sistema.
5.  Clique em "Iniciar Extração" para começar o processo.
6.  A janela de log mostrará o progresso da extração.
7.  Clique em "Parar Extração" para interromper o processo a qualquer momento.

<a href="https://www.flaticon.com/free-icons/archives" title="archives icons">Archives icons created by Freepik - Flaticon</a>
