from fastapi import FastAPI
from modules.jdanalyzer import jdExtractor
from modules.question_generator import generate_questions
from classes_types_dec.structured_outputs import JDResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from modules.text2speech import convert_to_speech
app = FastAPI()

origins = ["*","http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ParseJD(BaseModel):
    job_description:str

@app.post("/parse_jd")
def parse_jd(params:ParseJD)->JDResponse:
    return jdExtractor(params.job_description)

@app.post("/generate_questions")
def generate_question_endpoint(params:ParseJD):
    jd_dict = jdExtractor(params.job_description)
    return generate_questions(str(jd_dict))

class Text2Speech(BaseModel):
    question_text:str
    experience:int

@app.post("/generate_audio")
def generate_audio(params:Text2Speech):
    audio_filename = convert_to_speech(params.question_text)
    return FileResponse(
        path = f"./{audio_filename}"
    )
