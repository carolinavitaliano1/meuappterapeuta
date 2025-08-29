import streamlit as st
import google.generativeai as genai

# --- Configuração da Página e da API ---
# NOTA: Substitua "SUA_API_KEY_AQUI" pela sua chave de API do Google AI Studio.
# Você pode obter uma em: https://makersuite.google.com/app/apikey
try:
    from api_key import GOOGLE_API_KEY
except ImportError:
    GOOGLE_API_KEY = "SUA_API_KEY_AQUI"

st.set_page_config(
    page_title="Gerador de Roteiros Pedagógicos",
    page_icon="✨",
    layout="wide"
)

# Configurando o modelo Gemini
if GOOGLE_API_KEY != "SUA_API_KEY_AQUI":
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

# --- Cabeçalho e Título ---
st.title("Painel de Roteiros de Atividades ✨")
st.markdown("Use o menu à esquerda para navegar entre os roteiros existentes ou crie um novo com o poder da IA.")

# --- Barra Lateral (Sidebar) ---
st.sidebar.header("Navegação")
pagina_selecionada = st.sidebar.radio(
    "Selecione uma opção:",
    ["Criar Roteiro com IA", "Ver Roteiros Existentes"]
)

# --- Funcionalidade Principal ---

if pagina_selecionada == "Criar Roteiro com IA":
    st.header("✨ Criar Roteiro Personalizado com IA")
    st.markdown("Preencha os campos abaixo para gerar uma atividade sob medida.")

    if not model:
        st.error("Por favor, configure sua API Key do Google AI no código para usar esta funcionalidade.")
    else:
        # --- NOVOS CAMPOS ADICIONADOS AQUI ---
        col1, col2 = st.columns(2)
        with col1:
            nome_paciente = st.text_input("Nome do Paciente / Aluno")
        with col2:
            numero_sessao = st.number_input("Número da Sessão", min_value=1, step=1)
        
        with st.form("roteiro_form"):
            st.markdown("---")
            st.subheader("Detalhes para a Criação do Roteiro")
            
            tema_aula = st.text_input("Qual o tema da aula ou conteúdo a ser trabalhado?", "Consciência fonológica")
            
            faixa_etaria = st.selectbox(
                "Qual a faixa etária da criança/aluno?",
                ("0-1 ano", "1-2 anos", "2-3 anos", "3-4 anos", "4-5 anos", "5-6 anos", "6-8 anos", "8-10 anos")
            )

            dificuldade = st.text_input("Qual a principal dificuldade ou transtorno do aluno?", "Dislexia")
            
            ferramentas = st.multiselect(
                "Quais ferramentas digitais você gostaria de usar? (Opcional)",
                ["Wordwall", "Genially", "Padlet", "Kahoot", "Jamboard", "Pixton", "Canva", "YouTube"]
            )
            
            # --- NOVO CAMPO DE COMANDOS ADICIONADO AQUI ---
            comandos_ia = st.text_area(
                "Informações Adicionais ou Comandos para a IA", 
                placeholder="Ex: Crie uma história curta com o personagem. Use frases simples e repita a palavra-chave 'barco' pelo menos 3 vezes."
            )
            
            submitted = st.form_submit_button("Gerar Roteiro")

            if submitted:
                with st.spinner("Aguarde, a IA está criando um roteiro incrível..."):
                    # Construindo o prompt para a IA
                    prompt_parts = [
                        "Crie um roteiro de aula ou intervenção pedagógica estruturado.",
                        f"Tema principal: {tema_aula}.",
                        f"Faixa etária: {faixa_etaria}.",
                        f"Foco da adaptação: {dificuldade}.",
                        "Estruture a resposta com: Objetivo, Ferramentas Sugeridas e um Passo a Passo detalhado (Acolhida, Apresentação, Desenvolvimento, Síntese, Encerramento).",
                        "Seja criativo e didático."
                    ]
                    if ferramentas:
                        prompt_parts.append(f"Incorpore o uso das seguintes ferramentas: {', '.join(ferramentas)}.")
                    
                    # --- ADICIONANDO OS NOVOS COMANDOS AO PROMPT ---
                    if comandos_ia:
                        prompt_parts.append(f"Instrução adicional importante do terapeuta: {comandos_ia}")

                    prompt = "\n".join(prompt_parts)
                    
                    try:
                        response = model.generate_content(prompt)
                        st.subheader(f"📝 Roteiro Gerado para: {nome_paciente} (Sessão {numero_sessao})")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao gerar o roteiro: {e}")


elif pagina_selecionada == "Ver Roteiros Existentes":
    st.header("📚 Banco de Roteiros de Atividades")
    st.markdown("Aqui você encontrará os 40 roteiros que desenvolvemos anteriormente.")

    # Exemplo de como exibir alguns roteiros (em um app real, isso viria de um banco de dados)
    st.subheader("Roteiro 19 – Gincana de Jogos Rápidos (Adaptado para TDAH)")
    st.markdown("""
    - **Objetivo:** Revisar conteúdos de forma dinâmica, mantendo a atenção através da novidade e da competição amigável.
    - **Ferramentas sugeridas:** Baamboozle, Wordwall, LearningApps.
    - **Passo a passo:**
        - **Acolhida (1 min):** Anunciar uma "gincana de jogos" com 3 rodadas rápidas para criar expectativa.
        - **Apresentação (1 min):** Explicar que cada jogo será diferente e rápido, mantendo o ritmo acelerado.
        - **Desenvolvimento (15 min):** Realizar rodadas de 5 minutos cada, alternando entre a competição em equipe do Baamboozle, um jogo de "Roda Aleatória" do Wordwall e uma atividade de "Arrastar e Soltar" do LearningApps.
        - **Síntese (2 min):** Perguntar qual dos três jogos foi o favorito e por quê, permitindo uma breve expressão de preferência.
        - **Encerramento (1 min):** Comemorar a participação e os pontos de todos na gincana, focando no esforço e na diversão.
    """)

    st.subheader("Roteiro 21 – Mapa Interativo de Sons (Adaptado para Dislexia)")
    st.markdown("""
    - **Objetivo:** Fortalecer a consciência fonológica e a associação grafema-fonema com forte suporte de áudio e visual.
    - **Ferramentas sugeridas:** ThingLink, Genially.
    - **Passo a passo:**
        - **Acolhida (2 min):** Iniciar com um som de um animal (áudio) e pedir para adivinhar qual é e qual a letra inicial do nome.
        - **Apresentação (3 min):** Apresentar uma imagem interativa (ex: uma fazenda) no ThingLink com hotspots. Explicar que ao clicar nos animais, eles ouvirão o nome e o som da letra inicial.
        - **Desenvolvimento (10 min):** O paciente explora a imagem. Ao clicar em um hotspot (ex: na VACA), ele vê a palavra escrita e pode clicar para ouvir a narração: "Vaca começa com o som /v/". O desafio é encontrar todos os objetos que começam com um som específico.
        - **Síntese (3 min):** O paciente deve falar em voz alta outras duas palavras que também comecem com o mesmo som, sem a necessidade de escrevê-las.
        - **Encerramento (2 min):** Parabenizar pela exploração sonora e reforçar o som aprendido.
    """)
    
    # Adicione mais roteiros aqui conforme necessário...
