#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from .my_utils import show_message

### Credentials #####################################################################################################################

def get_credentials(file):
    try:
        with open(f'credentials/{file}.txt', encoding="utf-8") as f:
            lines = f.readlines()

    except FileNotFoundError as e:
        show_message(f"No s'ha trobat el fitxer 'credentials/{file}'.txt: ", "error", e)
        return None

    if len(lines) < 2 or not lines[1].strip():
        show_message(f"No s'ha trobat cap dada a la segona línia de '{file}'. Escriu-la sota el comentari.", "error")
        return None

    return lines[1].strip()

### Mail Functions ##################################################################################################################

def smail(subject, body, sender, recipients, password):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

        show_message("Email sent successfully")

    except Exception as e:
        show_message(f"Error sending email: {str(e)}", "error")
