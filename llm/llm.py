from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains.openai_functions import (
    create_openai_fn_chain,
    create_structured_output_chain,
)
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.output_parsers import CommaSeparatedListOutputParser
import tkinter as tk
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from tkinter import messagebox
import re
import requests
from langchain.text_splitter import CharacterTextSplitter
chat = ChatOpenAI(openai_api_key="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",temperature=0,)
import os
os.environ["OPENAI_API_KEY"]="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"
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()
from datetime import datetime
import json
import os
from pdf2docx import Converter
from docx import Document
import docx2txt
 
def resume_scoring_main(resume):
    # def resume_space_issue_pdf(resume):
    #     system_message_prompt = SystemMessagePromptTemplate.from_template("You are a document corecter. The given is a resume , rewrite it  so that it can be read easily")
    #     Human_message_prompt = HumanMessagePromptTemplate.from_template("Rewrite the following resume : {resume}")
    #     chat_promt_1 = ChatPromptTemplate.from_messages([system_message_prompt,Human_message_prompt])
    #     request = chat_promt_1.format_prompt(resume=resume).to_messages()
    #     result = chat(request)
    #     result = result.content
    #     return(result)
    # def update_key(input_data):
    #     if 'Total Experience' in input_data:
    #         input_data['Experience'] = input_data.pop('Total Experience')
        
    #     # Rename 'Year of Graduation' to 'Year_of_Graduation'
    #     input_data['Year_of_Graduation'] = input_data.pop('Year of Graduation')
        
    #     return input_data
 
    def update_key(input_data):
        if 'Total Experience' in input_data:
            input_data['Experience'] = input_data.pop('Total Experience')
            
        if 'Phone number' in input_data:
            input_data['phone'] = input_data.pop('Phone number')
            
        elif 'phone number' in input_data:    
            input_data['phone'] = input_data.pop('phone number')
                
        elif 'Phone Number' in input_data:    
            input_data['phone'] = input_data.pop('Phone Number')
        
        elif 'Phone' in input_data:    
            input_data['phone'] = input_data.pop('Phone')
        if 'Email ID' in input_data:
            input_data['Email'] = input_data.pop('Email ID')
                       
        # Rename 'Year of Graduation' to 'Year_of_Graduation'
     
        input_data['Year_of_Graduation'] = input_data.pop('Year of Graduation')
        
        return input_data
 
    def json_convertor(resume):
        def extract_integer_from_string(line):
            match = re.search(r'\d+', line)
            return int(match.group()) if match else None
        today_date = datetime.now()
        formatted_date = today_date.strftime("%Y-%m-%d")
        x = formatted_date
 
        system_text = "You are a helpful assistant who filter out the name of the person,Phone number ,email id ,toience in job, and his year of graduation in the resume submitted by the user. No need to show other details . Calculate the expireince until  date:"
        system_text = system_text+x
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_text)
 
        sample_resume = resume
        
        example_input_one = HumanMessagePromptTemplate.from_template(sample_resume)
 
        human_text1 = "Name, Total Experience, Year of Graduation should be in JSON Format\
                    Even if multiple resume are imported the details should be in this Exact order\
                    For Total Years of experience calculate time duration in the resume experience\
                    and add those months and convert to years and display as years\
                    If there is no experience then mention as 0 years\
                    Consider Present year as current calender year"
        example_output_one = AIMessagePromptTemplate.from_template(human_text1)
 
        human_template = "{sample_resume}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
 
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, example_input_one, example_output_one, human_message_prompt]
        )
 
 
        request = chat_prompt.format_prompt(sample_resume=resume).to_messages()
 
        result = chat(request)
 
        result = result.content
        result.replace("\n", "")
        data_dict = json.loads(result)
        total_experience_key = "Total Experience" if "Total Experience" in data_dict else "Experience"
        
        data_dict[total_experience_key] = extract_integer_from_string(data_dict[total_experience_key]) + 2
 
        return(data_dict)
    def routing_resume(resume):
        template1 = '''[Jane Smith]
        [456 Oak Street, Suite 78]
        [Metropolis, State 67890]
        [janesmith@email.com]
        [555-987-6543]
        [LinkedIn Profile, if applicable]
 
        Objective:
        Results-driven Sales Professional with expertise in selling ERP solutions. Seeking a challenging role in an ERP service company to apply my skills in driving revenue growth and building enduring client relationships.
 
        Professional Experience:
 
        ERP Sales Specialist
        TechPro Solutions, New York, NY
        Feb 2021 – Present
 
        Surpassed quarterly sales targets by 15% through strategic prospecting and effective client engagement.
        Conducted thorough needs assessments to understand client requirements and proposed customized ERP solutions to address specific business challenges.
        Worked collaboratively with the technical team to ensure the successful and timely implementation of ERP solutions, achieving a 90% customer satisfaction rate.
        Established and nurtured a robust pipeline of potential clients through participation in networking events, industry conferences, and client referrals.
        Senior Account Executive
        InnoData Systems, Chicago, IL
        June 2017 – Jan 2021
 
        Managed a portfolio of key accounts, achieving a 30% year-over-year revenue growth through effective upselling and cross-selling of ERP services.
        Conducted regular reviews with clients to align solutions with evolving business needs and identified opportunities for additional services.
        Collaborated with the marketing team to design and implement targeted campaigns, resulting in a 25% increase in lead generation.
        Partnered with the pre-sales team to ensure a seamless transition from sales to implementation.
        '''
        template2 = '''Curtis Samuel
        (123) 456-7890
        csamuel@example.com
        123 Your Street, San Diego, CA 12345
 
        Profile
        A Java Developer with entry-level experience, specializing in software development, JavaScript, SQL, and computer science. A strong background in supporting the design and development of user-centric mobile applications. Adept at performing complex testing to refine application performance and functionality.
 
        Professional Experience
        Java Developer, SoCal Tech Group, San Diego, CA
        May 2021 – Present
 
        Design, develop, and deploy Java microservices for a suite of applications supporting insurance companies and enterprise customers
        Coordinate with the development team to identify automation opportunities and improve technical support for end users
        Perform code optimization, conduct unit testing, and develop frameworks using object-oriented design principles
        Attend meetings with the development team, IT Department, and Product Owner to evaluate project progress and ensure alignment with business specifications
        Academic Experience
        Academic Projects, University of San Diego, San Diego, CA
        May 2020 – May 2021
 
        Participated in a university hackathon event, which included interfacing with software developers, web developers, graphic designers, and engineers
        Designed a web survey platform featuring questions on music genre preferences using Java and SQL
        Education
        Bachelor of Science (B.S.) Computer Science
        University of San Diego, San Diego, CA September 2017 – May 2021
        GPA: 3.85
 
        Key Skills
        JavaScript
        Software Engineering
        Python
        Object-Oriented Design (OOD)
        Application Development
        Unit Testing
        Certifications
        Oracle Certified Associate Java Programmer (OCAJP), 2021
        '''
        text = '''
        You are a expert in sorting resume . You have 7 options for the job roles  to choose from :
        Job roles to be used:
        Sales
        Java developer
        Human resources
        Oracle Apps DBA
        Accounts / Finance
        Oracle finance
        Oracle HRMS/ HCM consultant
        Note : You have to give it in the same format as mentioned above
        '''
        human_mes_1 = HumanMessagePromptTemplate.from_template(template1)
        human_mes_2 = HumanMessagePromptTemplate.from_template(template2)
        ai_mes_1 = AIMessagePromptTemplate.from_template("Sales")
        ai_mes_2 = AIMessagePromptTemplate.from_template("Java developer")
        system_m_p = SystemMessagePromptTemplate.from_template(text)
        human_m_P = HumanMessagePromptTemplate.from_template('''what is job role suited for the following {resume} . print only the job role , do not include other words         
        "Sales"
        "Java developer"
        "Human resources"
        "Oracle Apps DBA"
        "Accounts / Finance"
        "Oracle finance"
        "Oracle HRMS/ HCM consultant"
        Note: Note it  should be in same format as mentioned above
        Eg: If accountant you should return Accounts / Finance ''')
        chat_promt_1 = ChatPromptTemplate.from_messages([human_mes_1, human_mes_2,ai_mes_1,ai_mes_2,system_m_p,human_m_P])
        request = chat_promt_1.format_prompt(resume=resume).to_messages()
        result = chat(request)
        result = result.content
        return(result)
    
    def extract_total_score(text):
        def extract_integer_from_string(line):
            match = re.search(r'\d+', line)
            return int(match.group()) if match else None
 
        lines = text.split('\n')
        last_line = lines[-1]
        return extract_integer_from_string(last_line)        
            
            
            
    def resume_scoring(job_role,resume):
        def job_role_based_system_message(job_role):
            # def read_word_document(file_path):
            #     doc = Document(file_path)
            #     content = ""
 
            #     for paragraph in doc.paragraphs:
            #         content += paragraph.text + "\n"
 
            #     return content
 
 
            
            
            # content_variable = read_word_document(document_path)
 
            sales = '''
 
 
 
        You are sales expert in ERP service comapany . Your role to score a resume based on the given scoring scheme. Below mentioned are the maximum marks for each skill that can awarded. Do not just search for key words . Understand the  resume based on that give score using the marking scheme.
        Any experience involving Lead generation: 0-8 points
        Any experience involving Client management: 0-11 points
        Any experience involving Cold calling: 0-9 points
        Any experience involving Communication: 0-15 points
        Any experience involving Presentation: 0-10 points
        Any experience involving Market analysis: 0-15 points
        Any experience involving IT / ERP sales: 0-15 points
        IF the Work Experience is
        3-5 years 8 points
        5-10 years 10 points
        more than 10 years 17 points
 
        if CGPA<7 -10 points
        High Switching frequency (Switching between the jobs frequently i.e for less tha a year) -10 points
        The resume is mentionaed below
 
        Note : Even if the experice in working with certain skill is directly not mentioned : Based on the Pervious expireince if the candidate might have used a the skill or not .
 
 
        '''
            java_dev = '''
        You are a expert in Java . Your role to score a resume based on the given scoring scheme. Below mentioned are the maximum marks for each skill that can awarded. Do not just search for key words . Understand the  resume based on that give score using the marking scheme.
 
        Points allocation = Any experience in Core java: 0-5 points
        Any experience involving Mysql: 0-5 points
        Any experience involving in springboot: 0-9 points
        Any experience involving bootstrap: 0-15 points
        Any experience involving oops: 0-5 points
        Any experience involving Restapi: 0-15 points
        Any experience involving Exception Handling: 0-5 points
        Any experience involving collection : 0-5 ponits
        Any experience involving Threading : 0-5 ponits
        Any experience involving Revelant Certifications : 0-8 ponits
        Any experience involving Project description : 0-9 ponits
        Any experience involving Github or portfolio links : 0-5 ponits
        IF the Work Experience is
        3-5 years 4 points
        5-10 years 5 points
        more than 10 years 9 points
 
        if CGPA<7 -15 points
        High Switching frequency (Switching between the jobs frequently i.e for less than a year) -15 points
 
        Note : Even if the experice in working with certain skill is directly not mentioned : Based on the Pervious expireince if the candidate might have used a the skill or not .
 
 
        '''
            h_r = '''Points allocation = Any experience involving Sourcing: 0-5 points
        Any experience involving Recruitment cycle: 0-9 points
        Any experience involving Screening: 0-9 points
        Any experience involving Payroll: 0-15 points
        Any experience involving Administration: 0-14 points
        Any experience involving Grevience: 0-8 points
        Any experience involving Negotiation : 0-15 ponits
        Any experience involving Performance management : 0-5 ponits
        IF the Work Experience is
        3-5 years 5 points
        5-10 years 15 points
        more than 10 years 20 points
 
        if CGPA<7 -15 points
        High Switching frequency (Switching between the jobs frequently i.e for less than a year) -15 points
        CONSIDER THE TEMPLATE1 as resume
        '''
 
            or_apps_dba = '''Points allocation = Any experience in Oracle apps DBA & Oracle 10g / 11g / 12 c : 0-5 points
        Any experience involving Recoveries : 0-9 points
        Any experience involving Performance tuning : 0-9 points
        Any experience involving Installation bootstrap: 0-15 points
        Any experience involving Configuration : 0-14 points
        Any experience involving Upgradation: 0-15 points
        Any experience involving Patching : 0-8 points
        Any experience involving Performance management : 0-5 ponits
        IF the Work Experience is
        3-5 years 5 points
        5-10 years 15 points
        more than 10 years 20 points
 
        if CGPA<7 -15 points
        High Switching frequency (Switching between the jobs frequently i.e for less than a year) -15 points
        CONSIDER THE TEMPLATE1 as resume
        '''
            
            a_f = '''     
        Points allocation = Any experience in Invoice generation : 0-5 points
        Any experience involving Accounts receivable / AR : 0-9 points
        Any experience involving in GSTR1 & GSTR2B : 0-9 points
        Any experience involving TDS: 0-15 points
        Any experience involving Bank reconcile : 0-14 points
        Any experience involving Vendor payment : 0-8 points
        Any experience involving Zoho books : 0-15 points
        Any experience involving Performance management  : 0-5 ponits
 
        IF the Work Experience is
        3-5 years 5 points
        5-10 years 15 points
        more than 10 years 20 points
 
        if CGPA<7 -15 points
        High Switching frequency (Switching between the jobs frequently i.e for less than a year) -15 points
        CONSIDER THE TEMPLATE1 as resume
        '''
            of = '''     
        Points allocation: Any experience in Oracle EBS (R12) : 0-14 points
        Any experience involving AP (Oracle accounts payable) : 0-15 points
        Any experience involving in AR (Oracle accounts receivable) : 0-9 points
        Any experience involving GL : 0-9 points
        Any experience involving FA: 0-8 points
        Any experience involving CM: 0-5 points
        Any experience involving TDS: 0-5 points
        Any experience involving GST : 0-5 ponits
        Any experience involving Indian localization : 0-4 ponits
 
        IF the Work Experience is
        3-5 years 5 points
        5-10 years 15 points
        more than 10 years 20 points
 
        if CGPA<7 -15 points
        High Switching frequency (Switching between the jobs frequently i.e for less than a year) -15 points
        CONSIDER THE TEMPLATE1 as resume
        '''
 
            o_hrms = '''     
        Points allocation = Any experience in Core HR : 0-14 points
        Any experience involving Payroll : 0-15 points
        Any experience involving in Self-service HR : 0-15 points
        Any experience involving Performance management : 0-9 points
        Any experience involving Time & labor : 0-9 points
        Any experience involving Oracle R12 / R13: 0-18 points
 
        IF the Work Experience is
        3-5 years 5 points
        5-10 years 15 points
        more than 10 years 20 points
 
        if CGPA<7 -15 points
        High Switching frequency (Switching between the jobs frequently i.e for less than a year) -15 points
        CONSIDER THE TEMPLATE1 as resume
        '''
 
                    
            if job_role == '''Sales''':
                document_path = sales
 
            elif job_role == "Java developer":
                document_path  = java_dev
 
            elif job_role =="Human resources":
                document_path = h_r
 
            elif job_role =="Oracle Apps DBA":
                document_path = or_apps_dba
 
            elif job_role =="Accounts / Finance":
                document_path =   a_f
 
            elif job_role =="Oracle finance":
                document_path = of
 
            elif job_role =="Oracle HRMS/ HCM consultant":
                document_path = o_hrms
            else:
                document_path  = java_dev
 
 
 
            return(document_path)
        marking_sheme = job_role_based_system_message(job_role)
        system_m_p = SystemMessagePromptTemplate.from_template(marking_sheme)
        human_m_P = HumanMessagePromptTemplate.from_template("Give the cummulative calculated score of the following resume : {resume}.")
        chat_promt_1 = ChatPromptTemplate.from_messages([system_m_p,human_m_P])
        request = chat_promt_1.format_prompt(resume=resume).to_messages()
        result = chat(request)
        result = result.content
        return result
    
    # resume = resume_space_issue_pdf(resume)
    job_role= routing_resume(resume)
    initial_json = json_convertor(resume)
    
    initial_json['Resume_score'] = extract_total_score(resume_scoring(job_role,resume))
    initial_json['Job_Role'] = job_role
    #resume_score = extract_total_score(resume_scoring(job_role,resume))
    #resume_score = resume_scoring(job_role,resume)
    initial_json=update_key(initial_json)
    # resumelist=[]
    # resumelist.append(initial_json)
    return initial_json
 
