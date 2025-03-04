import streamlit as st
from build_graph import app
from build_pdf import convert_to_pdf
import warnings

warnings.filterwarnings("ignore")

def main():
    st.set_page_config(page_title="AI-Powered Resume Builder", layout="centered")
    st.markdown("""
        <style>
            .main-title { font-size: 3.5em; font-weight: bold; text-align: center; color: #4F8BF9; }
            .sub-title { font-size: 1.8em; text-align: center; color: #6c757d; }
            .input-box { border-radius: 10px; padding: 10px; }
            .stButton>button { width: 100%; border-radius: 10px; padding: 12px; font-size: 1.3em; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='main-title'>🚀 AI-Powered Resume Builder</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Craft professional resumes tailored to your dream job in seconds.</p>", unsafe_allow_html=True)

    with st.form(key='resume_form'):
        linkedin_url = st.text_input("Enter your LinkedIn profile URL:", placeholder="E.g., https://www.linkedin.com/in/your-profile")
        query = st.text_area("Enter your information (education, skills, projects, etc.):", placeholder="E.g., BTech in Computer Science, skilled in Python, built an AI project...")
        question = st.selectbox(
            "Select a role to tailor your resume:",
            ["Data Scientist", "Product Manager", "Content Writer", "Custom"]
        )
        custom_question = ""
        if question == "Custom":
            custom_question = st.text_input("Enter your custom role:", placeholder="E.g., AI Researcher")

        submit_button = st.form_submit_button(label="Generate Resume")

    if submit_button:
        if not linkedin_url.strip():
            st.warning("Please provide your LinkedIn profile URL.")
        else:
            user_name = "User"
            output_pdf_dir = f"{user_name}_Resume.pdf"
            linkedin_url = linkedin_url.strip()
            selected_question = custom_question if question == "Custom" else question

            inputs = {"question": selected_question, "query": query, "linkedin_link": linkedin_url}
            json_output = None

            with st.spinner("Generating your resume... ✨"):
                for output in app.stream(inputs):
                    for key, value in output.items():
                        if "json_output" in value:
                            json_output = value["json_output"]

            if json_output:
                convert_to_pdf(output_file=output_pdf_dir, content=json_output)
                st.success("🎉 Resume generated successfully!")
                with open(output_pdf_dir, "rb") as pdf_file:
                    st.download_button(label="📥 Download Resume", 
                                       data=pdf_file.read(),
                                       file_name=output_pdf_dir,
                                       mime="application/pdf")
            else:
                st.error("Failed to generate resume. Please try again.")

if __name__ == "__main__":
    main()
