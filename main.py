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

def criar_novo_personagem(dados_genesis, estilos):
     return {
            "nome": dados_genesis['protagonista']['nome'],
            "energia": 100,
            "localizacao_atual": dados_genesis['cenario_mundo'].split('.')[0], # Pega a primeira frase do cenário como local
            "inventario": ["Roupas de Viajante"],
            "dia_da_jornada": 1,
            "estilos_preferidos": estilos,
            "titulo_saga": dados_genesis['titulo_saga'],
            "background_personagem": dados_genesis['protagonista']['background'],
            "conflito_central": dados_genesis['conflito_central'],
            "personagens_chave": dados_genesis['personagens_chave'],
            "trackers": [
                {
                    "nome_tracker": tracker['nome_tracker'],
                    "descricao": tracker['descricao'],
                    "valor": tracker['valor_inicial'],
                    "valor_maximo": tracker['valor_maximo']
                } for tracker in dados_genesis['trackers_narrativos']
            ],
            "log_narrativo": [dados_genesis['capitulo_zero']] # O Capítulo Zero é a primeira entrada do log!
        }

def salvar_jogo(dados_personagem):
    print("\n[Salvando sua jornada...]")
    with open(NOME_ARQUIVO_SAVE, 'w', encoding='utf-8') as f:
        json.dump(dados_personagem, f, indent=4, ensure_ascii=False)

def carregar_jogo(modelo):
    if not os.path.exists(NOME_ARQUIVO_SAVE):
        print("[Nenhuma jornada encontrada. Começando uma nova saga!]")
        estilos = ["As Crônicas do Gelo e Fogo", "One Piece", "Raul Seixas"]
        dados_genesis = gerar_genesis_da_saga(modelo, estilos)

        if not dados_genesis:
            raise Exception("Não foi possível criar o mundo inicial. Tente novamente.")

        personagem = criar_novo_personagem()

        print("\n" + "="*50)
        print(f"BEM-VINDO A: {personagem['titulo_saga'].upper()}")
        print("="*50)
        print("\n--- CAPÍTULO ZERO ---")
        print(personagem['log_narrativo'][0])
        print("---------------------\n")
        
        salvar_jogo(personagem)
        return personagem
    

    

def gerar_genesis_da_saga(modelo, estilos_preferidos):
    print("[Forjando uma nova saga nos reinos da imaginação...]")
    
    prompt_genesis = f"""
    Você é um "Arquiteto de Mundos", um criador de universos para jogos de RPG, com a habilidade de mesclar estilos e criar tramas envolventes.

    ### INSPIRAÇÃO ESTILÍSTICA
    Baseie TODA a sua criação na seguinte fusão de estilos e universos: {', '.join(estilos_preferidos)}.

    ### TAREFA
    Sua missão é gerar os elementos fundamentais de uma nova saga. Sua resposta DEVE SER um objeto JSON válido e nada mais, contendo as seguintes chaves:

    - "titulo_saga": (String) Um título épico e evocativo para esta saga.
    - "protagonista": (Objeto) Detalhes do personagem principal.
        - "nome": (String) Um nome adequado ao estilo da saga.
        - "background": (String) Um parágrafo (4-5 frases) descrevendo o passado do protagonista, sua origem e o que o torna único.
    - "conflito_central": (String) Um parágrafo descrevendo a trama principal da história. Qual é a grande ameaça, o mistério a ser resolvido ou o objetivo final da saga?
    - "cenario_mundo": (String) Um parágrafo descrevendo o mundo ou universo onde a história se passa.
    - "personagens_chave": (Lista de Objetos) Uma lista com 2 NPCs (personagens não-jogáveis) iniciais.
        - "nome": (String) Nome do NPC.
        - "papel": (String) O papel do NPC na história (ex: "Mentor relutante", "Rival misterioso", "Guardião de um segredo").
        - "descricao": (String) Uma breve descrição da aparência e personalidade do NPC.
     - "trackers_narrativos": (Lista de Objetos) Uma lista com 2 a 3 "medidores" que serão usados para rastrear o progresso do protagonista NESTE universo específico.
        - "nome_tracker": (String) O nome do medidor (ex: "Confiança da Tripulação", "Nível de Suspeita da Corporação", "Laços com a Família Montecchio").
        - "descricao": (String) O que este medidor representa na história.
        - "valor_inicial": (Inteiro) O valor inicial para este medidor.
        - "valor_maximo": (Inteiro) O valor máximo possível.
    - "capitulo_zero": (String) O parágrafo narrativo inicial. Este texto deve apresentar o protagonista em seu cenário, introduzir a "situação incitante" que dá início à trama e terminar com uma frase que leva diretamente aos eventos do Dia 1.

    Garanta que todos os elementos sejam coesos e reflitam a INSPIRAÇÃO ESTILÍSTICA fornecida.
    """
    
    try:
        print("CHEGOU AQUI")
        resposta_ia = modelo.generate_content(prompt_genesis)
        if not resposta_ia.text:
            print("\n!!! RESPOSTA DA IA ESTÁ VAZIA !!!")
            print("A resposta provavelmente foi bloqueada pelos filtros de segurança.")
            # O prompt_feedback nos dá o motivo exato do bloqueio.
            print(f"Feedback do Prompt: {resposta_ia.prompt_feedback}\n")
        print(resposta_ia.text)
        return json.loads(resposta_ia.text)
    except Exception as e:
        print(f"Erro crítico ao gerar o gênesis da saga: {e}")
        return None
    
