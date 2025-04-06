import os
from openai import OpenAI, AzureOpenAI
import openai
import backoff
import requests

# 自定义一个名为 CustomError 的错误类型
class NoAPIKeyError(Exception):
    """自定义错误类型，用于特定业务场景"""
    def __init__(self, message="请检查系统环境变量是否有相应的API密钥"):
        self.message = message
        super().__init__(self.message)

def query_agent(syetem_prompt,llm,query):
    pass

def create_chat_func(llm):
    if llm == "deepseek-r1":
        return deepseek_R1_chat()
    elif llm == "deepseek-v3":
        return deepseek_v3_chat()
    else:
        raise NotImplementedError
    
def deepseek_R1_chat():
    deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY") #TODO 请确保环境变量里有deepseek api key
    if not deepseek_api_key:
        raise NoAPIKeyError
    def backoff_hdlr(details):
        print ("Backing off {wait:0.1f} seconds after {tries} tries calling function {target} \
        with args {args} and kwargs {kwargs}".format(**details))
    @backoff.on_exception(
        backoff.constant,
        (openai.RateLimitError, openai.APITimeoutError, openai.APIConnectionError, ValueError),
        interval=5,
        on_backoff=backoff_hdlr
    )
    def chat(messages,temperature=0.5,max_tokens=2048):
        client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # reasoning_content = response.choices[0].message.reasoning_content
        # content = response.choices[0].message.content
        # messages.append({'role': 'assistant', 'content': content}) 
        return response
    return chat

def deepseek_v3_chat():
    deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY") #TODO 请确保环境变量里有deepseek api key
    if not deepseek_api_key:
        raise NoAPIKeyError
    def backoff_hdlr(details):
        print ("Backing off {wait:0.1f} seconds after {tries} tries calling function {target} \
        with args {args} and kwargs {kwargs}".format(**details))
    @backoff.on_exception(
        backoff.constant,
        (openai.RateLimitError, openai.APITimeoutError, openai.APIConnectionError, ValueError),
        interval=5,
        on_backoff=backoff_hdlr
    )
    def chat(messages,temperature=0.5,max_tokens=2048):
        client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response
    return chat

