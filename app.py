import google.generativeai as genai
import os
import base64
from dotenv import load_dotenv 

from openai import OpenAI
import fitz


load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=API_KEY)

# API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))





def prep_image(image_path):
    # Upload the file and print a confirmation.
    sample_file = genai.upload_file(path=image_path,
                                display_name="Diagram")
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")
    return sample_file

def extract_text_from_image(image_path, prompt):
    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    # Prompt the model with text and the previously uploaded image.
    response = model.generate_content([image_path, prompt])
    return response.text


# def prep_pdf(pdf_path):
#     sample_file = genai.upload_file(path=pdf_path, display_name="PDF Document")
#     print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
#     file = genai.get_file(name=sample_file.name)
#     print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")
#     return sample_file


# def extract_text_from_pdf(pdf_path, prompt):
#     model = genai.GenerativeModel(model_name="gemini-1.5-pro")
#     response = model.generate_content([pdf_path, prompt])
#     return response.text





# sample_file = prep_image('/home/alignminds/Desktop/Alignminds/Gemini_OCR_Vision/Test_images/Screenshot from 2023-12-29 21-19-10.png') 
# text = extract_text_from_image(sample_file, "Extract the text in the image verbatim")
# if text:
#     print("Extracted Text:")
#     print(text)
# else:
#     print("Failed to extract text from the image.")

# sample_file = prep_image('/home/alignminds/Desktop/Alignminds/Gemini_OCR_Vision/Test_images/Screenshot from 2023-12-29 21-19-10.png') 
# text = extract_text_from_image(sample_file, "Analyze the given diagram and carefully extract the information. Include the cost of the item")
# if text:
#     print("Interpreted Image:")
#     print(text)
# else:
#     print("Failed to extract text from the image.")





sample_file = prep_image('/home/alignminds/Desktop/Alignminds/Gemini_OCR_Vision/extracted_images/page_7.png') 
text = extract_text_from_image(sample_file, "Extract the text in the image. with columns and mapping exact. extract the full text in the image, and make a dictionary with keys name, title and its correct exact values. inside that dictionary that must be the key as  column name as 'D', 'E', 'F' and its correct values. do not give incorrect values to the keys fetch exact the correct vision values")
if text:
    print("Extracted Text:")
    print(text)
else:
    print("Failed to extract text from the image.")

