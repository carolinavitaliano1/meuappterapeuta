import openai
import os

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
# ESTADO GLOBAL (CADASTRO)
# ===============================
if "patients" not in st.session_state:
    st.session_state.patients = {}

# ===============================
# FUNÇÕES AUXILIARES
# ===============================

def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")


def generate_session_prompt(patient_info, goals, approach, knowledge_base, num_sessions):
    prompt = f"""
Atue como uma EQUIPE TERAPÊUTICA MULTIDISCIPLINAR EXPERIENTE.

══════════════════════════════
📌 DADOS DO PACIENTE
══════════════════════════════
Nome: {patient_info.get('name')}
Idade: {patient_info.get('age')}
Contexto clínico / queixa principal:
{patient_info.get('context')}

══════════════════════════════
🎯 OBJETIVOS TERAPÊUTICOS
══════════════════════════════
{goals}

══════════════════════════════
🧠 ABORDAGENS TERAPÊUTICAS
══════════════════════════════
{approach}

══════════════════════════════
📅 PLANEJAMENTO
══════════════════════════════
Crie {num_sessions} sessões terapêuticas,
cada uma com atividades diferentes e progressivas.

══════════════════════════════
📚 BASE DE CONHECIMENTO
══════════════════════════════
{knowledge_base[:15000]}

══════════════════════════════
🛠️ TAREFA
══════════════════════════════
Para CADA sessão, descreva:
- Acolhimento
- Desenvolvimento (atividades detalhadas)
- Fecho
- Objetivos da sessão
- Indicadores de evolução

Use linguagem técnica, prática e clínica.
Evite respostas genéricas.
"""
    return prompt

# ===============================
# INTERFACE PRINCIPAL
# ===============================

def main():
    st.title("🧠 NeuroTech Evoluir")
    st.subheader("Planejamento Terapêutico Multidisciplinar")

    col1, col2 = st.columns([1, 1])

    # ===============================
    # COLUNA 1 – CADASTRO / SELEÇÃO
    # ===============================
    with col1:
        st.info("👤 Cadastro de Paciente")

        with st.expander("➕ Cadastrar novo paciente"):
            name = st.text_input("Nome do paciente")
            age = st.number_input("Idade", min_value=0, max_value=120, step=1)
            context = st.text_area("Contexto clínico / queixa principal")

            if st.button("Salvar paciente"):
                if name:
                    st.session_state.patients[name] = {
                        "name": name,
                        "age": age,
                        "context": context
                    }
                    st.success("Paciente cadastrado com sucesso!")

        if st.session_state.patients:
            selected_patient = st.selectbox(
                "Selecione o paciente",
                list(st.session_state.patients.keys())
            )
            patient_data = st.session_state.patients[selected_patient]
        else:
            patient_data = None
            st.warning("Nenhum paciente cadastrado.")

        st.markdown("---")

        session_goals = st.text_area(
            "Objetivos terapêuticos",
            placeholder="Ex: estimular comunicação funcional, ampliar atenção..."
        )

        num_sessions = st.number_input(
            "Quantidade de sessões / atividades",
            min_value=1,
            max_value=52,
            step=1,
            help="Ex: 4 sessões = 1 mês (1x por semana)"
        )

        approach = st.multiselect(
            "Abordagens terapêuticas",
            [
                "Psicologia",
                "Psicopedagogia",
                "Psicomotricidade",
                "Fonoaudiologia",
                "Musicoterapia",
                "Terapia Ocupacional",
                "ABA",
                "CAA (Comunicação Aumentativa e Alternativa)"
            ]
        )

    # ===============================
    # COLUNA 2 – BASE DE CONHECIMENTO
    # ===============================
    with col2:
        st.warning("📚 Base de Conhecimento")

        uploaded_files = st.file_uploader(
            "Anexe materiais (PDF ou TXT)",
            type=["pdf", "txt"],
            accept_multiple_files=True
        )

        knowledge_text = ""

        if uploaded_files:
            for file in uploaded_files:
                knowledge_text += f"\n--- Fonte: {file.name} ---\n"
                if file.name.endswith(".pdf"):
                    knowledge_text += extract_text_from_pdf(file)
                else:
                    knowledge_text += extract_text_from_txt(file)

            st.success(f"{len(uploaded_files)} arquivo(s) carregado(s).")

    # ===============================
    # GERAR PLANO
    # ===============================
    st.markdown("---")

    if st.button("✨ Gerar Plano Terapêutico"):
        if not patient_data or not session_goals:
            st.error("Selecione um paciente e informe os objetivos.")
        else:
            final_prompt = generate_session_prompt(
                patient_data,
                session_goals,
                ", ".join(approach),
                knowledge_text,
                num_sessions
            )

            st.markdown("### 📝 Plano Gerado (Simulação)")
            with st.expander("Ver prompt enviado para a IA"):
                st.code(final_prompt)


if __name__ == "__main__":
    main()

