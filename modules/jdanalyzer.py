from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from classes_types_dec.structured_outputs import JDResponse
from langchain_core.prompts import PromptTemplate
import json
from typing import Dict


def jdExtractor(jd)->JDResponse:

    model = ChatOpenAI(
        model="alibaba/tongyi-deepresearch-30b-a3b:free",
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        model_kwargs={"temperature": 0}   # instead of client_kwargs
    ).with_structured_output(JDResponse)

    prompt = PromptTemplate.from_template(
        f"""Instruction: Given the job description , output all the necessary fields in a structured format :

    JOB DESCRIPTION : 
    {jd}
                    
    """
    )
    JD = """

    {jd}
    """

    prompt = prompt.invoke({"JD": JD})

    result = model.invoke(prompt)
 
    return result
