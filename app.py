import streamlit as st
from PyPDF2 import PdfReader
import io

# Configuração da Página
st.set_page_config(page_title="NeuroTech Evoluir - Terapeuta AI", layout="wide")

# --- FUNÇÕES AUXILIARES ---

def extract_text_from_pdf(file):
    """Extrai texto de um ficheiro PDF carregado."""
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(file):
    """Extrai texto de um ficheiro TXT carregado."""
    return file.getvalue().decode("utf-8")

def generate_session_prompt(patient_info, goals, knowledge_base):
    """Cria o prompt para a IA com base nos dados do paciente e no conhecimento adicionado."""
    
    prompt = f"""
    Atua como um Terapeuta Especialista e cria um plano de sessão detalhado.
    
    --- DADOS DO PACIENTE ---
    Nome: {patient_info.get('name', 'N/A')}
    Idade: {patient_info.get('age', 'N/A')}
    Diagnóstico/Contexto: {patient_info.get('diagnosis', 'N/A')}
    
    --- OBJETIVOS DA SESSÃO ---
    {goals}
    
    --- MATERIAL DE REFERÊNCIA (BASE DE CONHECIMENTO) ---
    Utiliza as seguintes informações extraídas de livros/artigos/documentos fornecidos pelo terapeuta para guiar a metodologia desta sessão:
    
    {knowledge_base[:15000]} # Limite de caracteres para não exceder tokens (ajustável)
    
    --- TAREFA ---
    Cria uma sessão estruturada (Acolhimento, Desenvolvimento, Fecho) aplicando as técnicas mencionadas no Material de Referência.
    """
    return prompt

# --- INTERFACE PRINCIPAL ---

def main():
    # Título e Cabeçalho
    st.title("🧠 NeuroTech Evoluir")
    st.subheader("Assistente de Planeamento de Sessões Terapêuticas")
    
    st.markdown("""
    Esta ferramenta ajuda terapeutas a criar sessões personalizadas. 
    **Novidade:** Agora pode anexar livros, artigos ou transcrições de vídeos para a IA usar como base!
    """)
    
    # Dividir o layout em colunas
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("📂 **1. Dados do Paciente e Objetivos**")
        name = st.text_input("Nome do Paciente")
        age = st.number_input("Idade", min_value=0, max_value=120, step=1)
        diagnosis = st.text_area("Diagnóstico ou Contexto Clínico", placeholder="Ex: TEA, Ansiedade Generalizada, TDAH...")
        session_goals = st.text_area("Objetivo desta Sessão", placeholder="Ex: Trabalhar regulação emocional usando técnicas cognitivas...")

    with col2:
        st.warning("📚 **2. Base de Conhecimento (Anexos)**")
        st.markdown("Carregue livros (PDF), artigos ou notas de vídeo para a IA estudar antes de criar a sessão.")
        
        uploaded_files = st.file_uploader(
            "Arraste os ficheiros aqui", 
            type=["pdf", "txt"], 
            accept_multiple_files=True
        )
        
        knowledge_text = ""
        if uploaded_files:
            with st.spinner("A processar documentos..."):
                for uploaded_file in uploaded_files:
                    try:
                        if uploaded_file.name.endswith(".pdf"):
                            knowledge_text += f"\n--- Fonte: {uploaded_file.name} ---\n"
                            knowledge_text += extract_text_from_pdf(uploaded_file)
                        elif uploaded_file.name.endswith(".txt"):
                            knowledge_text += f"\n--- Fonte: {uploaded_file.name} ---\n"
                            knowledge_text += extract_text_from_txt(uploaded_file)
                    except Exception as e:
                        st.error(f"Erro ao ler {uploaded_file.name}: {e}")
                
                if knowledge_text:
                    st.success(f"Base de conhecimento carregada! ({len(knowledge_text)} caracteres extraídos)")
                    with st.expander("Ver conteúdo extraído (apenas para verificação)"):
                        st.write(knowledge_text[:1000] + "...")

    # Botão de Geração
    st.markdown("---")
    if st.button("✨ Gerar Sessão com IA", type="primary"):
        if not diagnosis or not session_goals:
            st.error("Por favor, preencha o diagnóstico e os objetivos da sessão.")
        else:
            # Preparar os dados
            patient_data = {"name": name, "age": age, "diagnosis": diagnosis}
            
            # Construir o Prompt Final
            final_prompt = generate_session_prompt(patient_data, session_goals, knowledge_text)
            
            # --- INTEGRAÇÃO COM IA (Simulação) ---
            # Aqui entraria a chamada real para OpenAI (GPT-4), Anthropic, etc.
            # Como não tenho a sua API Key, simulo a resposta abaixo.
            
            with st.spinner("A IA está a ler os seus anexos e a planear a sessão..."):
                
                # EXEMPLO DE CHAMADA REAL (Comentado):
                # import openai
                # response = openai.ChatCompletion.create(
                #     model="gpt-4",
                #     messages=[{"role": "user", "content": final_prompt}]
                # )
                # result = response.choices[0].message.content
                
                # Resposta Simulada para demonstração
                st.markdown("### 📝 Plano de Sessão Gerado")
                st.markdown(f"""
                **Paciente:** {name} ({age} anos)  
                **Baseado em:** {len(uploaded_files)} ficheiros de referência.

                ---
                
                #### 1. Acolhimento (10 min)
                *Revisão do estado atual baseada no diagnóstico de {diagnosis}.*
                - **Atividade:** Check-in emocional.
                - **Conexão com a teoria:** Utilizando o conceito extraído dos anexos sobre 'vínculo terapêutico'.

                #### 2. Desenvolvimento (30 min)
                *Foco: {session_goals}*
                - **Técnica Aplicada:** Se carregou um livro sobre TCC, aqui seria aplicada a reestruturação cognitiva.
                - **Dinâmica:** Exercício prático conforme descrito no documento carregado.
                
                *(Nota: Esta é uma simulação. Para ver o resultado real, integre a sua chave de API no código).*
                """)
                
                # Mostrar o prompt que seria enviado (para debug)
                with st.expander("Ver Prompt enviado para a IA"):
                    st.code(final_prompt)

if __name__ == "__main__":
    main()
