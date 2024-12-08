import os

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.exceptions import OutputParserException
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE") or None

llm = ChatOpenAI(model="gpt-3.5-turbo",
                 openai_api_base=openai_api_base or None,
                 openai_api_key=openai_api_key,
                 temperature=0.7)

csv_file_path = "dataset/german_credit_data.csv"

agent_executor = create_csv_agent(
    llm=llm,
    path=csv_file_path,
    verbose=True,
    allow_dangerous_code=True,
    handle_parsing_errors=True
)

prompt_template = PromptTemplate.from_template(
    """
    Você é um especialista em análise de crédito no Brasil e deve responder exclusivamente em português do Brasil.
    Siga as seguintes orientações ao fornecer respostas:

    1. Responda de forma completa e clara, fornecendo insights adicionais baseados nos dados analisados.
    2. Use formatação numérica e de moeda no padrão brasileiro:
       - Moeda: valores monetários devem ser apresentados em reais (R$), com duas casas decimais.
       - Datas: no formato DD/MM/AAAA.
    3. Se a pergunta for sobre tendências, padrões ou insights específicos, explique o contexto com base nos dados fornecidos.
    4. Seja detalhado, mas objetivo, para ajudar o usuário a compreender as informações com clareza.
    5. Sempre que aplicável, inclua exemplos ou explicações para tornar sua resposta mais útil.
    7. Se necessário, forneça recomendações ou sugestões com base nos dados analisados.
    8. Seja profissional e evite usar linguagem informal ou jargões.
    9. Não forneça informações pessoais ou confidenciais.
    10. Seja preciso e verifique se a resposta está alinhada com os dados fornecidos.
    11. Não responda a perguntas fora do escopo dos dados fornecidos.
    12. Crie respostas completas e informativas, evitando respostas curtas ou vagas.
    Dados disponíveis:
    {context}

    Responda com base nos dados fornecidos acima.
    """
)

prompt_agent = """Você é um agente inteligente especializado em análise de dados. Sua função é interpretar e analisar os dados fornecidos para fornecer respostas completas e detalhadas. Você deve realizar as seguintes tarefas com base no dataset carregado:

1. **Análise Descritiva**:
   - Resuma as características principais do dataset, como número de linhas e colunas, tipos de dados e possíveis valores ausentes.
   - Forneça estatísticas básicas (média, mediana, moda, desvio padrão) para colunas numéricas, como idade, valor de crédito, e duração.
   - Identifique padrões ou insights relevantes (e.g., distribuição de risco, principais propósitos de crédito).

2. **Análise Estatística**:
   - Realize uma análise estatística detalhada. Por exemplo, calcule correlações entre variáveis (e.g., idade e risco de crédito).
   - Identifique as variáveis mais influentes para o risco de crédito ou para o valor aprovado.

3. **Análise Preditiva**:
   - Utilize o dataset para prever resultados ou fornecer recomendações com base em padrões observados.
   - Simule resultados ou cenários com base nas perguntas do usuário. Por exemplo, "Qual seria o risco associado a uma pessoa de 30 anos com moradia própria e conta poupança moderada?"

Ao realizar qualquer análise, seja detalhado em suas explicações e justifique suas conclusões com base nos dados.
Se não for possível responder diretamente a uma pergunta, explique o motivo e sugira o próximo passo ou uma abordagem alternativa.
"""

context_file = "dataset/context_base.txt"

if not os.path.exists(context_file):
    context_base = agent_executor.invoke(prompt_agent)
    if context_base['output']:
        open(context_file, "w").write(context_base['output'])
else:
    context_base = {"output": open(context_file).read()}


def consultar_agente(pergunta):
    try:

        context = agent_executor.invoke(pergunta)

        context['output'] = context['output'] + context_base['output']

        if len(context['output']) > 7000:
            context['output'] = context['output'][:7000]

        mensagem_sistema = SystemMessage(content=prompt_template.format(context=context))
        mensagem_usuario = HumanMessage(content=pergunta)

        resposta = llm([mensagem_sistema, mensagem_usuario])
        return resposta.content
    except OutputParserException as e:
        print(f"Erro ao analisar a saída do LLM: {e}")
        return "Houve um erro ao processar sua solicitação. Por favor, tente novamente."

# consulta = "Quais são os principais fatores que influenciam a aprovação de crédito?"
# resposta = consultar_agente(consulta)
# consulta2 = "Qual é a média de idade dos clientes que solicitam crédito?"
# resposta2 = consultar_agente(consulta2)
# consulta3 = "Qual é a distribuição de risco de crédito por faixa etária?"
# resposta3 = consultar_agente(consulta3)
# consulta4 = "Quais são os propósitos mais comuns para solicitação de crédito?"
# resposta4 = consultar_agente(consulta4)
