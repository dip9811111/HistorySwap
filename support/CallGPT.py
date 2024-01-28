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

        return answer
    else:
        # current_date = datetime.now()
        # formatted_date = current_date.strftime("%B %d, %Y")
        if type_prompt == "Prompt_for_image":
            answer = """Generate an image depicting Vegeta from DragonBall declaring "Total War" against the Allies in a dramatic and intense setting. Capture the essence of Vegeta's character as he takes on a leadership role similar to Adolf Hitler, showcasing his determination and power in the midst of the conflict. Ensure the visual elements convey the intensity of this alternate scenario, blending Vegeta's iconic traits with the historical context of a total war declaration against the Allies."""
        elif type_prompt == "Prompt_for_instagram":
            answer = """This is the caption of instagram"""
        # answer = f"{formatted_date}\n\n{answer}"
        return answer
