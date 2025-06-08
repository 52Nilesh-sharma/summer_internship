import gradio as gr
import google.generativeai as genai
import fitz  # PyMuPDF for PDF text extraction

# 🔐 Step 1: Configure Gemini API
genai.configure(api_key="AIzaSyDdMZbIwXtOAi0A3hCl6T4eJHpB_6qrw7Q")  # Replace with your actual key
model = genai.GenerativeModel("gemini-1.5-flash")

# Create a persistent chat object with memory
chat = model.start_chat(history=[])

# 📄 Step 2: PDF extraction function
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 🌟 Step 3: Main chat + tagging + risk logic
def legal_chat(file, user_message, history=[]):
    # Check if PDF is uploaded
    if file is None:
        return history + [[user_message, "Please upload a legal document."]], "", ""

    # Extract and store text from PDF if this is the first message
    if not hasattr(legal_chat, "document_text"):
        legal_chat.document_text = extract_text_from_pdf(file)

    doc_text = legal_chat.document_text

    # Use the Gemini chat object for multi-turn interaction
    prompt = f"""
You are an AI legal assistant. Based on the following legal document, answer the user's question in plain language.

Document:
{doc_text}

User question:
{user_message}
"""

    # AI responds to the user's current message
    try:
        ai_response = chat.send_message(prompt).text
    except Exception as e:
        ai_response = f"Error from Gemini API: {str(e)}"

    # Clause tagging and risk detection only on first interaction
    clause_tags = ""
    risk_flags = ""
    if len(history) == 0:
        clause_prompt = f"""
Identify and list important clauses in the document, grouped by category (e.g., Payment, Termination, Confidentiality):

Document:
{doc_text}
"""
        risk_prompt = f"""
Analyze the document and highlight any unusual, risky, or unfair terms. Provide plain-English explanations.

Document:
{doc_text}
"""
        try:
            clause_tags = model.generate_content(clause_prompt).text
            risk_flags = model.generate_content(risk_prompt).text
        except Exception as e:
            clause_tags = "Error generating clause tags."
            risk_flags = "Error analyzing risks."

    # Append to chat history
    history.append([user_message, ai_response])
    return history, clause_tags, risk_flags

# 🎨 Gradio UI with chat-style layout
with gr.Blocks(title="📚 AI Legal Chat Assistant") as demo:
    gr.Markdown("## 🤖 AI Legal Assistant")
    gr.Markdown("Upload a legal PDF and chat with the AI. It will remember your context.")

    with gr.Row():
        file_input = gr.File(label="📄 Upload PDF Document", file_types=[".pdf"])

    chatbot = gr.Chatbot(label="💬 Legal Assistant", height=400)
    msg = gr.Textbox(label="Type your question here and press Enter")
    clause_box = gr.Textbox(label="📑 Tagged Clauses", lines=8, interactive=False)
    risk_box = gr.Textbox(label="⚠️ Risky Clauses Detected", lines=6, interactive=False)

    clear_btn = gr.Button("🔁 Clear Conversation")

    def reset():
        chat.history.clear()
        if hasattr(legal_chat, "document_text"):
            del legal_chat.document_text
        return [], "", ""

    msg.submit(legal_chat, inputs=[file_input, msg, chatbot], outputs=[chatbot, clause_box, risk_box])
    clear_btn.click(fn=reset, outputs=[chatbot, clause_box, risk_box])

# 🚀 Launch the app
if __name__ == "__main__":
    demo.launch()
