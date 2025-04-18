import openai

client = openai.OpenAI(api_key='<pasteKeyHere>')


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


def giveDecriptiveAnswer(text):


    prompt = f"""
    Given the text, return the response by describing it for each field called jira id in the text input
    ```{text}```
    """

    res = get_completion(prompt)
    return str(res)

def get_static_code_analysis(diff) :
    prompt = """
    assume role of a code reviewer
    you will be given a git diff delimited by ``` which contains git diff file

    check the following areas in the code and comment on the code quality
    Null pointer checks
    Proper logs
    Performance impacts
    Readability

    give consise summary of the code quality based on the above pointer in the diff file
    make sure to be specific and give examples

    ```{diff}```
    """

    res = get_completion(prompt)
    return str(res)