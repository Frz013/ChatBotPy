import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq
import string

load_dotenv()

roleAI = "kamu adalah AI terminal yang serba tahu. berikan jawaban dengan teks yang mudah dibaca diterminal tanpa terlalu banyak simbol. buat jawaban menggunakan bahasa Indonesia yang sesuai dengan kaidah kebahansaan Indonesia serta mudah dimengerti dan dipahami"

def main():
    model = int(input("Pilih model AI yang akan digunakan:\n1. Gemini\n2. Ollama\nPilihan model: "))
    while True:
        user_prompt = get_user_prompt() 
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
                    
        print("Loading...\n\n")
        output(hasil_generate)
        create_memory(hasil_generate)


def read_memory():
    try:
        with open("memory.txt", "r") as file:
            content = file.read()
            return content

    except FileNotFoundError:
        print("The file was not found.")

def create_memory(hasil_output_AI):
    try:
         with open("memory.txt", "w") as file:
            file.write(hasil_output_AI)

    except FileNotFoundError:
        print("The file was not found.")

def get_user_prompt():
    prompt = str(input("\n\nMasukan Prompt: "))
    return prompt

def output(hasil_generate):
    hasil = print(hasil_generate)

if __name__ == "__main__":
    main()