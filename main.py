import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import random

NOME_ARQUIVO_SAVE = "savegame.json"

def configurar_ia():
    load_dotenv() 
    api_key = os.getenv("GEMINI_KEY")
    if not api_key:
        raise ValueError("Chave de API do Gemini não encontrada. Verifique seu arquivo .env")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

def iniciar_aventura(personagem):
    print("=============================================")
    print("Bem-vindo à sua história!")
    print(f"""Você e {personagem} crescem juntos.""")
    print("=============================================\n")

def criar_novo_personagem():
     return {
        "nome": "Gabriel Neves",
        "energia": 100,
        "localizacao_atual": "Acampamento na clareira",
        "inventario": ["Adaga de Ferro", "Pederneira"],
        "dia_da_jornada": 1
    }

def salvar_jogo(dados_personagem):
    print("\n[Salvando sua jornada...]")
    with open(NOME_ARQUIVO_SAVE, 'w', encoding='utf-8') as f:
        json.dump(dados_personagem, f, indent=4, ensure_ascii=False)

def carregar_jogo():
    if not os.path.exists(NOME_ARQUIVO_SAVE):
        print("[Nenhuma jornada encontrada. Começando uma nova saga!]")
        return criar_novo_personagem()
    
    print("[Continuando sua jornada...]")
    with open(NOME_ARQUIVO_SAVE, 'r', encoding='utf-8') as f:
        return json.load(f)

def obter_objetivo_do_usuario():
    objetivo = input("Qual é a sua missão para hoje? (Ex: Programar por 1 hora): ")
    return objetivo

def verificar_progresso(objetivo):
    print(f"\nAo final do dia...")
    resposta = input(f"Você cumpriu sua missão de '{objetivo}'? (s/n): ")
    
    return resposta.lower() == 's'

def aplicar_consequencias(personagem, progresso_do_dia):
    if progresso_do_dia:
        energia_recuperada = 10
        personagem['energia'] = min(100, personagem['energia'] + energia_recuperada)

        itens_encontrados = ["Moeda de Prata", "Fruta Silvestre Energizante", "Pedaço de Mapa Antigo", "Erva Curativa"]
        item_descoberto = random.choice(itens_encontrados)
        personagem['inventario'].append(item_descoberto)
        
        return f"Você encontrou um(a) '{item_descoberto}' e recuperou um pouco de suas energias."
    
    energia_perdida = 15
    personagem['energia'] = max(0, personagem['energia'] - energia_perdida)
    

    return f"A falha de hoje drenou suas energias, deixando-o mais fraco."

def gerar_narrativa_com_ia(modelo, objetivo, cumpriu_objetivo, personagem, consequencia_mecanica):
    status_desfecho = "um triunfo retumbante" if cumpriu_objetivo else "um revés desafiador"

    prompt = f"""
    Como um **Mestre de Jogo de RPG**, crie um trecho de narrativa de **fantasia sombria e medieval**, focado na jornada do protagonista.

    ESTADO ATUAL DO PROTAGONISTA:
    - Nome: {personagem['nome']}
    - Energia: {personagem['energia']}%
    - Localização: {personagem['localizacao_atual']}
    - Itens: {', '.join(personagem['inventario'])}
    - Dia da Jornada: {personagem['dia_da_jornada']}

    EVENTOS DE HOJE: 
    - O objetivo do protagonista era: "{objetivo}".
    - Resultado: A missão {status_desfecho}.
    - Consequência Direta: {consequencia_mecanica}

    Com base nesse resultado, descreva em um **parágrafo vívido e conciso (3 a 5 frases)** o imediato **próximo capítulo** na aventura do protagonista.
    A narrativa deve ser:
    - **Informativa:** Deixe claro o impacto do desfecho nos planos do protagonista.
    - **Imersiva:** Utilize linguagem evocativa que transporte o leitor para o mundo do RPG.
    - **Direcionada:**
        - Se foi um triunfo: Mostre um avanço significativo, a revelação de uma nova oportunidade ou um ganho tangível.
        - Se foi um revés: Introduza uma nova complicação, a perda de um recurso vital, ou a aparição de um antagonista inesperado.
    - **Proibido:** Não utilize as palavras "missão", "objetivo", "tarefa" ou "quest" na sua resposta.
    - **Final inspirador:** O parágrafo deve terminar com uma frase que instigue a curiosidade sobre o futuro da jornada.
    """

    print("\n--- Capítulo do Dia ---")
    try:
        resposta_ia = modelo.generate_content(prompt)
        print(resposta_ia.text)
    except Exception as e:
        print(f"Ocorreu um erro ao contatar a IA: {e}")
        print("Hoje foi um dia de acumular experiências e refletir sobre o passado.");

    print("-----------------------\n")


def main():
    try:
        personagem_atual = carregar_jogo()
        modelo_ia = configurar_ia()
        iniciar_aventura(personagem_atual['nome'])
        objetivo_diario = obter_objetivo_do_usuario()
        progresso_do_dia = verificar_progresso(objetivo_diario)
        consequencia_mecanica = aplicar_consequencias(personagem_atual, progresso_do_dia)
        print(f"\n[CONSEQUÊNCIA: {consequencia_mecanica}]")
        gerar_narrativa_com_ia(modelo_ia, objetivo_diario, progresso_do_dia, personagem_atual, consequencia_mecanica)
        personagem_atual['dia_da_jornada'] += 1
        salvar_jogo(personagem_atual)
        print("Sua saga continuará amanhã...")
    except ValueError as e:
        print(f"Erro de Configuração: {e}")

if __name__ == "__main__":
    main()