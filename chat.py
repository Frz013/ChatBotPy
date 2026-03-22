import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq

load_dotenv()

roleAI = "kamu adalah AI chatbot yang serba tahu. berikan jawaban dengan teks yang mudah dibaca diterminal tanpa terlalu banyak simbol. buat jawaban menggunakan bahasa Indonesia yang sesuai dengan kaidah kebahansaan Indonesia serta mudah dimengerti dan dipaham."

def askAI(prompt):
    model = 2
    while True:
        user_prompt = prompt
        ai_memory = read_memory()
        contents = "berikut adalah hasil output dari prompt sebelumnya: " + ai_memory + "\nabaikan jika tidak berhubungan dengan prompt saat ini\n" + "prompt saat ini: " + user_prompt

        if model == 1:
            API_Key = os.getenv("GEMINI_API")
            client = genai.Client(api_key= API_Key)

            response = client.models.generate_content(
                model = "gemini-2.5-flash",
                contents = contents,
                config={
                            "temperature": 0.7,
                            "max_output_tokens": 1000,
                            "system_instruction": roleAI,
                        }
                )
            
            hasil_generate = response.text

        if model == 2:
            API_Key = os.getenv("GROQ_API")
            client = Groq(api_key= API_Key)

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                {
                    "role": "system",
                    "content": roleAI
                },
                {
                    "role": "user",
                    "content": contents
                }
                ],
                temperature=0.7,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
                stop=None
            )

            hasil_generate = response.choices[0].message.content
                    
        create_memory(hasil_generate)

        return hasil_generate 


def read_memory():
    try:
        with open("memory.txt", "r") as file:
            content = file.read()
            return content

    except FileNotFoundError:
        return

def create_memory(hasil_output_AI):
    try:
         with open("memory.txt", "w") as file:
            file.write(hasil_output_AI)

    except FileNotFoundError:
        return

if __name__ == "__main__":
    askAI()