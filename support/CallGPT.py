import os
import openai
import re
from dotenv import load_dotenv


def UseGPT(prompt_, type_prompt, boolReal=False):
    if boolReal:
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_KEY")

        message = [{"role": "system", "content": prompt_}]
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=message, temperature=1.0
        )

        answer = response.choices[0].message.content

        if type_prompt == "Prompt_for_image":
            match = re.search(r"PROMPT: (.+)", answer)
            if match:
                answer = match.group(1)
            # else:
            #     print("No PROMPT found in the string.")
        # elif type_prompt == "Prompt_for_instagram":
            # pass
            # current_date = datetime.now()
            # formatted_date = current_date.strftime("%B %d, %Y")

            # print(formatted_date)
            # answer = f"{formatted_date}\n\n{answer}"

    else:
        # current_date = datetime.now()
        # formatted_date = current_date.strftime("%B %d, %Y")
        load_dotenv()
        main_dir = os.getenv("MAIN_DIR")
        if type_prompt == "Prompt_for_image":
            with open(f"{main_dir}/Examples/PromptForImage.txt", 'r') as file:
                answer = file.read()
        elif type_prompt == "Prompt_for_instagram":
            with open(f"{main_dir}/Examples/InstagramCaption.txt", 'r',
                      encoding='utf-8') as file:
                answer = file.read()

    return answer
