# Automatização de Refatoração de Código com IA

## Descrição
Este projeto investiga como a integração de design patterns, refatoração de código e inteligência artificial pode melhorar a qualidade do software. Foi realizado um estudo comparativo entre as refatorações manuais e aquelas assistidas por modelos de IA avançados, incluindo GPT-3.5, GPT-4, Gemini e Mistral. A pesquisa foca na avaliação da eficácia desses modelos na otimização de aspectos como clareza, modularidade e manutenibilidade do código.

Para isso, foi desenvolvida uma plataforma em Python que automatiza o processo de refatoração, enviando requisições para diferentes modelos de IA e armazenando os resultados. Os resultados indicam que a IA pode aprimorar significativamente a legibilidade, a estrutura e a documentação do código, facilitando sua manutenção e expansão futura.

## Instalação
1. Clone este repositório:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```
2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso
1. Configure suas chaves de API nos lugares indicados no código:
    ```python
    genai.configure(api_key="SUA_API_KEY_GENAI")
    OPENAI_API_KEY="SUA_API_KEY_OPENAI"
    ```

2. Prepare o conteúdo para refatoração colocando os arquivos de código original no diretório especificado:
    ```python
    directory = 'caminho/para/seus/arquivos'
    ```

3. Execute o script de automação de refatoração:
    ```bash
    python refactoring_automation.py
    ```

4. Os resultados das refatorações serão armazenados no diretório `responses3` e em um arquivo Excel `Refactored_Codes3.xlsx`.

## Contribuições
Contribuições são bem-vindas! Se você tiver sugestões, encontre algum problema ou quiser adicionar uma nova funcionalidade, por favor, abra uma issue ou envie um pull request.

## Contato
Para mais informações, entre em contato pelo e-mail: seu-email@exemplo.com
