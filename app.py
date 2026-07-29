import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
import streamlit as st

st.set_page_config(page_title="Voice AI Email Assistant", page_icon="🎙️")
st.title("🎙️ Voice-Activated AI Email Sender")
st.write("Urdu mein voice note upload karein aur direct professional email bhejein!")

# Credentials Setup (Streamlit Secrets se Direct Retrieval)
API_KEY = "AQ.Ab8RN6JuTyte20IgTBs9NUJ8" "fQSy1P80ABZF276FGRSd8bVjWA"
SENDER_EMAIL = "duarayyan99@gmail.com"
SENDER_PASSWORD = "dua2222@"

client = genai.Client(api_key=API_KEY)

audio_file_input = st.file_uploader(
    "🎙️ Step 1: Urdu Voice Record/Upload Karein",
    type=["mp3", "wav", "m4a", "ogg"]
)

receiver_email = st.text_input(
    "📧 Step 2: Recipient Email Address", 
    placeholder="e.g. receiver@gmail.com"
)

if st.button("🚀 Send Email"):
    if audio_file_input and receiver_email:
        with st.spinner("AI aapke voice note ko samjh kar email tayar kar raha hai..."):
            try:
                # Gemini Audio File Upload & Processing
                uploaded_file = client.files.upload(file=audio_file_input)
                
                prompt = """
                Listen to this Urdu audio carefully. 
                Extract the context and draft a professional, polite, and well-structured email in English.
                Return ONLY a JSON response with 'subject' and 'body' keys.
                """
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[uploaded_file, prompt]
                )
                
                # JSON Parsing
                email_data = json.loads(response.text.strip('```json').strip('```'))
                subject = email_data.get('subject', 'Voice Email')
                body = email_data.get('body', '')
                
                # SMTP Email Sending
                msg = MIMEMultipart()
                msg['From'] = SENDER_EMAIL
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
                server.quit()
                
                st.success("✅ Email successfully bhej di gayi hai!")
                st.subheader("Drafted Email Preview:")
                st.write(f"**Subject:** {subject}")
                st.write(f"**Body:**\n{body}")
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please voice note upload karein aur receiver email daalein!")
