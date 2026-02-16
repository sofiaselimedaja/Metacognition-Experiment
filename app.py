import streamlit as st
from openai import OpenAI

# Recupera la chiave dai Secrets di Streamlit
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if 'page' not in st.session_state:
    st.session_state.page = 1
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'chat_1' not in st.session_state:
    st.session_state.chat_1 = []
if 'chat_2' not in st.session_state:
    st.session_state.chat_2 = []

def next_page():
    st.session_state.page += 1
    st.rerun()

# --- PAGINA 1: CONSENSO ---
if st.session_state.page == 1:
    st.title("Consenso Informato")
    st.write("Benvenuto in questo studio sulla Generative AI e l'apprendimento.")
    st.session_state.responses['age'] = st.text_input("Quanti anni hai?")
    if st.button("Accetto e Inizio"):
        if st.session_state.responses['age']: next_page()
        else: st.warning("Inserisci l'età.")

# --- PAGINA 2: GROWTH MINDSET SURVEY (6 ITEMS) ---
elif st.session_state.page == 2:
    st.title("Pre-Task Survey")
    st.write("Indica il tuo grado di accordo (1=Strongly Disagree, 6=Strongly Agree):")
    items = [
        "I believe that I can significantly change my basic level of intelligence through learning and effort.",
        "Your intelligence is something about you that you can't change very much.",
        "No matter who you are, you can always substantially improve your mental abilities.",
        "My ability to effectively interact with AI is a skill that can be developed, not just a natural talent.",
        "If I struggle to get a good result from AI, it means I need to refine my strategies and keep trying.",
        "Some people have a natural 'knack' for AI, and if you don't have it, you will never truly master it."
    ]
    for i, item in enumerate(items):
        st.session_state.responses[f"gm_{i}"] = st.select_slider(item, options=[1,2,3,4,5,6], key=f"gm_{i}")
    if st.button("Prosegui"): next_page()

# --- PAGINA 3: TASK 1 (PULSARS + SOCRATIC) ---
elif st.session_state.page == 3:
    st.title("Task 1: Neutron Stars & Pulsars")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""Deep in space, there are objects so dense that a single teaspoon of their material would weigh a billion tons on Earth. These are neutron stars, the collapsed remains of giant stars that exploded in a supernova. Among them, the most fascinating are the 'Pulsars.' A pulsar is a highly magnetized, rapidly rotating neutron star that emits beams of electromagnetic radiation out of its magnetic poles. This radiation can only be observed when a beam of emission is pointing toward Earth, much like the way a lighthouse can only be seen when its light is pointed at an observer.""")
        st.info("Ask the AI to help you reflect on why your choice is correct.")
        st.radio("Q1. Why are pulsars compared to lighthouses?", ["A", "B", "C", "D"], key="q1")
    with col2:
        st.subheader("Socratic Assistant")
        for m in st.session_state.chat_1: st.chat_message(m["role"]).write(m["content"])
        if p := st.chat_input("Ask the tutor...", key="chat1"):
            st.session_state.chat_1.append({"role": "user", "content": p})
            res = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a Socratic Tutor. Never give direct answers. Ask reflective questions."}]+st.session_state.chat_1)
            msg = res.choices[0].message.content
            st.session_state.chat_1.append({"role": "assistant", "content": msg})
            st.rerun()
    if st.button("Next"): next_page()

# --- PAGINA 4: CONCLUSIONE TEMPORANEA (PER IL TUO TEST) ---
elif st.session_state.page == 4:
    st.title("Fine Test")
    st.write("I tuoi dati salvati finora:")
    st.json(st.session_state.responses)
    st.write("Log Chat:", st.session_state.chat_1)
