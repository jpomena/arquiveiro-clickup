from src.utils.regex_patterns import RegexPatterns

# Lista dos padrões que queremos inspecionar
patterns_to_inspect = {
    'Backlog': RegexPatterns.backlog,
    'Start': RegexPatterns.start,
    'Done': RegexPatterns.done,
    'Delivery': RegexPatterns.delivery,
}

print("--- Iniciando Inspeção dos Padrões de Regex ---\n")

try:
    with open('output.txt', 'r', encoding='utf-8') as f:
        html_content = f.read()
    print("Arquivo 'output.html' lido com sucesso.\n")
except FileNotFoundError:
    print("ERRO: O arquivo 'output.html' não foi encontrado.")
    exit()

# Itera sobre cada padrão e aplica no conteúdo do HTML
for name, pattern in patterns_to_inspect.items():
    print(f"--- Testando Padrão: '{name}' ---")

    # Usamos finditer para encontrar
    #  todas as ocorrências, não apenas a primeira
    matches = list(pattern.finditer(html_content))

    if not matches:
        print("Nenhuma correspondência encontrada para este padrão.")
    else:
        for i, match in enumerate(matches, 1):
            print(f"  [Match #{i}]")
            # match.group(0) é o texto completo que a regex capturou
            print(f"    Texto Completo (group 0): '{match.group(0).strip()}'")
            # match.groups() são apenas os grupos capturados pelos parênteses ()
            print(f"    Grupos Capturados        : {match.groups()}")

    print("-" * (len(name) + 22) + "\n")