
import streamlit as st
from groq import Groq
import os

# =========================
# CONFIGURATION DE LA PAGE
# =========================
st.set_page_config(
    page_title="Analyseur de Texte IA",
    page_icon="🧠",
    layout="wide"
)

# =========================
# TITRE ET INTRODUCTION
# =========================
st.title("🧠 Analyseur de Texte IA")
st.markdown("### Analysez n'importe quel texte en un clic avec l'IA")
st.markdown("---")

# =========================
# SIDEBAR (barre latérale)
# =========================
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Saisie de la clé API
    api_key = st.text_input(
        "🔑 Clé API Groq",
        type="password",
        help="Ta clé API Groq (récupérable sur console.groq.com)"
    )
    
    st.markdown("---")
    st.markdown("### 📊 À propos")
    st.markdown("""
    Cet outil utilise l'IA pour analyser automatiquement :
    - 📝 Résumé
    - 🔑 Mots-clés
    - 😊 Sentiment
    - 🎯 Thème principal
    """)
    
    st.markdown("---")
    st.markdown("👤 **Par Benjamin Gravé**")
    st.markdown("Data Analyst Freelance")

# =========================
# CONTENU PRINCIPAL
# =========================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✍️ Texte à analyser")
    
    texte_input = st.text_area(
        "Colle ton texte ici",
        height=300,
        placeholder="Exemple : Un avis client, un article de presse, un email..."
    )
    
    analyser_btn = st.button("🚀 Analyser le texte", type="primary", use_container_width=True)

with col2:
    st.subheader("💡 Cas d'usage")
    st.info("""
    **Parfait pour :**
    - Analyse d'avis clients
    - Traitement d'emails
    - Classification de documents
    - Veille médias
    - Synthèse de rapports
    """)

# =========================
# ANALYSE DU TEXTE
# =========================
if analyser_btn:
    if not api_key:
        st.error("⚠️ Merci de renseigner ta clé API Groq dans la barre latérale")
    elif not texte_input.strip():
        st.error("⚠️ Merci de coller un texte à analyser")
    else:
        with st.spinner("🔍 Analyse en cours..."):
            try:
                # Connexion à Groq
                client = Groq(api_key=api_key)
                
                # Prompt d'analyse
                prompt = f"""Tu es un expert en analyse de texte. Analyse le texte suivant et fournis :

1. RÉSUMÉ : Un résumé en 2-3 phrases maximum
2. MOTS-CLÉS : 5 mots-clés importants (séparés par des virgules)
3. SENTIMENT : Positif, Négatif ou Neutre (avec un score de 0 à 10)
4. THÈME PRINCIPAL : Le sujet principal en quelques mots

Texte à analyser :
{texte_input}

Réponds de manière structurée avec les 4 sections clairement séparées."""
                
                # Appel à Groq
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Tu es un expert en analyse de texte, précis et structuré."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                
                resultat = response.choices[0].message.content
                
                # Affichage des résultats
                st.markdown("---")
                st.subheader("📊 Résultats de l'analyse")
                
                st.success("✅ Analyse terminée !")
                st.markdown(resultat)
                
                # Statistiques du texte
                st.markdown("---")
                st.subheader("📈 Statistiques du texte")
                
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Caractères", len(texte_input))
                col_b.metric("Mots", len(texte_input.split()))
                col_c.metric("Phrases", texte_input.count('.') + texte_input.count('!') + texte_input.count('?'))
                
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>🤖 Propulsé par Llama 3.3 via Groq | Développé par Benjamin Gravé</p>",
    unsafe_allow_html=True
)
