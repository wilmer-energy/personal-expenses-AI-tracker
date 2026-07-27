import os

import resend

from core.providers.email.email_provider import EmailProvider


class ResendEmailProvider(EmailProvider):

    def __init__(self):
        resend.api_key = os.environ["RESEND_API_KEY"]

    def send_verification_code_email(
        self,
        code: int,
        email: str,
    ) -> None:

        resend.Emails.send(
            {
                "from": "Expenses Tracker <noreply@mi-energia.online>",
                "to": [email],
                "subject": "Password recovery code",
                "html": f"""
                    <h2>Password recovery</h2>

                    <p>Your verification code is:</p>

                    <h1>{code}</h1>

                    <p>This code expires in 10 minutes.</p>
                """,
            }
        )
