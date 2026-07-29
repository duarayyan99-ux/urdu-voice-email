import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai
import streamlit as st

st.set_page_config(page_title="Voice AI Email Assistant", page_icon="🎙️")
st.title("🎙️ Voice-Activated AI Email Sender")
st.write(
    "Urdu mein voice note upload karein aur direct professional email bhejein!"
)

# Credentials Setup
API_KEY = "AQ.Ab8RN6JuTyte20IgTBs9NUJ8fQSylP8OABZF276FGRSd8bVjWA"
SENDER_EMAIL = "duarayyan99@gmail.com"
SENDER_PASSWORD = "dua2222@"

client = genai.Client(api_key=API_KEY)

audio_file_input = st.file_uploader(
    "🎤 Step 1: Urdu Voice Record/Upload Karein",
    type=["mp3", "wav", "m4a", "ogg"],
)
receiver_email = st.text_input(
    "📧 Step 2: Recipient Email Address", placeholder="e.g. receiver@gmail.com"
)

if st.button("🚀 Send Email"):
  if not audio_file_input:
    st.error("Pehle audio file upload karein!")
  elif not receiver_email or "@" not in receiver_email:
    st.error("Sahi email address likhein!")
  else:
    with st.spinner("AI processing & sending email..."):
      try:
        with open("temp_audio.mp3", "wb") as f:
          f.write(audio_file_input.getbuffer())

        audio_file = client.files.upload(file="temp_audio.mp3")

        prompt = """
                Aap ek expert AI Email Assistant hain. Audio mein user Urdu mein bol raha hai.
                1. Formal professional English Email (Subject & Body) banayein.
                2. PURE URDU SCRIPT (اردو) mein summary likhein. No Roman Urdu.
                Output format strictly JSON:
                {
                    "subject": "Subject",
                    "body": "Body",
                    "urdu_summary": "اردو خلاصہ"
                }
                """

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=[audio_file, prompt]
        )

        raw_text = (
            response.text.strip()
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )
        data = json.loads(raw_text)

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = data.get("subject", "Voice Email")
        msg.attach(MIMEText(data.get("body", ""), "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()

        st.success("✅ Email Kamyabi Se Bhej Di Gayi!")
        st.subheader("📄 Email Content:")
        st.write(data.get("body", ""))
        st.subheader("🇵🇰 Urdu Verification:")
        st.write(data.get("urdu_summary", ""))

      except Exception as e:
        st.error(f"Error: {str(e)}")
