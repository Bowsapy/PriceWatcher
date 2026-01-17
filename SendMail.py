import smtplib
from email.message import EmailMessage
password= "jfeg hvsl nijx mquh"

def send_price_alert(to_email, product, price, target_price, url):
    msg = EmailMessage()
    msg["Subject"] = f"🔔 Cena klesla: {product}"
    msg["From"] = "janbouza5@gmail.com"
    msg["To"] = to_email

    msg.set_content(
        f"""Cena produktu klesla!

Produkt: {product}
Aktuální cena: {price} Kč
Tvoje cílová cena: {target_price} Kč

Odkaz:
{url}
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("janbouza5@gmail.com", password)
        smtp.send_message(msg)

send_price_alert("janbouza5@seznam.cz","produkt","333","555","fsf")