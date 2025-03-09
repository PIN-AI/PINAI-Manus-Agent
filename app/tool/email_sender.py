import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Optional
import aiosmtplib

from app.tool.base import BaseTool


class EmailSender(BaseTool):
    name: str = "email_sender"
    description: str = """Send emails from smile@pinai.io Google account.
Use this tool when you need to send information, documents, or notifications through email.
You can specify recipients, subject, body content, and optional attachments.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "to": {
                "type": "array",
                "items": {"type": "string"},
                "description": "(required) List of email addresses to send the email to.",
            },
            "subject": {
                "type": "string",
                "description": "(required) Subject line of the email.",
            },
            "body": {
                "type": "string",
                "description": "(required) Content of the email, can be plain text or HTML.",
            },
            "cc": {
                "type": "array",
                "items": {"type": "string"},
                "description": "(optional) List of email addresses to CC.",
            },
            "bcc": {
                "type": "array",
                "items": {"type": "string"},
                "description": "(optional) List of email addresses to BCC.",
            },
            "attachment_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "(optional) List of file paths to attach to the email.",
            },
        },
        "required": ["to", "subject", "body"],
    }

    async def execute(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachment_paths: Optional[List[str]] = None,
    ) -> str:
        """
        Send an email from smile@pinai.io Google account.

        Args:
            to (List[str]): List of recipients' email addresses.
            subject (str): Email subject.
            body (str): Email body content.
            cc (Optional[List[str]]): List of CC recipients.
            bcc (Optional[List[str]]): List of BCC recipients.
            attachment_paths (Optional[List[str]]): List of file paths to attach.

        Returns:
            str: Status message indicating success or failure.
        """
        try:
            # Set up message
            msg = MIMEMultipart()
            msg["From"] = "smile@pinai.io"
            msg["To"] = ", ".join(to)
            msg["Subject"] = subject
            
            if cc:
                msg["Cc"] = ", ".join(cc)
            if bcc:
                msg["Bcc"] = ", ".join(bcc)
            
            # Attach body
            msg.attach(MIMEText(body, "html" if "<html>" in body.lower() else "plain"))
            
            # Attach files if provided
            if attachment_paths:
                for file_path in attachment_paths:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as file:
                            part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
                        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
                        msg.attach(part)
                    else:
                        return f"Error: Attachment file not found: {file_path}"
            
            # Get credentials from environment variables for security
            email = "smile@pinai.io"
            password = os.environ.get("EMAIL_PASSWORD")
            
            
            if not password:
                return "Error: EMAIL_PASSWORD environment variable not set"
            
            # 修复：直接使用SSL连接，避免TLS问题
            smtp = aiosmtplib.SMTP(hostname="smtp.gmail.com", port=465, use_tls=True)
            await smtp.connect()
            await smtp.login(email, password)
            
            # Prepare all recipients
            all_recipients = to.copy()
            if cc:
                all_recipients.extend(cc)
            if bcc:
                all_recipients.extend(bcc)
            
            # Send email
            await smtp.send_message(msg)
            await smtp.quit()
            
            return f"Email successfully sent to {', '.join(to)}"
            
        except Exception as e:
            return f"Failed to send email: {str(e)}" 