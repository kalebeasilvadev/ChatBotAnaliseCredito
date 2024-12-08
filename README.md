# Chatbot de Análise de Créditos

Um chatbot simples desenvolvido em Python para análise e consultas de crédito.

## Requisitos

- Python 3.x
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/kalebeasilvadev/ChatBotAnaliseCredito
cd ChatBotAnaliseCredito
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:
```txt
OPENAI_API_KEY="chave do OpenAI"
OPENAI_API_BASE="link da API do OpenAI" # se estiver usando o chatgpt nao precisa
```

1. Execute o arquivo principal:
```bash
python main.py
```

2. Use o chatbot:
   - Digite sua pergunta na caixa de texto
   - Pressione Enter ou clique em "Enviar"
   - Aguarde a resposta do chatbot

## Estrutura do Projeto

```
.
├── main.py           # Interface gráfica do chatbot
├── agente.py         # Lógica do chatbot
└── dataset/
    ├── context_base.txt          # Base de conhecimento
    └── german_credit_data.csv    # Dados para análise
```

## Suporte

Em caso de dúvidas, abra uma issue no repositório.

