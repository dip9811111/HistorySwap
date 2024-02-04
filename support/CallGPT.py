import openai
import re
from datetime import datetime
from general.predefined_strings import OPEN_AI_KEY, MAIN_DIR


def UseGPT(prompt_, type_prompt, year=None, boolReal=False):
    if boolReal:
        openai.api_key = OPEN_AI_KEY

        message = [{"role": "system", "content": prompt_}]
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=message, temperature=1.0
        )

        answer = response.choices[0].message.content

        if type_prompt == "Prompt_for_image":
            match = re.search(r"PROMPT: (.+)", answer)
            if match:
                answer = match.group(1)

        elif type_prompt == "Prompt_for_instagram":
            current_date = datetime.now()
            formatted_date = current_date.strftime("%B %d")
            formatted_date = f"{formatted_date}, {year}"
            answer = f"{formatted_date}\n\n{answer}"

    else:
        if type_prompt == "Prompt_for_image":
            with open(f"{MAIN_DIR}/Examples/PromptForImage.txt", 'r') as file:
                answer = file.read()
        elif type_prompt == "Prompt_for_instagram":
            with open(f"{MAIN_DIR}/Examples/InstagramCaption.txt", 'r',
                      encoding='utf-8') as file:
                answer = file.read()

    return answer
