import os
# import google.generativeai as genai
import openai
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv 
import io
import base64
import re
load_dotenv()

# API_KEY = os.getenv('GOOGLE_API_KEY')
# genai.configure(api_key=API_KEY)

openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))



# def prep_image(image_path):
#     # Upload the file and return the uploaded file object
#     sample_file = genai.upload_file(path=image_path, display_name=os.path.basename(image_path))
#     print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
#     return sample_file

# def extract_text_from_image(image_path, prompt):
#     # Choose the Gemini model
#     model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    
#     # Upload and extract text from image
#     sample_file = prep_image(image_path)
#     response = model.generate_content([sample_file.uri, prompt])
#     return response.text




# def prep_image(image_path):
#     # Upload the file and print a confirmation.
#     sample_file = openai.upload_file(path=image_path, display_name="Image File")
#     print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
    
#     return sample_file


# def extract_text_from_image(image_path, prompt):
#     # Use GPT-4-o model
#     model = openai.GenerativeModel(model_name="gpt-4o-mini-2024-07-18")

#     # Upload the image file
#     sample_file = prep_image(image_path)

#     # Use GPT-4 to generate a response using the image URI and the prompt
#     response = model.generate_content([sample_file.uri, prompt])
    
#     return response.text



def extract_text_from_image(image_path, prompt):
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Open the image file using Pillow
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Convert image to RGB if needed
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")  # Save the image to a bytes buffer
        img_b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8") 

    # Prepare the system message for ChatCompletion
    prompt = (
        "Extract the full text from the image"
        "read all the text and extract all the minute and text from the image."
        "extract the full content like table data and values with corresponding data and values from the image."
        "Extract the correct names and fetch using vision ocr technique."
        "And extract the correct Fields and data from the image."
        "some pages contain different columns and table data. extract with coresponding names and values related to the columns"
        "Extract the text in the image with columns and mapping exact. "
        "Extract the full text in the image, and make a dictionary with keys name, title, and their correct exact values. "
        "Inside that dictionary, there must be the keys as column names 'D', 'E', 'F' and their correct values. "
        "Do not give incorrect values to the keys; fetch the exact correct vision values."
    )

    img_type = "image/png"  # Set the correct image type

    # Prepare the message for ChatCompletion with image data
    response = openai.chat.completions.create(
        model="gpt-4o",  # Use the appropriate model
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{img_type};base64,{img_b64_str}"},
                    },
                ],
            }
        ],
    )
    print("Responce is...",response)
    # Return the extracted text
    if response.choices:
        return response.choices[0].message.content  # Use the attributes correctly
    else:
        return "No content returned from the model."




def natural_sort_key(s):
    """Helper function to sort strings with embedded numbers in a natural way."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]



def extract_text_from_images_in_folder(folder_path, prompt):
    # Dictionary to store the results
    text_extraction_results = {}

    # Iterate over each image in the folder
    for file_name in sorted(os.listdir(folder_path), key=natural_sort_key):
    # for file_name in os.listdir(folder_path):
        # Get the full path of the image
        image_path = os.path.join(folder_path, file_name)
        
        # Ensure it's an image (basic check)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing image: {file_name}")
            print("*"*100)
            
            # Extract text from the image
            extracted_text = extract_text_from_image(image_path, prompt)
            
            # Store the result with the image filename (or page number) as the key
            text_extraction_results[file_name] = extracted_text

    return text_extraction_results





# Example usage
folder_path = "/home/alignminds/Desktop/Alignminds/Gemini_OCR_Vision/Non_Profit_images"
prompt = """Extract the full text from the image.
            read all the text and extract all the minute and text from the image.
            extract the full content like table data and values with corresponding data and values from the image.
            Extract the full text from the image. with columns and mapping exact.
            Extract the correct names and fetch using vision ocr technique.
            some pages contain different columns and table data. extract with coresponding names and values related to the columns
            And extract the correct Fields and data from the image.
            only if the text contains title and name make only that as dictionary rest of the text must be get as text itself.
            extract the full text in the image, and make a dictionary with keys name, title and its correct exact values.
            if the image contains like, Inside that dictionary that must be the key as  column name as 'D', 'E', 'F' and its correct values. 
            Do not give incorrect values to the keys fetch exact the correct vision values"""
extracted_data = extract_text_from_images_in_folder(folder_path, prompt)
print("Extracted data is..",extracted_data)

# Print extracted data
for image, text in extracted_data.items():
    print(f"Image: {image}, Extracted Text: {text}")
