from langchain.output_parsers import OutputFixingParser, PydanticOutputParser
from pydantic import BaseModel

from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 1. .env 파일에서 환경변수 불러오기
load_dotenv()

# 2. 불러온 키 확인 (선택)
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set.")

llm = ChatOpenAI(openai_api_key=openai_api_key)


# 원래의 파서 생성
class EmailSummary(BaseModel):
    person: str
    email: str


pydantic_parser = PydanticOutputParser(pydantic_object=EmailSummary)

# OutputFixingParser로 감싸기
fixing_parser = OutputFixingParser.from_llm(parser=pydantic_parser, llm=llm)

# LLM  응답이 조금 틀렸을 때도 파싱 시도
response = """
{ person: 홍길동, email: hong@example.com} # ' ' 누락 
"""

result = fixing_parser.parse(response)
print(result)  # person='홍길동' email='hong@example.com'
