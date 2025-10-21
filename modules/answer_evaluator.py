from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from classes_types_dec.structured_outputs import QuestionGenerate
from langchain_core.prompts import PromptTemplate
import json

model = ChatOpenAI(
    model="alibaba/tongyi-deepresearch-30b-a3b:free",
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    model_kwargs={"temperature": 0}   # instead of client_kwargs
).with_structured_output(QuestionGenerate)

prompt = PromptTemplate.from_template(
    """
You are an expert interview agent tasked with generating a comprehensive set of interview questions for a candidate. Your goal is to produce **well-rounded questions** that assess every relevant aspect of the interviewee. Consider the following areas:

1. **Technical Skills** – Assess domain knowledge, problem-solving, coding, and tools relevant to the role.
2. **Soft Skills** – Communication, teamwork, leadership, adaptability, and conflict resolution.
3. **Experience & Background** – Past projects, accomplishments, learning experiences.
4. **Behavioral & Situational** – How the candidate handles challenges, failure, decision-making, and ethical dilemmas.
5. **Cultural Fit & Motivation** – Alignment with company values, long-term goals, work style, and passion for the field.
6. **Creativity & Critical Thinking** – Ability to innovate, think outside the box, and approach problems differently.
7. **Learning & Growth Mindset** – Openness to feedback, learning from mistakes, and self-improvement.

**Instructions:**
- Ensure all the above parameters are covered withing 5 questions
- Ensure a mix of open-ended, scenario-based, and probing questions.
- Avoid simple yes/no questions unless necessary as a lead-in.


Generate the questions now.

JOB DESCRIPTION : 
{JD}
                   
"""
)

with open("./response.json") as f:
    JD = json.dumps(f.read(),indent=2)

prompt = prompt.invoke({"JD": JD})

result = model.invoke(prompt)

print(result)