from fastapi import FastAPI
from modules.jdanalyzer import jdExtractor
from modules.question_generator import generate_questions
from classes_types_dec.structured_outputs import JDResponse
from pydantic import BaseModel

app = FastAPI()


class ParseJD(BaseModel):
    job_description:str

@app.post("/parse_jd")
def parse_jd(params:ParseJD)->JDResponse:
    return jdExtractor(params.job_description)

@app.post("/generate_questions")
def generate_question_endpoint(params:ParseJD):
    jd_dict = jdExtractor(params.job_description)
    return generate_questions(str(jd_dict))

