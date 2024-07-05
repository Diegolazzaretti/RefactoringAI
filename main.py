import json
import os
import ollama
import requests
import google.generativeai as genai
import tracemalloc
import time
from openpyxl import Workbook

genai.configure(api_key="API-KEY")
OPENAI_API_KEY="API-KEY"

def preparar_conteudo_para_refatoracao(diretorio):
    arquivos_conteudo = []
    contador = 1

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('_before.py'):
            caminho_completo_py = os.path.join(diretorio, arquivo)
            with open(caminho_completo_py, 'r', encoding='utf-8') as arquivo_py:
                conteudo = arquivo_py.read()
            nome_sem_before = arquivo.replace('_before.py', '')
            arquivos_conteudo.append((contador, nome_sem_before, conteudo))
            contador += 1

    return arquivos_conteudo

# Start global performance tracking
start_time = time.time()

tracemalloc = tracemalloc
tracemalloc_global = tracemalloc
tracemalloc_global.start()

# Lista de instruções para cada requisição
instructions = [
    ("Refactor the following code to enhance its readability, modularity, and maintainability. "
     "The code to be refactored is presented next."),

    ("Refactor the following code to enhance its readability, modularity, and maintainability. "
     "Apply appropriate design patterns to reduce code duplication, simplify the logic, and improve overall organization. "
     "Ensure that the refactored code adheres to the best practices of software development, "
     "facilitating future modifications while maintaining functional integrity. "
     "After refactoring, explain the changes made to the code, describing how they contribute to the improvements. "
     "The code to be refactored is presented next.")
]

# Preparando o arquivo Excel
wb = Workbook()
ws = wb.active
ws.append(["Model", "Instruction", "Com/sem título", "Title", "API Time", "Memory used", "Peak memory"])

# Diretório dos arquivos
directory = 'H:\\0235020\\Documents\\Feevale\\TC\\python'
directory_responses = 'H:\\0235020\\Documents\\Feevale\\TC\\responses3'
contents = preparar_conteudo_para_refatoracao(directory)

model_gemini = genai.GenerativeModel('gemini-pro')

models = ["mistral:7b-instruct-q3_K_S", "gemini-pro", "gpt-4", "gpt-3.5-turbo-1106"]
headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "Application/json"}
link = "https://api.openai.com/v1/chat/completions"

for count, title, code in contents:
    base_filename = f"{directory_responses}\\{title}_all_refactorings.txt"
    with open(base_filename, 'w', encoding='utf-8') as main_file:
        main_file.write(f"Código Original ({title}):\n\n{code}\n\nRefatorações:\n\n")
        
        for idx, instruction in enumerate(instructions, start=1):
            for suffix in ["sem titulo", "com titulo"]:
                if suffix == "sem titulo":
                    complete_message = f"{instruction}\n\n{code}"
                else:
                    complete_message = f"{instruction}\n\n{count}. {title}\n{code}"

                for model_id in models:
                    model_name = model_id

                    # Restart memory tracking
                    tracemalloc.start()
                    api_start = time.time()

                    if model_id == "gemini-pro":
                        response = model_gemini.generate_content(complete_message)
                        response_text = response.text
                    elif model_id.startswith("mistral"):
                        model_name = "mistral"
                        response = ollama.chat(model=model_id, messages=[{'role': 'user', 'content': complete_message}])
                        response_text = response['message']['content']
                    else:
                        body_mensagem = json.dumps({
                            "model": model_id,
                            "messages": [{"role": "user", "content": complete_message}]
                        })
                        response = requests.post(link, headers=headers, data=body_mensagem)
                        response_text = json.loads(response.text)['choices'][0]['message']['content']

                    current_memory, peak_memory = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    api_end = time.time()
                    # Log API metrics
                    ws.append([model_name, f"instruction {idx}", suffix, title, api_end - api_start, current_memory, peak_memory])
                    print(f"Model: {model_name}, Instruction: {idx}, Title: {title}, API Time: {api_end - api_start} seconds, Memory used: {current_memory} bytes, Peak memory: {peak_memory} bytes")

                    model_filename = f"{directory_responses}\\{title}_{model_name}_instr{idx}_{suffix}.txt"
                    with open(model_filename, 'w', encoding='utf-8') as model_file:
                        model_file.write(f"{model_name} - Instrução {idx} {suffix}:\n\n{response_text}\n")
                    
                    # Also write to the main file
                    main_file.write(f"{model_name} - Instrução {idx} {suffix}:\n{response_text}\n\n")

wb.save("Refactored_Codes3.xlsx")
wb.close()

# Stop global timer
current_memory, peak_memory = tracemalloc_global.get_traced_memory()
tracemalloc_global.stop()
total_time = time.time() - start_time
print(f"Total execution time: {total_time} seconds, Memory used: {current_memory} bytes, Peak memory: {peak_memory} bytes")