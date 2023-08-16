import os

from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    print("OPENAI_API_KEY is not set up")
    raise SystemExit()

# Choose your model between gpt-3, gpt-3.5-turbo, gpt-4
SELECTED_MODEL = os.getenv("SELECTED_MODEL", "gpt-3.5-turbo")


def get_chat_model(temperature: float = 0.7) -> ChatOpenAI:
    return ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name=SELECTED_MODEL,
        temperature=temperature,
    )


template = """Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

{history}
Human: {human_input}
Assistant:"""

prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)


chatgpt_chain = LLMChain(
    llm=get_chat_model(),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=3),
)


def process_chat_message(human_input: str) -> str:
    output = chatgpt_chain.predict(human_input=human_input)
    return output