def convert_pdf_to_docx(pdf_path, docx_path):
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()
 
def extract_text_from_docx(docx_path):
    try:
        text = docx2txt.process(docx_path)
        return text
    except Exception as e:
        print(f"Error extracting text from {docx_path}: {e}")
        return ""
 
def convert_and_extract_text(pdf_directory, docx_directory, moved_pdf_directory):
    Text_list = []
    if not os.path.exists(docx_directory):
        os.makedirs(docx_directory)
    if not os.path.exists(moved_pdf_directory):
        os.makedirs(moved_pdf_directory)
 
    for pdf_filename in os.listdir(pdf_directory):
        if pdf_filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, pdf_filename)
            docx_filename = os.path.splitext(pdf_filename)[0] + '.docx'
            docx_path = os.path.join(docx_directory, docx_filename)
 
            try:
                convert_pdf_to_docx(pdf_path, docx_path)
                Text_list.append(extract_text_from_docx(docx_path))
                # print(f"Text extracted from {docx_filename}:\n{text}")
                os.remove(docx_path)
                moved_pdf_path = os.path.join(moved_pdf_directory, pdf_filename)
                os.rename(pdf_path, moved_pdf_path)
                Text_list.append(moved_pdf_path)
            except Exception as e:
                print(f"Error processing {pdf_filename}: {e}")
        elif pdf_filename.endswith('.docx'):
            docx_path = os.path.join(pdf_directory, pdf_filename)
            try:
                Text_list.append(extract_text_from_docx(docx_path))
                moved_docx_path = os.path.join(moved_pdf_directory, pdf_filename)
                os.rename(docx_path, moved_docx_path)
                Text_list.append(moved_docx_path)
            except Exception as e:
                print(f"Error processing {pdf_filename}: {e}")
 
    return Text_list