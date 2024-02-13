
class emailHtmlLoader:
    
    @staticmethod
    def userCreatedMail(userpayload):
        content = f"""<html><body>
        Good day {userpayload.get('username', None)},<br>
        User created!<br>
        <b>Username:</b> {userpayload.get('username', None)}<br>
        <b>password: </b>{userpayload.get('password', None)}<br> 
        <b>email: </b>{userpayload.get('email', None)}<br> 
        <p>Thanks and Regards,</p>
        <p>Team FocusR</p>
        </body></html>"""
        return content
    
    @staticmethod
    def userUpdateMail(userpayload):
        content = f"""<html><body>
        Good day {userpayload.get('username', None)},<br>
        User updated!<br>
        <b>Username:</b> {userpayload.get('username', None)}<br>
        <b>password: </b>{userpayload.get('password', None)}<br> 
        <b>email: </b>{userpayload.get('email', None)}<br> 
        <p>Thanks and Regards,</p>
        <p>Team FocusR</p>
        </body></html>"""
        return content

    @staticmethod
    def HrNotShortistedMail(candidate):
        content = f"""<html><body>
        Dear {candidate.get('name', None)},<br>
        
        <p>Thank you for applying for the {candidate.get('jobRole'), None} role at <b>FocusR consultancy and Technologies</b>. After careful consideration, we regret to inform you that we have chosen to move forward with other candidates</p><br>
        
        <p>We appreciate your interest and encourage you to keep an eye on our career page for future opportunities.</p>
        <p>Thanks and Regards,</p>
        <p>Team FocusR</p>
        </body></html>"""
        return content
    
    @staticmethod
    def HrShortistedMail(candidate):
        content = f"""<html><body>
        
        Dear {candidate.get('name', None)},<br>
        
        <p>Congratulations! We are excited to inform you that your application for the {candidate.get('jobRole'), None} role at <b>FocusR consultancy and Technologies</b> has been shortlisted.</p>
        
        <p>We were impressed with your qualifications and experience, and we look forward to getting to know you better during the next stages of the hiring process. Our team will be in touch soon to schedule an interview.</p><br>
        
        <p>Once again, congratulations on reaching this milestone, and thank you for your interest in joining [Company Name].</p>
        
        <p>Thanks and Regards,</p>
        <p>Team FocusR</p>
        </body></html>"""
        return content