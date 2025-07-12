import os
from dotenv import load_dotenv
import google.generativeai as genai

def configurar_ia():
    load_dotenv() 
    api_key = os.getenv("GEMINI_KEY")
    if not api_key:
        raise ValueError("Chave de API do Gemini não encontrada. Verifique seu arquivo .env")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

def iniciar_aventura():
    print("=============================================")
    print("Bem-vindo à sua história!")
    print("Você e seu personagem crescem juntos.")
    print("=============================================\n")

def obter_objetivo_do_usuario():
    objetivo = input("Qual é a sua missão para hoje? (Ex: Programar por 1 hora): ")
    return objetivo

def verificar_progresso(objetivo):
    print(f"\nAo final do dia...")
    resposta = input(f"Você cumpriu sua missão de '{objetivo}'? (s/n): ")
    
    return resposta.lower() == 's'

def gerar_narrativa_com_ia(modelo, objetivo, cumpriu_objetivo):
    status_desfecho = "um triunfo retumbante" if cumpriu_objetivo else "um revés desafiador"

    prompt = f"""
    Como um **Mestre de Jogo de RPG**, crie um trecho de narrativa de **fantasia sombria e medieval**, focado na jornada do protagonista.

    O protagonista estava focado em: "{objetivo}".
    O desfecho de seu empreendimento de hoje foi {status_desfecho}.

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
        modelo_ia = configurar_ia()
        iniciar_aventura()
        objetivo_diario = obter_objetivo_do_usuario()
        progresso_do_dia = verificar_progresso(objetivo_diario)
        gerar_narrativa_com_ia(modelo_ia, objetivo_diario, progresso_do_dia)
        print("Sua saga continuará amanhã...")
    except ValueError as e:
        print(f"Erro de Configuração: {e}")

if __name__ == "__main__":
    main()