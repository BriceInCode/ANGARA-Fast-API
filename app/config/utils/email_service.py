import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.settings import settings  

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 465  # Port SSL
        self.sender_email = settings.GMAIL_EMAIL      # Exemple : "votre_email@gmail.com"
        self.password = settings.GMAIL_PASSWORD         # Mot de passe ou App Password
        self.company_name = settings.GMAIL_USERNAME

    def send_email(self, receiver_email: str, subject: str, body: str) -> bool:
        
        message = MIMEMultipart()
        message["From"] = self.company_name
        message["To"] = receiver_email
        message["Subject"] = subject

        # Ajout du corps de l'email
        message.attach(MIMEText(body, "plain"))
        text = message.as_string()

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, receiver_email, text)
            return True
        except Exception as e:
            print("Erreur lors de l'envoi de l'email :", e)
            return False