def resumir_saga(modelo, log_narrativo):

    if len(log_narrativo) < 3:
        return "A jornada está apenas começando."

    historia_completa = "\n\n".join(log_narrativo)

    prompt_resumo = f"""
    Você é um escriba inteligente e conciso. A seguir está o diário de bordo de uma jornada de um protagonista. 
    Sua única tarefa é ler todo o diário e escrever um resumo em um único parágrafo (cerca de 4-6 frases).
    O resumo deve capturar os eventos mais importantes, os personagens chave encontrados (se houver), e o estado emocional geral do protagonista.

    DIÁRIO DE BORDO:
    {historia_completa}

    RESUMO CONCISO:
    """
    try:
        resposta_ia = modelo.generate_content(prompt_resumo)
        return resposta_ia.text
    except Exception as e:
        print(f"Erro ao resumir a saga: {e}")
        return "Houve um lapso na memória da jornada..."

def obter_objetivo_do_usuario():
    objetivo = input("Qual é a sua missão para hoje? (Ex: Programar por 1 hora): ")
    return objetivo

def verificar_progresso(objetivo):
    print(f"\nAo final do dia...")
    resposta = input(f"Você cumpriu sua missão de '{objetivo}'? (s/n): ")
    
    return resposta.lower() == 's'

def aplicar_consequencias(modelo, personagem, objetivo, progresso_do_dia):

    trackers_atuais = personagem['trackers']

    prompt_juiz = f"""
    Você é um "Juiz de Consequências" imparcial. Sua tarefa é determinar o impacto mecânico de uma ação em um universo narrativo.

    ### CONTEXTO
    - Objetivo do Dia: "{objetivo}"
    - Resultado: {'Sucesso' if progresso_do_dia else 'Fracasso'}
    - Trackers Atuais do Universo: {trackers_atuais}

    ### TAREFA
    Com base no resultado, decida qual(is) tracker(s) devem ser modificados. Sua resposta deve ser um objeto JSON com duas chaves:
    1. "modificacoes": Uma lista de objetos, cada um com "nome_tracker" e "novo_valor".
    2. "descricao_mecanica": Uma frase descrevendo o porquê da mudança (ex: "A sua honestidade aumentou a afeição do Sr. Darcy.").

    Exemplo de Resposta para um Sucesso:
    {{
        "modificacoes": [{{ "nome_tracker": "Afeição do Sr. Darcy", "novo_valor": 25 }}],
        "descricao_mecanica": "Uma conversa espirituosa e inteligente no jardim aumentou a admiração do Sr. Darcy."
    }}
    """
    try:
        # 1. PARSE DA RESPOSTA: A resposta da IA é um texto. Precisamos convertê-la para um dicionário Python.
        resposta_ia = modelo.generate_content(prompt_juiz)
        dados_consequencia = json.loads(resposta_ia.text)
        
        modificacoes = dados_consequencia.get('modificacoes', [])
        descricao_mecanica = dados_consequencia.get('descricao_mecanica', "Os ventos do destino sopram...")

        # 2. APLICAÇÃO DIRETA DAS MODIFICAÇÕES
        for mod in modificacoes:
            nome_tracker = mod.get('nome_tracker')
            novo_valor = mod.get('novo_valor')

            if nome_tracker and novo_valor is not None:
                # 3. VERIFICAÇÃO: Checa se o tracker existe no estado do nosso personagem.
                if nome_tracker in personagem['trackers']:
                    
                    # 4. BUSCA PELAS REGRAS (VALOR MÁXIMO):
                    # Para limitar o valor, precisamos encontrar a definição original do tracker.
                    # Isso pressupõe que você salvou as definições do Gênesis no personagem.
                    definicao_tracker = next((d for d in personagem.get('tracker_definitions', []) if d['nome_tracker'] == nome_tracker), None)
                    
                    if definicao_tracker:
                        valor_maximo = definicao_tracker.get('valor_maximo', 100) # Padrão de 100 se não encontrar
                        
                        # Aplica o novo valor, garantindo que ele fique entre 0 e o máximo.
                        personagem['trackers'][nome_tracker] = max(0, min(valor_maximo, novo_valor))
                    else:
                        # Se não houver definição, apenas aplica o valor (menos seguro, mas funciona)
                        personagem['trackers'][nome_tracker] = novo_valor
                        
                    print(f"[Estado Atualizado] {nome_tracker}: {personagem['trackers'][nome_tracker]}")

                else:
                    print(f"[Aviso] O Juiz de IA tentou modificar um tracker desconhecido: '{nome_tracker}'")
        
        return descricao_mecanica

    except (json.JSONDecodeError, AttributeError, KeyError) as e:
        print(f"Erro ao processar consequência da IA: {e}")
        return "Um evento misterioso ocorreu, mas suas consequências ainda não são claras."
   

