import os
from openai import OpenAI
from markdown2 import markdown
from weasyprint import HTML
import pdfkit
import pdfplumber
from template import mdtemplate
import streamlit as st 

client = None
linkedin = os.environ.get("LINKEDIN",None)
github = os.environ.get("GITHUB",None)

prompt = f"""
Role:
You are a highly skilled resume expert specializing in enhancing and tailoring resumes to align with specific job requirements. Your expertise lies in refining resumes to highlight the most relevant skills, achievements, and experiences, ensuring they align with the target role's expectations.

Task:
You will be provided with:
    1. An existing resume.
    2. A set of job requirements for a specific role.

Your goal is to generate a refined resume in Markdown format following the provided {mdtemplate} structure.

Enhancements to Apply:
    - Alignment with Job Requirements: Modify and emphasize skills, experiences, and accomplishments that best match the job description.
    - Bullet Points for Impact: Ensure each work experience entry contains exactly five compelling bullet points, highlighting key contributions and quantifiable achievements.
    - Invented/Expanded Content: If necessary, infer or creatively enhance project descriptions, job tasks, or impact statements to better fit the target role.
    - Consistency & Readability: Maintain professional formatting, clarity, and readability. Ensure the resume is concise yet detailed.
    - Additional Sections: Include LinkedIn URL: {linkedin} and GitHub URL: {github} if applicable, ensuring a comprehensive and well-rounded professional profile.

Output Format:
    The final output must be structured in Markdown format as per provided template.
"""


def get_client():
    global client
    if client is None:
        open_api_key = st.secrets["API_KEY"]
        if not open_api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        client = OpenAI(api_key=open_api_key)
    return client

def optimize(cl, resume, job_requirements):
    response = cl.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"""1. My resume: 

                                    {resume} 
                                
                                2. Below is job requirements: 
                    
                                     {job_requirements}
                        """
            }
        ]
    )
    return response.choices[0].message.content


def md_to_pdf(resume_md):
    html_content = markdown.markdown(resume_md)
    pdfkit.from_string(html_content, 'output_resume.pdf')


def extract_pdf(file):
    with pdfplumber.open(file) as pdf:
        resume_text = ""
        for page in pdf.pages:
            resume_text += page.extract_text()
        return resume_text
    return ""

def write_pdf_resume(newresume, output_pdf):
    custom_css = """
    <style>
    /* General Page Settings */
@page {
    margin: 0.25in;
}

body {
    font-family: Arial, sans-serif; /* Professional, clean font */
    font-size: 12px; /* Adjust to your desired size */
    line-height: 1.6; /* Better readability */
    color: #333;
    margin: 0;
    padding: 0;
}

/* Header Section (Name and Contact Info) */
header {
    text-align: center;
    margin-bottom: 10px;
}

header h1 {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}

header p {
    font-size: 12px;
    margin: 0;
    color: #555;
}

header a {
    color: #1a73e8; /* Subtle blue for links */
    text-decoration: none;
}

header a:hover {
    text-decoration: underline;
}

/* Section Titles */
h2, h3 {
    color: #222;
    font-weight: bold;
    border-bottom: 1px solid #ccc; /* Section dividers */
    padding-bottom: 5px;
    margin-top: 10px;
}

/* Section Content */
section {
    margin-bottom: 20px;
}

/* Bullet Points */
ul {
    list-style-type: disc;
    margin-left: 10px;
    padding-left: 0;
}

li {
    margin-bottom: 0;
    padding-left: 0;
    padding-bottom: 0;
}

/* Thin Light Gray Lines Between Sections */
hr {
    border: 0;
    border-top: 1px solid #ddd;
    margin: 20px 0;
}

/* Table for Skills/Certifications (Optional Alignment) */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

td {
    padding: 5px;
    vertical-align: top;
}

/* Footer Section (For Certification/Skills if Necessary) */
footer {
    text-align: center;
    font-size: 10px;
    color: #999;
    margin-top: 20px;
}

</style>
    """
    html_content = markdown(newresume)

    html_with_style = f"""
    <!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    {custom_css}
</head>
<body>
    <!-- markdown -->
    {html_content}
</body>
</html>
"""
    HTML(string=html_with_style).write_pdf(output_pdf)
    print(f"PDF generated: {output_pdf}")



# write_pdf_resume("/home/raman/Downloads/MyResumes.md", "output.pdf")
