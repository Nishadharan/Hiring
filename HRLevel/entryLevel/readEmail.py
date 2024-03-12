import imaplib
import email
from bs4 import BeautifulSoup
import base64
from email.utils import parsedate_to_datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def read_mail(email_address, email_user, email_password):
    def process_batch_emails(email_ids, email_json, email_address):
        futures = []
        with ThreadPoolExecutor() as executor:
            for email_id in email_ids:
                email_id_str = email_id.decode('utf-8')
                try:
                    _, msg_data = mail.uid('fetch', email_id_str, "(RFC822)")
                    if msg_data is not None and msg_data[0] is not None and msg_data[0][1] is not None:
                        msg = email.message_from_bytes(msg_data[0][1])
                        futures.append(executor.submit(process_email, msg, email_id_str, email_json, email_address))
                    else:
                        print(f"No data found for email ID: {email_id_str}")
                except imaplib.IMAP4_SSL.error as e:
                    print(f"Error fetching email ID: {email_id_str} - {e}")
                    continue

        # Wait for all tasks to complete
        for future in as_completed(futures):
            future.result()

    mail = imaplib.IMAP4_SSL("imap.secureserver.net")
    mail.login(email_user, email_password)
    email_json = {}
    # Process received emails
    mail.select('"inbox"')
    status_received, messages_received = mail.uid('search', None, f'(FROM "{email_address}")')
    if status_received == "OK" and messages_received is not None:
        message_ids_received = messages_received[0].split()
        batch_size = 20  # Adjust the batch size based on your system's capabilities
        for i in range(0, len(message_ids_received), batch_size):
            process_batch_emails(message_ids_received[i:i+batch_size], email_json, email_address)
    else:
        print(f"Error searching for received emails: {status_received}")

    # Process sent emails
    # mail.select('"Sent Items"')
    mail.select('"Sent Items"')
    status_sent, messages_sent = mail.uid('search', None, f'(TO "{email_address}")')
    if status_sent == "OK" and messages_sent is not None:
        message_ids_sent = messages_sent[0].split()
        batch_size = 20  # Adjust the batch size based on your system's capabilities
        for i in range(0, len(message_ids_sent), batch_size):
            process_batch_emails(message_ids_sent[i:i+batch_size], email_json, email_user)
    else:
        print(f"Error searching for sent emails: {status_sent}")

    mail.logout()
    return email_json

# The process_email function remains unchanged

# Example usage



def process_email(msg, email_id, email_json, email_address):
    # Extract date and time information
    received_date = parsedate_to_datetime(msg.get("Date"))

    # Initialize an empty string to store the HTML content
    full_html_content = ""
    image_datas = []

    # Loop through the parts of the email
    for part in msg.walk():
        
        if part.get_content_type().startswith("text/html"):
            # Handle HTML part
            html_content = part.get_payload(decode=True).decode("utf-8", errors="ignore")
            full_html_content += html_content

        if part.get_content_type().startswith("image"):
            image_content = part.get_payload(decode=True)
            image_datas.append(image_content)

        if part.get("Content-Disposition") and part.get("Content-Disposition").startswith("attachment"):
            # Handle attachment
            filename = part.get_filename()

            # Add a new link to the HTML for each attachment
            attachment_link = f'<a href="data:application/octet-stream;base64,{base64.b64encode(part.get_payload(decode=True)).decode("utf-8")}" download="{filename}">{filename}</a>'
            full_html_content += f"<p>Attachment: {attachment_link}"

    count = len(image_datas) - 1
    soup = BeautifulSoup(full_html_content, "html.parser")

    # Update image sources in the HTML content
    for img_tag in soup.find_all("img"):
        content_id = img_tag.get("src")
        if content_id and content_id.startswith("cid:"):
            # Fetch the image data using the content_id

            # Encode the image data as base64
            base64_data = base64.b64encode(image_datas[count]).decode("utf-8")
            count -= 1
            # Update the src attribute of the img tag with the base64 data
            img_tag["src"] = f"data:image/png;base64,{base64_data}"

    # Write the modified HTML content to a new HTML file
    email_json[email_id] = {
        'emailContent': str(soup.prettify()),
        'dateAndTime': received_date,
        'emailAddress': email_address
    }

    