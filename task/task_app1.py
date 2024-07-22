from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
import os
import json

# Load environment variables from .env file
load_dotenv()

# Set environment variables for LangChain
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Retrieve the Google API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize GoogleGenerativeAI with the API key
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

# Define the prompt template for extracting entities
extract_prompt_template = """
You are an experienced recruiter. Please extract the following information from the job description and return it as a JSON object:
1. Job Title
2. Responsibilities
3. Required Skills
4. Qualifications
5. Experience Required
6. Company Information
7. Location

Job Description:
{job_desc}
"""

# Define the prompt template for generating questions
question_prompt_template = """
Based on the following extracted job description entities, generate questions to fill in any gaps or missing information:

Entities:
{entities}

Please generate questions in a numbered list format.
"""

# Define the prompt template for generating the refined job description
refine_prompt_template = """
You are an experienced recruiter. Based on the original job description, extracted entities, and additional information provided by the user, generate an enhanced job description.

Original Job Description:
{job_desc}

Extracted Entities:
{entities}

Additional Information:
{answers}

Please provide an ideal job description for the recruiter.
"""

# Function to extract entities from the job description
def extract_entities(job_desc):
    try:
        response = llm.invoke(extract_prompt_template.format(job_desc=job_desc))
        response = response.strip().strip("```json").strip()
        extracted_entities = json.loads(response)
        return extracted_entities
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return {"error": "Response is not valid JSON"}
    except Exception as e:
        print("An unexpected error occurred:", e)
        return {"error": "An unexpected error occurred"}

# Function to generate questions based on extracted entities
def generate_questions(extracted_entities):
    try:
        entities_str = json.dumps(extracted_entities, indent=2)
        question_prompt = question_prompt_template.format(entities=entities_str)
        questions_response = llm.invoke(question_prompt)
        questions = questions_response.strip().split('\n')
        return questions
    except Exception as e:
        print("An unexpected error occurred while generating questions:", e)
        return ["An error occurred while generating questions."]

# Function to generate the refined job description
def generate_refined_job_description(job_desc, extracted_entities, answers):
    try:
        entities_str = json.dumps(extracted_entities, indent=2)
        answers_str = json.dumps(answers, indent=2)
        refine_prompt = refine_prompt_template.format(
            job_desc=job_desc, entities=entities_str, answers=answers_str
        )
        refined_response = llm.invoke(refine_prompt)
        return refined_response.strip()
    except Exception as e:
        print("An unexpected error occurred while refining the job description:", e)
        return "An error occurred while refining the job description."

# Streamlit setup
st.title('Job Description Refinement')

# Initialize session state variables to store state
if 'job_desc' not in st.session_state:
    st.session_state.job_desc = ""
if 'extracted_entities' not in st.session_state:
    st.session_state.extracted_entities = {}
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0

# User input
st.session_state.job_desc = st.text_area("Enter the job description", value=st.session_state.job_desc)
submit_extract = st.button("Extract Entities and Generate Questions")

# Handle state and interactions for extraction and question generation
if submit_extract:
    try:
        st.session_state.extracted_entities = extract_entities(st.session_state.job_desc)
        st.subheader("Extracted Entities:")
        st.write(st.session_state.extracted_entities)
        st.session_state.questions = generate_questions(st.session_state.extracted_entities)
        st.session_state.current_question_index = 0
        st.session_state.answers = {}

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Interactive Chatbot for collecting responses
if st.session_state.questions:
    st.subheader("Please answer the following question to refine the job description:")

    current_index = st.session_state.current_question_index
    if current_index < len(st.session_state.questions):
        question = st.session_state.questions[current_index]
        answer_key = f"answer_{current_index}"

        answer = st.text_input(question, key=answer_key)
        submit_answer = st.button("Submit Answer")

        if submit_answer:
            st.session_state.answers[answer_key] = answer
            st.session_state.current_question_index += 1
            st.experimental_rerun()
    else:
        st.subheader("All questions answered. Here is the refined job description:")
        st.write("Display refined job description here (to be implemented)")

# Handle state and interactions for refining the job description
submit_final = st.button("Generate Final Job Description")

if submit_final:
    try:
        answers = [st.session_state.answers[f"answer_{i}"] for i in range(len(st.session_state.questions))]
        refined_job_desc = generate_refined_job_description(st.session_state.job_desc, st.session_state.extracted_entities, answers)
        
        st.subheader("Refined Job Description:")
        st.write(refined_job_desc)

    except Exception as e:
        st.error(f"An error occurred: {e}")






























# from langchain_google_genai import GoogleGenerativeAI
# from dotenv import load_dotenv
# import streamlit as st
# import os
# import json

# # Load environment variables from .env file
# load_dotenv()

# # Set environment variables for LangChain
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# # Retrieve the Google API key from environment variables
# google_api_key = os.getenv("GOOGLE_API_KEY")

