#EMAIL = "pruebacarniceria49@gmail.com"
#PASSWORD_EMAIL = "ebsc lqyp rbms cugb"

import smtplib
from email.mime.text import MIMEText

class EmailService:
    def __init__(self):
        self.remitente = "pruebacarniceria49@gmail.com"
        self.password = "ebsc lqyp rbms cugb" # Contraseña de aplicación de Google

    def enviar_codigo_verificacion(self, destino, codigo):
        msg = MIMEText(f"Tu código de verificación para tu pedido de carnicería es: {codigo}")
        msg['Subject'] = 'Verificación de Pedido - Carnicería'
        msg['From'] = self.remitente
        msg['To'] = destino

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.remitente, self.password)
                server.sendmail(self.remitente, destino, msg.as_string())
            return True
        except Exception as e:
            print(f"Error enviando correo: {e}")
            return False