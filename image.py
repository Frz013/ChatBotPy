from gradio_client import Client, handle_file
import requests
from bs4 import BeautifulSoup
import uuid
import os

def edit_images():
    prompt = str(input("Masukan Prompt: \n"))
    client = Client("selfit-camera/Omni-Image-Editor")
    try: 
        result = client.predict(
                input_image=handle_file('assets/input_images/kurisu.png'),
                prompt=prompt,
                api_name="/edit_image_interface"
        )
        html_output, status, extra_info = result
        # print(f"Status; {status}\n html result: {html_output}")
        save_images(html_output)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def save_images(html_output, folder_name='output_images'):

    unique_id = uuid.uuid4()
    file_extension = ".png"
    file_name = f"hasil_{unique_id}{file_extension}"
    save_path = os.path.join(f'assets/{folder_name}', file_name)

    soup = BeautifulSoup(html_output, 'html.parser')
    img_tag = soup.find('img')
    img_url = img_tag['src'] if img_tag else None

    response = requests.get(img_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

if __name__ == "__main__":
    edit_images()