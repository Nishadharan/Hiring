from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class sendMail:
    from_email='nishadharan.kumar@focusrtech.com'
    
    def sendMailtoReceipients(self, htmlMessage, subject, recipient):
            # Extract data from the request, if needed
            # subject = request.data.get('subject', 'Default Subject')
            # html_message = request.data.get('html_message', '<p>Default HTML Message</p>')
            # subject=subject
            
            # recipient_list = recipient
            print('before send method called')
            # Create an EmailMultiAlternatives object to send both HTML and plain text versions
            email = EmailMultiAlternatives(subject, strip_tags(htmlMessage), self.from_email, [recipient])
            email.attach_alternative(htmlMessage, "text/html")
            print('send method called')
            try:
                email.send()
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)