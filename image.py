from gradio_client import Client, handle_file
import requests
from bs4 import BeautifulSoup
import uuid
import os
import io

def edit_images(user_prompt, user_images):
    client = Client("selfit-camera/Omni-Image-Editor")
    try: 
        result = client.predict(
                input_image=handle_file(user_images),
                prompt= user_prompt,
                api_name="/edit_image_interface"
        )
        html_output, status, extra_info = result

        soup = BeautifulSoup(html_output, 'html.parser')
        img_tag = soup.find('img')
        img_url = img_tag['src'] if img_tag else None

        response = requests.get(img_url)
        edit_result = io.BytesIO(response.content)
        edit_result.seek(0)
        return edit_result, img_url
    
    except Exception as e:
        return 

def save_images(html_output, folder_name='output_images'):

    unique_id = uuid.uuid4()
    file_extension = ".png"
    file_name = f"hasil_{unique_id}{file_extension}"
    save_path = os.path.join(f'assets/{folder_name}', file_name)

    soup = BeautifulSoup(html_output, 'html.parser')
    img_tag = soup.find('img')
    img_url = img_tag['src'] if img_tag else None

    response = requests.get(img_url)

    # with open(save_path, 'wb') as file:
    #     file.write(response.content)
    

if __name__ == "__main__":
    edit_images()