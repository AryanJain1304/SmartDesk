import streamlit as st
import time
import faiss
from sentence_transformers import SentenceTransformer

KB_ENTRIES = [
    {"title": "Password Reset", "content": "To reset your password, click 'Forgot Password' on login page."},
    {"title": "Billing Queries", "content": "For billing issues, check Account -> Billing for invoices."},
    {"title": "Upgrade Plan", "content": "To upgrade, go to Account -> Plans and select the desired plan."},
    {"title": "Invoice Missing", "content": "If an invoice is missing, contact support with invoice number and date."}
]

EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

kb_texts = [entry["content"] for entry in KB_ENTRIES]
kb_embeddings = EMBED_MODEL.encode(kb_texts, convert_to_numpy=True)

embedding_dim = kb_embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(kb_embeddings)

account_settings = {
    "user123": {"plan": "Free", "email": "user123@example.com"}
}

def status_config_api(user_id, action=None, value=None):
    if action == "read":
        return account_settings.get(user_id, {})
    elif action == "write" and value:
        account_settings[user_id] = value
        return account_settings[user_id]
    return None

def email_reply_draft_api(ticket, reply):
    return f"Draft Reply:\nTo: {ticket['user_id']}\nSubject: {ticket['title']}\n\n{reply}"

def escalation_logger(ticket, reason):
    return f"Escalated Ticket: {ticket['title']}\nUser: {ticket['user_id']}\nReason: {reason}"

def kb_retriever_semantic(query, top_k=1):
    query_emb = EMBED_MODEL.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, top_k)
    if distances[0][0] < 1.0:
        return KB_ENTRIES[indices[0][0]]["content"]
    return None

def agent_loop(ticket):
    logs = []
    user_id = ticket.get("user_id", "user123")
    title = ticket.get("title", "")
    description = ticket.get("description", "")
    combined_text = f"{title} {description}"

    kb_result = kb_retriever_semantic(combined_text)
    if kb_result:
        logs.append(f"KB Retrieved: {kb_result}")
        reply = kb_result
        return {"status": "solved", "reply": email_reply_draft_api(ticket, reply), "logs": logs}

    if "upgrade" in combined_text.lower() or "change plan" in combined_text.lower():
        current_settings = status_config_api(user_id, action="read")
        logs.append(f"Current Settings: {current_settings}")
        new_plan = "Pro Monthly"
        status_config_api(user_id, action="write", value={"plan": new_plan, "email": current_settings["email"]})
        logs.append(f"Plan upgraded to {new_plan}")
        reply = f"Your plan has been upgraded to {new_plan}."
        return {"status": "solved", "reply": email_reply_draft_api(ticket, reply), "logs": logs}

    if "invoice" in combined_text.lower() or "billing" in combined_text.lower():
        reason = "Billing query not found in KB"
        logs.append(f"Escalation reason: {reason}")
        return {"status": "escalated", "escalation_note": escalation_logger(ticket, reason), "logs": logs}

    reason = "Unknown ticket type"
    logs.append(f"Escalation reason: {reason}")
    return {"status": "escalated", "escalation_note": escalation_logger(ticket, reason), "logs": logs}

st.title("SmartDesk")

st.markdown("Enter a support ticket below:")

with st.form(key='ticket_form'):
    user_id = st.text_input("User ID", "user123")
    title = st.text_input("Ticket Title")
    description = st.text_area("Ticket Description")
    submit_button = st.form_submit_button(label='Submit Ticket')

if submit_button:
    ticket = {"user_id": user_id, "title": title, "description": description}
    with st.spinner("Processing ticket..."):
        time.sleep(1)
        result = agent_loop(ticket)

    st.subheader("Tool Call Logs")
    for log in result.get("logs", []):
        st.write(f"- {log}")

    if result["status"] == "solved":
        st.success("Ticket Solved!")
        st.subheader("Proposed Customer Reply")
        st.code(result["reply"])
    else:
        st.error("Ticket Escalated!")
        st.subheader("Escalation Note")
        st.code(result["escalation_note"])