def gerar_narrativa_com_ia(modelo, objetivo, cumpriu_objetivo, personagem, consequencia_mecanica, resumo_saga):
    status_desfecho = "um triunfo retumbante" if cumpriu_objetivo else "um revés desafiador"

    prompt = f"""
        Você é Aetherius, um Mestre de Jogo de RPG e um contador de histórias de classe mundial, conhecido por criar sagas imersivas e coerentes.

        ### INSTRUÇÕES GERAIS
        1.  **Estilo e Tom:** Inspire-se fortemente nos seguintes universos: {', '.join(personagem['estilos_preferidos'])}. Adapte sua prosa para refletir a atmosfera desses mundos.
        2.  **Formato da Resposta:** Sua resposta deve ser um único parágrafo conciso, contendo de 3 a 5 frases. Não inclua preâmbulos como "Claro, aqui está..." ou qualquer texto fora do parágrafo da história.
        3.  **Linguagem Proibida:** Jamais utilize as palavras "missão", "objetivo", "tarefa" ou "quest".
        4.  **Finalização:** A última frase do parágrafo deve ser inspiradora ou intrigante, deixando um gancho para o futuro.

        ### CONTEXTO DA SAGA
        - Título da Saga: {personagem['titulo_saga']}
        - Trama Principal (O Conflito Central): {personagem['conflito_central']}
         - Personagens Relevantes no Mundo: {', '.join([p['nome'] + ' (' + p['papel'] + ')' for p in personagem['personagens_chave']])}
        -   **Resumo da Jornada Até Agora:** {resumo_saga}
        -   **Estado Atual do Protagonista:**
            -   Nome: {personagem['nome']}
            -   Energia: {personagem['energia']}%
            -   Localização: {personagem['localizacao_atual']}
            -   Inventário: {', '.join(personagem['inventario'])}
            -   Dia da Jornada: {personagem['dia_da_jornada']}
        -   **Eventos Recentes (Hoje):**
            -   Intenção do Dia: O esforço do protagonista foi direcionado a "{objetivo}".
            -   Desfecho: {'Triunfo' if status_desfecho else 'Revés'}.
            -   Consequência Mecânica: {consequencia_mecanica}.

        ### TAREFA
        Baseado em TODO o contexto fornecido, escreva o próximo capítulo da saga.
        -   Sua narrativa deve ser uma continuação direta e coerente do resumo da jornada.
        -   Incorpore o impacto dos "Eventos Recentes" de forma vívida.
        -   **Se o desfecho foi um Triunfo:** A narrativa deve mostrar um avanço claro, uma nova oportunidade ou uma descoberta significativa.
        -   **Se o desfecho foi um Revés:** A narrativa deve introduzir uma complicação, um obstáculo inesperado ou a perda de algo importante.

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
        personagem_atual = carregar_jogo(modelo_ia)
        iniciar_aventura(personagem_atual['nome'])
        objetivo_diario = obter_objetivo_do_usuario()
        progresso_do_dia = verificar_progresso(objetivo_diario)
        resumo_da_jornada = resumir_saga(modelo_ia, personagem_atual['log_narrativo'])
        consequencia_mecanica = aplicar_consequencias(personagem_atual, progresso_do_dia)
        print(f"\n[CONSEQUÊNCIA: {consequencia_mecanica}]")
        narrativa_gerada = gerar_narrativa_com_ia(modelo_ia, objetivo_diario, progresso_do_dia, personagem_atual, consequencia_mecanica, resumo_da_jornada)

        if narrativa_gerada:
            personagem_atual['log_narrativo'].append(narrativa_gerada)

        personagem_atual['dia_da_jornada'] += 1
        salvar_jogo(personagem_atual)
        print("Sua saga continuará amanhã...")
    except ValueError as e:
        print(f"Erro de Configuração: {e}")

if __name__ == "__main__":
    main()