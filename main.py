import threading
import time
from tkinter import Button, END, Label, Text, Tk

import markdown
from tkinterhtml import HtmlFrame

from agente import consultar_agente

historico_html = ""


def enviar_pergunta(event=None):
    """
    Captura a entrada do usuário, exibe no chat e inicia o processamento.
    """
    pergunta = entrada_texto.get("1.0", END).strip()
    if pergunta:
        adicionar_markdown(f"**Você:** {pergunta}\n", color="blue")
        entrada_texto.delete("1.0", END)

        threading.Thread(target=animar_processamento).start()
        threading.Thread(target=processar_resposta, args=(pergunta,)).start()


def processar_resposta(pergunta):
    """
    Processa a resposta do agente em uma thread separada.
    """
    try:
        resposta = consultar_agente(pergunta)  # Consulta o agente
        if not resposta:
            resposta = "Desculpe, não consegui gerar uma resposta."
    except Exception as e:
        resposta = f"Ocorreu um erro: {e}"

    adicionar_markdown(f"**Chatbot:** {resposta}\n\n")

    indicador["text"] = ""


def animar_processamento():
    """
    Exibe uma mensagem de processamento dinâmica enquanto a resposta é gerada.
    """
    textos = ["Processando", "Processando.", "Processando..", "Processando..."]
    while indicador["text"] != "":
        for texto in textos:
            if indicador["text"] == "":
                break
            indicador["text"] = texto
            time.sleep(0.5)


def adicionar_markdown(texto_markdown, color="black"):
    """
    Converte o texto Markdown para HTML e adiciona ao histórico do HtmlFrame.
    """
    global historico_html
    html_content = markdown.markdown(texto_markdown)
    html_completo = f"<span style='font-size: 24px; color:{color}'>{html_content}</span>"
    historico_html += html_completo
    janela_respostas.set_content(historico_html)


def configurar_janela():
    """
    Configura a janela para abrir centralizada na tela.
    """
    largura_janela = int(janela.winfo_screenwidth() / 2)
    altura_janela = int(janela.winfo_screenheight() / 2)

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    x_centralizado = (largura_tela - largura_janela) // 2
    y_centralizado = (altura_tela - altura_janela) // 2

    janela.geometry(f"{largura_janela}x{altura_janela}+{x_centralizado}+{y_centralizado}")


janela = Tk()
janela.title("Chatbot de Análise de Créditos")
configurar_janela()
janela.attributes("-topmost", True)
janela.resizable(True, True)

indicador = Label(janela, text="", fg="orange", font=("Arial", 20))
indicador.grid(row=1, column=0, padx=10, pady=5, sticky="w")

entrada_texto = Text(janela, height=3, width=60, wrap="word", font=("Arial", 20))
entrada_texto.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
entrada_texto.bind("<Return>", enviar_pergunta)

botao_enviar = Button(janela, text="Enviar", command=enviar_pergunta, font=("Arial", 20))
botao_enviar.grid(row=2, column=1, padx=10, pady=10)

janela_respostas = HtmlFrame(janela, horizontal_scrollbar="auto", vertical_scrollbar="auto")
janela_respostas.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

adicionar_markdown(
    "**Bem-vindo ao Chatbot de Análise de Créditos!**\n\nPergunte sobre elegibilidade, simulações e dicas de crédito.\n\n")

janela.mainloop()
