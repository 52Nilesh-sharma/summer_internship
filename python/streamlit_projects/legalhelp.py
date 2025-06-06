import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Legal Help App", layout="wide")

# ---------- SIDEBAR MENU ----------
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Home", "Legal Advice", "Contact Lawyers", "Legal FAQs", "Traffic Help"],
        icons=["house", "chat", "person-lines-fill", "book", "traffic-cone"],
        default_index=0
    )

# ---------- LANGUAGE TOGGLE ----------
language = st.radio("Choose Language / भाषा चुनें", ["English", "हिन्दी"], horizontal=True)

# ---------- HOME ----------
if selected == "Home":
    st.title("🛡️ Legal Help App")
    st.markdown("Welcome! Get trusted legal help, connect with lawyers, and understand your rights.")
    if language == "हिन्दी":
        st.markdown("कानूनी सहायता, वकीलों से संपर्क और अपने अधिकारों को समझें।")

# ---------- LEGAL ADVICE ----------
elif selected == "Legal Advice":
    st.subheader("💬 Get Legal Advice" if language == "English" else "💬 कानूनी सलाह प्राप्त करें")
    user_question = st.text_input("Type your legal question..." if language == "English" else "अपना कानूनी प्रश्न लिखें...")

    if user_question:
        if "license" in user_question.lower():
            st.success("Driving without license can lead to a fine of ₹5000." if language == "English"
                       else "बिना लाइसेंस गाड़ी चलाने पर ₹5000 जुर्माना हो सकता है।")
        elif "helmet" in user_question.lower():
            st.success("Not wearing helmet: ₹1000 fine." if language == "English"
                       else "हेलमेट न पहनने पर ₹1000 जुर्माना।")
        else:
            st.info("Thanks for your query! A legal expert will respond soon." if language == "English"
                    else "धन्यवाद! एक कानूनी विशेषज्ञ जल्द ही उत्तर देगा।")

# ---------- CONTACT LAWYERS ----------
elif selected == "Contact Lawyers":
    st.subheader("⚖️ Contact a Lawyer" if language == "English" else "⚖️ वकीलों से संपर्क करें")

    lawyers = [
        {"name": "Adv. Rajeev Singh", "city": "Delhi", "phone": "9876543210", "specialization": "Traffic / Civil"},
        {"name": "Adv. Neha Sharma", "city": "Mumbai", "phone": "9823456780", "specialization": "Criminal / Family"},
        {"name": "Adv. Arjun Patel", "city": "Ahmedabad", "phone": "9012345678", "specialization": "Consumer Rights"},
    ]

    for lawyer in lawyers:
        st.markdown(f"**{lawyer['name']}** ({lawyer['specialization']})")
        st.markdown(f"📍 {lawyer['city']} | 📞 {lawyer['phone']}")
        st.markdown("---")

# ---------- LEGAL FAQ ----------
elif selected == "Legal FAQs":
    st.subheader("📚 Frequently Asked Questions" if language == "English" else "📚 अक्सर पूछे जाने वाले प्रश्न")

    faq_data = {
        "Traffic Law": {
            "English": "What is the fine for driving without a license?\nFine: ₹5000 under Motor Vehicles Act.",
            "हिन्दी": "बिना लाइसेंस गाड़ी चलाने पर जुर्माना?\nजुर्माना: ₹5000 मोटर वाहन अधिनियम के तहत।"
        },
        "Consumer Rights": {
            "English": "What to do if a product is defective?\nYou can file a complaint in Consumer Court online.",
            "हिन्दी": "अगर उत्पाद ख़राब निकले तो क्या करें?\nआप ऑनलाइन उपभोक्ता अदालत में शिकायत दर्ज कर सकते हैं।"
        },
        "Police Harassment": {
            "English": "What to do if police harasses you?\nStay calm. Ask for ID. File complaint at NHRC or online portal.",
            "हिन्दी": "अगर पुलिस परेशान करे तो क्या करें?\nशांत रहें। आईडी मांगें। NHRC या पोर्टल पर शिकायत करें।"
        }
    }

    category = st.selectbox("Choose FAQ Category" if language == "English" else "FAQ श्रेणी चुनें", list(faq_data.keys()))
    if language == "English":
        st.markdown(f"**Q:** {category}\n\n**A:** {faq_data[category]['English']}")
    else:
        st.markdown(f"**प्रश्न:** {category}\n\n**उत्तर:** {faq_data[category]['हिन्दी']}")

# ---------- TRAFFIC LAW HELP ----------
elif selected == "Traffic Help":
    st.subheader("🚦 Traffic Law Assistance" if language == "English" else "🚦 ट्रैफिक कानून सहायता")

    traffic_violations = [
        {"Violation": "Without Helmet", "Fine": "₹1000"},
        {"Violation": "Drunk Driving", "Fine": "₹10000 + Jail (up to 6 months)"},
        {"Violation": "Red Light Jump", "Fine": "₹1000"},
        {"Violation": "No License", "Fine": "₹5000"},
        {"Violation": "Over Speeding", "Fine": "₹1000-₹2000"},
    ]

    df = pd.DataFrame(traffic_violations)
    st.table(df)

    st.markdown("### 🚨 Caught Without Violation?" if language == "English" else "### 🚨 अगर बेवजह पकड़े गए हों तो क्या करें?")

    if language == "English":
        st.markdown("""
        - Stay calm. Don't argue aggressively.
        - Ask for reason and officer's ID.
        - Record video/audio if you feel threatened.
        - File a complaint at [grievance portal](https://pgportal.gov.in/)
        """)
    else:
        st.markdown("""
        - शांत रहें। ज़्यादा बहस न करें।
        - कारण और पुलिस अधिकारी का आईडी माँगें।
        - अगर धमकी लगे तो वीडियो/ऑडियो रिकॉर्ड करें।
        - शिकायत दर्ज करें: [शिकायत पोर्टल](https://pgportal.gov.in/)
        """)
