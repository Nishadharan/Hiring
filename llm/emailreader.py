from django.shortcuts import render

# Create your views here.

import os
import imaplib
import email
from email.header import decode_header
from pdfminer.high_level import extract_text
from docx import Document
from HRLevel.models import candidate_info

# Function to fetch PDF and DOCX attachments from unread emails
def fetch_attachments(email_address, password, server, port, mailbox="inbox"):
    # Connect to the email server
    mail = imaplib.IMAP4_SSL(server, port)
    mail.login(email_address, password)
    mail.select(mailbox)

    # Search for unread emails
    status, messages = mail.search(None, "(UNSEEN)")
    messages = messages[0].split()

    # Specify the directory to save attachments
    save_path = "resumes"

    for msg_id in messages:
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Iterate through the parts of the email
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Extract attachments (PDF and DOCX)
            if "attachment" in content_disposition:
                filename = decode_header(part.get_filename())[0][0]
                if isinstance(filename, bytes):
                    filename = filename.decode()

                if content_type == "application/pdf":
                    # Save PDF attachment to a specific directory
                    with open(os.path.join(save_path, filename), "wb") as pdf_file:
                        pdf_file.write(part.get_payload(decode=True))
                    # Extract text from PDF

                elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    # Save DOCX attachment to a specific directory
                    with open(os.path.join(save_path, filename), "wb") as docx_file:
                        docx_file.write(part.get_payload(decode=True))