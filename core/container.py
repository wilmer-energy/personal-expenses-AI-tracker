from core.providers.email.resend_email_provider import ResendEmailProvider


class Container:
    email_provider = ResendEmailProvider()