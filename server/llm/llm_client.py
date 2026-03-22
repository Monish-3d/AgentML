from langchain_google_genai import ChatGoogleGenerativeAI
from schema import Plan
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model= 'gemini-2.5-pro')
struct_model = model.with_structured_output(Plan)

def get_preprocess_steps(prompt):

    try:
        response = struct_model.invoke(prompt)
        return response.steps

    except Exception as e:
        #raise ValueError(f'LLM error: {e}')
        print(f'LLM error: {e}, performing no preprocessing steps')
        return []
        