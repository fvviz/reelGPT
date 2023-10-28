
import os
from os.path import join, dirname
from dotenv import load_dotenv

from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class ReelSelection:
    def __init__(self, srt_file_path) -> None:
        self.LLM = ChatOpenAI(temperature=0.6, model ='gpt-3.5-turbo-16k', OPENAI_API_KEY=OPENAI_API_KEY)
        with open(srt_file_path) as srt_file:
            self.srt_contents = srt_file.read()
    def get_imp_parts(self):
        response_schemas = [

        #ResponseSchema(name="duration_check", description="Duration of section, make sure this is between 30 and 60 seconds"),
        ResponseSchema(name="start_time", description="The start time of the viral section"),
        ResponseSchema(name="end_time", description="The end time of the viral section, needs to be atleast 30 seconds after start time.")
        #ResponseSchema(name="review", description="why was this section chosen?")
        
    ]
        

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        response_format = output_parser.get_format_instructions()

        pt = PromptTemplate(
        input_variables=["srt_transcript"],
        partial_variables= {"response_format": response_format},
        template ="""s
        You will be given an SRT file which is a transcript of speech/
        Identify the most viral section of the speech that has a duration STRICTLY between 30 and 60 seconds.
        ---
        Transcript in SRT format (hindi):
        {srt_transcript}
        ---
        {response_format}
        """
        )
        chain1 = LLMChain(llm = self.LLM, prompt=pt, 
                                output_key="reel_details"
                            )
        
        out = chain1.run(srt_transcript=self.srt_contents)
        return output_parser.parse(out)



rs = ReelSelection("","./experimental/RG.srt")
print(rs.get_imp_parts())   