# # Initialize GoogleGenerativeAI with the API key
# llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

# # Define the prompt template for extracting entities
# extract_prompt_template = """
# You are an experienced recruiter. Please extract the following information from the job description and return it as a JSON object:
# 1. Job Title
# 2. Responsibilities
# 3. Required Skills
# 4. Qualifications
# 5. Experience Required
# 6. Company Information
# 7. Location

# Job Description:
# {job_desc}
# """

# # Define the prompt template for generating questions
# question_prompt_template = """
# Based on the following extracted job description entities, generate questions to fill in any gaps or missing information:

# Entities:
# {entities}

# Please generate questions in a numbered list format.
# """

# # Function to extract entities from the job description
# def extract_entities(job_desc):
#     try:
#         response = llm.invoke(extract_prompt_template.format(job_desc=job_desc))
#         response = response.strip().strip("```json").strip()
#         extracted_entities = json.loads(response)
#         return extracted_entities
#     except json.JSONDecodeError as e:
#         print("JSON Decode Error:", e)
#         return {"error": "Response is not valid JSON"}
#     except Exception as e:
#         print("An unexpected error occurred:", e)
#         return {"error": "An unexpected error occurred"}

# # Function to generate questions based on extracted entities
# def generate_questions(extracted_entities):
#     try:
#         entities_str = json.dumps(extracted_entities, indent=2)
#         question_prompt = question_prompt_template.format(entities=entities_str)
#         questions_response = llm.invoke(question_prompt)
#         questions = questions_response.strip().split('\n')
#         return questions
#     except Exception as e:
#         print("An unexpected error occurred while generating questions:", e)
#         return ["An error occurred while generating questions."]

# # Function to refine the job description based on answers
# def refine_job_description(extracted_entities, answers):
#     # Assuming answers are in the same order as the generated questions
#     refined_entities = extracted_entities.copy()
    
#     # You can update this logic to suit the specific format of your questions and answers
#     for i, answer in enumerate(answers):
#         # Example: if the question was about Responsibilities, append the answer to Responsibilities
#         if "Responsibilities" in refined_entities and i < len(refined_entities["Responsibilities"]):
#             refined_entities["Responsibilities"].append(answer)
#         elif "Required Skills" in refined_entities and i < len(refined_entities["Required Skills"]):
#             refined_entities["Required Skills"].append(answer)
#         # Add similar conditions for other entities if needed
    
#     return refined_entities

# # Streamlit setup
# st.title('Job Description Refinement')

# # Initialize session state variables to store state
# if 'job_desc' not in st.session_state:
#     st.session_state.job_desc = ""
# if 'extracted_entities' not in st.session_state:
#     st.session_state.extracted_entities = {}
# if 'questions' not in st.session_state:
#     st.session_state.questions = []
# if 'answers' not in st.session_state:
#     st.session_state.answers = {}
# if 'current_question_index' not in st.session_state:
#     st.session_state.current_question_index = 0

# # User input
# st.session_state.job_desc = st.text_area("Enter the job description", value=st.session_state.job_desc)
# submit_extract = st.button("Extract Entities and Generate Questions")

# # Handle state and interactions for extraction and question generation
# if submit_extract:
#     try:
#         st.session_state.extracted_entities = extract_entities(st.session_state.job_desc)
#         st.subheader("Extracted Entities:")
#         st.write(st.session_state.extracted_entities)
#         st.session_state.questions = generate_questions(st.session_state.extracted_entities)
#         st.session_state.current_question_index = 0
#         st.session_state.answers = {}

#     except Exception as e:
#         st.error(f"An error occurred: {e}")

# # Interactive Chatbot for collecting responses
# if st.session_state.questions:
#     st.subheader("Please answer the following question to refine the job description:")

#     current_index = st.session_state.current_question_index
#     if current_index < len(st.session_state.questions):
#         question = st.session_state.questions[current_index]
#         answer_key = f"answer_{current_index}"

#         answer = st.text_input(question, key=answer_key)
#         submit_answer = st.button("Submit Answer")

#         if submit_answer:
#             st.session_state.answers[answer_key] = answer
#             st.session_state.current_question_index += 1
#             st.experimental_rerun()
#     else:
#         st.subheader("All questions answered. Here is the refined job description:")
#         st.write("Display refined job description here (to be implemented)")

# # Handle state and interactions for refining the job description
# submit_final = st.button("Generate Final Job Description")

# if submit_final:
#     try:
#         answers = [st.session_state.answers[f"answer_{i}"] for i in range(len(st.session_state.questions))]
#         refined_entities = refine_job_description(st.session_state.extracted_entities, answers)
        
#         st.subheader("Refined Job Description:")
#         st.write(refined_entities)

#     except Exception as e:
#         st.error(f"An error occurred: {e}")






















