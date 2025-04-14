from django.http import JsonResponse, HttpRequest
import json
from business.utils.agent_chats import create_chat_func,NoAPIKeyError
from business.utils.reply import fail, success
from django.views.decorators.http import require_http_methods

generual_system_prompt = "You are a helpful assistant."

@require_http_methods(['POST'])
def query_llm(request):
    data = json.loads(request.body)
    llm = data.get('llm') #选择的语言模型名称，比如deepseek-r1, deepseek-v3
    max_tokens = data.get('max_tokens') if data.get('max_tokens') else 2048
    query_content = data.get('query_content') #用户输入的查询语句
    historys = data.get('historys')
    chat_func = create_chat_func(llm) if llm else create_chat_func("deepseek-v3")
    system_prompt = generual_system_prompt
    if historys:
        historys = json.loads(historys)
        historys.append({"role": "user", "content": query_content})
        messages = historys
        print(messages)
    else:
        messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query_content}
                ]
    try:
        response = chat_func(messages=messages, max_tokens=max_tokens,temperature=1.3)
        if(isinstance(response,str)):
            assistant_content = response
        else:
            assistant_content = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_content})
        return success(data={"assistant_content": assistant_content,"historys": json.dumps(messages, ensure_ascii=False, indent=4)}, msg="询问成功")
    except NoAPIKeyError:
        return fail(msg=str("请检查系统环境变量是否有相应的api_key"))
    except Exception as e:
        print(response)
        print(e)
        return fail(msg=str("调用llm发生错误,请检查后端报错信息"))