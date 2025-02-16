import streamlit as st
import os

from utils import (optimize,write_pdf_resume, get_client, extract_pdf)

cl = get_client()

st.title("BoostPDF 🚀")

linkedin = st.text_input("LinkedIn URL (optional)", placeholder="https://linkedin.com/in/your-profile")

github = st.text_input("Github URL (optional)", placeholder="https://github.com/your-profile")


upload = st.file_uploader("Resume file", type="pdf")
job_description = st.text_area(label="Job Description",height=200)
downloadfname = st.text_input("Enhanced file name")

if st.button(label='Submit', type="primary", use_container_width=True):
    if upload is not None:
        resumetxt = extract_pdf(upload)
        if job_description is not None:
            if linkedin:
                os.environ["LINKEDIN"] = linkedin
            if github:
                os.environ["GITHUB"] = github
            enhanced = optimize(cl, resume=resumetxt, job_requirements=job_description)
            write_pdf_resume(enhanced, "temp.pdf")
        else:
            st.info("Please enter the job description")
    else:
        st.info("Please upload your resume to enhance")

dwnld = open("temp.pdf", "rb")
st.download_button("Save PDF", data=dwnld, use_container_width=True, file_name=f"{downloadfname}.pdf")
        

