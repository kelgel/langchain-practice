from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 1. .env 파일에서 환경변수 불러오기
load_dotenv()

# 2. 불러온 키 확인(선택)
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set.")

# parser 객체 생성
parser = CommaSeparatedListOutputParser()

# prompt에 parser의 지침 포함
prompt = PromptTemplate(
    template="다음 주제에 대한 키워드를 쉼표로 나열해줘 : \n주제: {topic}\n\n{format_instructions}",
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# prompt 구성
prompt_value = prompt.format(topic="인공지능")

# llm 호출
llm = ChatOpenAI(openai_api_key=openai_api_key)
output = llm.invoke(prompt_value)

# 파싱
parsed_output = parser.parse(output.content)
print(parsed_output)
