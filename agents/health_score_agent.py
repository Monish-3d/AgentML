from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel , Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

class Explanation(BaseModel):
        explanation: str = Field(description="Beginner friendly explanation of dataset health")


def generate_health_explanation(report):

    model = ChatGoogleGenerativeAI(model = 'gemini-3-flash-preview')
    # struct_model = model.with_structured_output(Explanation)

    #parser = JsonOutputParser(pydantic_object=Explanation)

    # class Report(BaseModel):
    #     rows : int = Field(description='the number of rows in the dataset')
    #     columns: int = Field(description='the number of columns in the dataset')
    #     missing_ratio: float
    #     skewed_features: List[str] = Field(description='the list of columns containing skewed features')
    #     high_correlations : List[Tuple[str,str]]
    #     health_score : int

 
    

    template = PromptTemplate(
        template= ''' 
        You are a machine learning assistant explaining dataset quality to a beginner.

        Dataset report:
        {report}

        Explain in simple language:

        1. Why the dataset health score is what it is
        2. What issues exist in the dataset
        3. How these issues might affect ML models
        4. What the system will automatically fix

        Keep the explanation very short, precise and beginner friendly. 
        Keep it in bullet points and to the point.
        ''',
        input_variables=['report']
        #partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    prompt = template.invoke({'report': report})

    stream = model.stream(prompt)

    return stream