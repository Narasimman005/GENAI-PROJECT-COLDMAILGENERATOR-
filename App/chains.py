import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
load_dotenv()

class Chain:
    def __init__(self):
        self.llm=ChatGroq(
                            model="llama-3.3-70b-versatile",
                            temperature=0,
                            groq_proxy = os.getenv("GROQ_API_KEY")
                            )
    def extract_jobs(self, cleaned_text):
        scrap_template = PromptTemplate.from_template("""
        ### SCRAPED TEXT:
        {scrap}

        ### TASK:
        You are an information extraction assistant.  
        Extract all job postings from the scraped text above.

        ### REQUIRED OUTPUT FORMAT:
        Return a *valid JSON array*.  
        Each job posting must contain exactly these keys:

        - "role"
        - "experience"
        - "skills"
        - "description"

        ### IMPORTANT RULES:
        - Do NOT include any explanation or preamble.
        - Do NOT add extra fields.
        - If some fields are missing, infer if possible or leave them as an empty string.
        - Output ONLY valid JSON.

        ### FINAL OUTPUT:
        Return ONLY the valid JSON.
        """)
        raw = scrap_template | self.llm
        fir_temp = raw.invoke({"scrap": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            json_fir_temp = json_parser.parse(fir_temp.content)
        except Exception:
            raise Exception("Context is very Big")
        if isinstance(json_fir_temp, list):
            return json_fir_temp
        else:
            return [json_fir_temp]

    def write_mail(self, job, links):
        mail_template = PromptTemplate.from_template("""
        ### Job DESCRIPTION:

{job_description}
## INSTRUCTION:

You are Narasimman, a business development executive at Rec. Rec is an AI & Software Consulting company dedicated to facilitating the seamless integration of business processes through automated tools.

Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, process optimization, cost reduction, and heightened overall efficiency.

Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Rec

in fulfilling their needs.

Also add the most relevant ones from the following links to showcase Rec's portfolio: {link_list}

Remember you are Mohan, BDE at Rec.



Do not provide a preamble.

### EMAIL (NO PREAMBLE):
        """)
        email = mail_template | self.llm
        sec_temp = email.invoke({"job_description": str(job), "link_list": links})
        return sec_temp


