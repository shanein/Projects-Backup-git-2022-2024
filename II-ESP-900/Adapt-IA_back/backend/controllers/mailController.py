from fastapi import FastAPI, UploadFile
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from io import BytesIO


welcome_mail = """
<!DOCTYPE html>
<html>
<head>
<title>Bienvenue chez SmartDisplay</title>
<style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
        background-color: #f4f4f4;
    }
    .container {
        background-color: #fff;
        padding: 20px;
        margin: auto;
        max-width: 600px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .header {
        background-color: #007bff;
        color: #ffffff;
        padding: 10px;
        text-align: center;
        border-radius: 8px 8px 0 0;
    }
    .content {
        margin-top: 20px;
    }
    .footer {
        margin-top: 20px;
        text-align: center;
        font-size: 0.9em;
        color: #777;
    }
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Bienvenue chez SmartDisplay</h1>
    </div>
    <div class="content">
        <p>Bonjour,</p>
        <p>Nous sommes ravis de vous compter parmi nous ! Votre compte est actuellement en cours de validation par notre équipe d'administration. Cela ne devrait pas prendre longtemps.</p>
        <p>Une fois validé, vous pourrez profiter pleinement de toutes les fonctionnalités de SmartDisplay.</p>
        <p>Si vous avez des questions ou besoin d'aide, n'hésitez pas à nous contacter.</p>
        <p>Merci de nous faire confiance,</p>
        <p>L'équipe SmartDisplay</p>
    </div>
    <div class="footer">
        © 2024 SmartDisplay. Tous droits réservés.
    </div>
</div>
</body>
</html>"""


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME="smartdisplay@propertize.fr",
    MAIL_PASSWORD="PipouSmart",
    MAIL_FROM="smartdisplay@propertize.fr",
    MAIL_PORT=587,
    MAIL_SERVER="ssl0.ovh.net",
    MAIL_FROM_NAME="Info Smart Display",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def simple_send(email: EmailSchema, subject: str, body: str) -> JSONResponse:
    message = MessageSchema(
        subject=subject,
        recipients=email.dict().get("email"),
        body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


async def send_welcome_email(email: EmailStr) -> JSONResponse:
    message = MessageSchema(
        subject="Bienvenue chez SmartDisplay",
        recipients=[email],
        body=welcome_mail,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
