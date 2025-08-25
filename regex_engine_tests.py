from src import RegexEngine

print("--- Iniciando Teste de Resultados do RegexEngine ---\n")

try:
    with open('output.txt', 'r', encoding='utf-8') as f:
        html_content = f.read()
    print("Arquivo 'output.html' lido com sucesso.\n")
except FileNotFoundError:
    print("ERRO: O arquivo 'output.html' não foi encontrado.")
    exit()

# Cria uma instância do seu motor de regex
engine = RegexEngine()

print("--- Resultados Finais ---")
print("Obs: As mensagens de 'log' abaixo vêm da sua própria classe.\n")

# Chama cada método e armazena o resultado
backlog_date = engine.get_task_backlog(html_content)
start_date = engine.get_task_start(html_content)
done_date = engine.get_task_done(html_content)
delivery_date = engine.get_task_delivery(html_content)

# Exibe os resultados finais de forma clara
print("\n--- Saída Formatada ---")
print(f"Data de Backlog  : {backlog_date}")
print(f"Data de Início   : {start_date}")
print(f"Data de Conclusão: {done_date}")
print(f"Data de Entrega  : {delivery_date}")
print("-----------------------")
