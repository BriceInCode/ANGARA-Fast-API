import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.configs.settings import settings

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class EmailService:
    """Service professionnel d'envoi d'email via SMTP avec gestion avancée des erreurs et support HTML."""

    SMTP_SERVER = "smtp.gmail.com"
    PORT = 465  # Port SSL
    SENDER_EMAIL = settings.GMAIL_EMAIL
    PASSWORD = settings.GMAIL_PASSWORD
    COMPANY_NAME = settings.GMAIL_USERNAME

    @classmethod
    def send_email(cls, receiver_email: str, subject: str, body: str, html: bool = False) -> bool:
        """
        Envoie un email sécurisé à un destinataire.
        :param receiver_email: Adresse email du destinataire.
        :param subject: Sujet de l'email.
        :param body: Contenu du message (HTML ou texte brut).
        :param html: True si le corps du message est en HTML.
        :return: True si l'email est envoyé avec succès, False sinon.
        """

        # Vérifier que les variables SMTP sont bien définies
        if not all([cls.SENDER_EMAIL, cls.PASSWORD, receiver_email]):
            logging.error("❌ Paramètres SMTP invalides ou email destinataire manquant.")
            return False

        # Création du message email
        message = MIMEMultipart()
        message["From"] = f"{cls.COMPANY_NAME} <{cls.SENDER_EMAIL}>"
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html" if html else "plain"))

        try:
            # Connexion sécurisée au serveur SMTP
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(cls.SMTP_SERVER, cls.PORT, context=context) as server:
                server.login(cls.SENDER_EMAIL, cls.PASSWORD)
                server.sendmail(cls.SENDER_EMAIL, receiver_email, message.as_string())

            logging.info(f"✅ Email envoyé avec succès à {receiver_email} - Sujet: {subject}")
            return True

        except smtplib.SMTPAuthenticationError:
            logging.error("❌ Erreur d'authentification SMTP : Vérifiez l'email et le mot de passe.")
        except smtplib.SMTPConnectError:
            logging.error("❌ Impossible de se connecter au serveur SMTP. Vérifiez votre connexion Internet.")
        except smtplib.SMTPException as e:
            logging.error(f"❌ Erreur SMTP : {e}")
        except Exception as e:
            logging.error(f"❌ Erreur inconnue : {e}")

        return False

    @classmethod
    def test_smtp_connection(cls) -> bool:
        """Test la connexion au serveur SMTP."""
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(cls.SMTP_SERVER, cls.PORT, context=context) as server:
                server.login(cls.SENDER_EMAIL, cls.PASSWORD)
                logging.info("✅ Connexion SMTP réussie.")
                return True
        except smtplib.SMTPAuthenticationError:
            logging.error("❌ Erreur d'authentification SMTP : Email ou mot de passe incorrect.")
        except smtplib.SMTPConnectError:
            logging.error("❌ Impossible de se connecter au serveur SMTP.")
        except Exception as e:
            logging.error(f"❌ Erreur SMTP inconnue : {e}")

        return False
