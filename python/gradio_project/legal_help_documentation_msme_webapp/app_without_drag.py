import gradio as gr
import google.generativeai as genai

# 🔐 Configure Gemini API
genai.configure(api_key="AIzaSyDdMZbIwXtOAi0A3hCl6T4eJHpB_6qrw7Q")  # Replace with your Gemini API Key

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

# 🔍 Core logic for analyzing and chatting
def legal_chat(document_text, user_message, history=[]):
    if not document_text.strip():
        return history + [[user_message, "❗ Please paste a legal document."]], "", ""

    # Save the document for memory (first time only)
    if not hasattr(legal_chat, "document_text"):
        legal_chat.document_text = document_text

    # Main question-response prompt
    prompt = f"""
You're an AI legal assistant. Analyze the following document and answer the user's question clearly in simple language.

Document:
{legal_chat.document_text}

Question:
{user_message}
"""

    try:
        response = chat.send_message(prompt).text
    except Exception as e:
        response = f"Error: {str(e)}"

    # Clause tagging and risk detection only on first run
    clause_tags = ""
    risk_flags = ""
    if len(history) == 0:
        clause_prompt = f"""
List and categorize the main clauses in the following legal agreement. Group them by topic such as Termination, Payment, Liability, etc.

Document:
{legal_chat.document_text}
"""
        risk_prompt = f"""
Identify any risky or unfair clauses in the following legal document. Explain why they might be problematic in plain English.

Document:
{legal_chat.document_text}
"""
        try:
            clause_tags = model.generate_content(clause_prompt).text
            risk_flags = model.generate_content(risk_prompt).text
        except Exception as e:
            clause_tags = "Clause tagging failed."
            risk_flags = "Risk detection failed."

    history.append([user_message, response])
    return history, clause_tags, risk_flags

# 🔄 Reset chat memory
def reset():
    chat.history.clear()
    if hasattr(legal_chat, "document_text"):
        del legal_chat.document_text
    return [], "", ""

# 🖼️ Gradio UI
with gr.Blocks(title="AI Legal Assistant - Paste Mode") as demo:
    gr.Markdown("## 🤖 AI Legal Assistant (No Upload Required)")
    gr.Markdown("Paste your legal contract below and ask legal questions. The AI will explain, tag clauses, and flag risks.")

    document_input = gr.Textbox(lines=15, label="📄 Paste Legal Document Here")
    chatbot = gr.Chatbot(label="💬 Chat with Legal Assistant", height=400)
    user_msg = gr.Textbox(label="Ask a question about the document", placeholder="e.g., Can I terminate this early?")
    clause_box = gr.Textbox(label="📑 Tagged Clauses", lines=6, interactive=False)
    risk_box = gr.Textbox(label="⚠️ Risky Clauses", lines=6, interactive=False)

    submit = gr.Button("Analyze")
    clear = gr.Button("Reset")

    submit.click(legal_chat, inputs=[document_input, user_msg, chatbot], outputs=[chatbot, clause_box, risk_box])
    clear.click(reset, outputs=[chatbot, clause_box, risk_box])

# 🚀 Launch
if __name__ == "__main__":
    demo.launch()
