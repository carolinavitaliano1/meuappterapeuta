import streamlit as st
from PyPDF2 import PdfReader

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="NeuroTech Evoluir – Terapeuta AI",
    layout="wide"
)

# ===============================
# FUNÇÕES AUXILIARES
# ===============================

def extract_text_from_pdf(file):
    """Extrai texto de um ficheiro PDF (com proteção contra páginas vazias)."""
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_from_txt(file):
    """Extrai texto de um ficheiro TXT."""
    return file.getvalue().decode("utf-8")


def generate_session_prompt(patient_info, goals, approach, knowledge_base):
    """Cria um prompt clínico avançado para geração da sessão terapêutica."""

    prompt = f"""
Atue como uma EQUIPE TERAPÊUTICA MULTIDISCIPLINAR EXPERIENTE,
integrando práticas baseadas em evidências científicas.

══════════════════════════════
📌 DADOS DO PACIENTE
══════════════════════════════
Nome: {patient_info.get('name', 'Não informado')}
Idade: {patient_info.get('age', 'Não informada')}
Contexto clínico / queixa principal:
{patient_info.get('context', 'Não informado')}

══════════════════════════════
🎯 OBJETIVOS DA SESSÃO
══════════════════════════════
{goals}

══════════════════════════════
🧠 ABORDAGENS TERAPÊUTICAS
══════════════════════════════
Utilize de forma integrada as seguintes abordagens:
{approach}

══════════════════════════════
📚 BASE DE CONHECIMENTO DO TERAPEUTA
══════════════════════════════
Utilize os conteúdos abaixo como referência teórica e prática.
Priorize estratégias coerentes com os materiais apresentados.

{knowledge_base[:15000]}

══════════════════════════════
🛠️ TAREFA
══════════════════════════════
Crie um PLANO DE SESSÃO TERAPÊUTICA estruturado e clínico contendo:

1. Acolhimento
   - Estratégia de vínculo e regulação
   - Adequação ao perfil sensorial, comunicativo e cognitivo

2. Desenvolvimento
   - Atividades terapêuticas detalhadas
   - Objetivos terapêuticos claros
   - Justificativa clínica ou teórica de cada atividade
   - Adaptações possíveis (idade, suporte, comunicação, sensorial)

3. Fecho
   - Estratégia de encerramento
   - Generalização ou orientação para casa/família

4. Indicadores de Evolução
   - O que observar
   - Critérios de progresso

Evite respostas genéricas.
Utilize linguagem técnica, clara e aplicável à prática clínica.
"""
    return prompt


# ===============================
# INTERFACE PRINCIPAL
# ===============================

def main():
    st.title("🧠 NeuroTech Evoluir")
    st.subheader("Assistente Inteligente para Planejamento Terapêutico Multidisciplinar")

    st.markdown("""
Esta ferramenta auxilia terapeutas a planejar sessões clínicas personalizadas,
utilizando **inteligência artificial + base teórica própria do profissional**.
""")

    col1, col2 = st.columns([1, 1])

    # ===============================
    # COLUNA 1 – DADOS DO PACIENTE
    # ===============================
    with col1:
        st.info("👤 **1. Dados do Paciente**")

        name = st.text_input("Nome do paciente")
        age = st.number_input("Idade", min_value=0, max_value=120, step=1)

        context = st.text_area(
            "Contexto clínico / queixa principal",
            placeholder="Ex: dificuldade de alfabetização, atraso de linguagem, dificuldades atencionais..."
        )

        session_goals = st.text_area(
            "Objetivos da sessão",
            placeholder="Ex: estimular comunicação funcional, ampliar atenção compartilhada..."
        )

        approach = st.multiselect(
            "Abordagens terapêuticas envolvidas",
            [
                "Psicologia",
                "Psicopedagogia",
                "Psicomotricidade",
                "Fonoaudiologia",
                "Musicoterapia",
                "Terapia Ocupacional",
                "ABA",
                "CAA (Comunicação Aumentativa e Alternativa)",
                "Neuroeducação",
                "Intervenção Multidisciplinar Integrada"
            ]
        )

    # ===============================
    # COLUNA 2 – BASE DE CONHECIMENTO
    # ===============================
    with col2:
        st.warning("📚 **2. Base de Conhecimento do Terapeuta**")

        uploaded_files = st.file_uploader(
            "Anexe livros, artigos ou materiais (PDF ou TXT)",
            type=["pdf", "txt"],
            accept_multiple_files=True
        )

        knowledge_text = ""

        if uploaded_files:
            with st.spinner("Processando materiais..."):
                for file in uploaded_files:
                    try:
                        knowledge_text += f"\n\n--- Fonte: {file.name} ---\n"
                        if file.name.endswith(".pdf"):
                            knowledge_text += extract_text_from_pdf(file)
                        elif file.name.endswith(".txt"):
                            knowledge_text += extract_text_from_txt(file)
                    except Exception as e:
                        st.error(f"Erro ao ler {file.name}: {e}")

            st.success(f"Base carregada com sucesso! ({len(knowledge_text)} caracteres)")

            with st.expander("Visualizar trecho do conteúdo extraído"):
                st.write(knowledge_text[:1200] + "...")

    # ===============================
    # BOTÃO DE GERAÇÃO
    # ===============================
    st.markdown("---")

    if st.button("✨ Gerar Plano Terapêutico com IA", type="primary"):
        if not session_goals:
            st.error("Informe pelo menos os objetivos da sessão.")
        else:
            patient_data = {
                "name": name,
                "age": age,
                "context": context
            }

            final_prompt = generate_session_prompt(
                patient_data,
                session_goals,
                ", ".join(approach) if approach else "Abordagem multidisciplinar integrada",
                knowledge_text
            )

            with st.spinner("A IA está analisando os dados e construindo o plano terapêutico..."):
                st.markdown("### 📝 Plano Terapêutico Gerado (Simulação)")
                st.info("Integre sua API de IA para obter respostas reais.")

                with st.expander("🔍 Ver prompt enviado para a IA"):
                    st.code(final_prompt)


if __name__ == "__main__":
    main()

