import PyPDF2
import os
from pdfminer.high_level import extract_text
from llm_service import OpenAIService


def upload_and_parse_folder(folder_path="KB"):
    """
    Parse all supported files in a given folder.
    
    Args:
        folder_path (str): Path to the folder containing files.
        
    Returns:
        dict: A dictionary with filenames as keys and preprocessed text as values.
    """
    
    total_no_files = len(os.listdir(folder_path))
    llm = OpenAIService()

    for _file_count, filename in enumerate(os.listdir(folder_path), start=1):
        if filename == ".DS_Store":
            continue

        print(f"> Extracting file {_file_count}/{total_no_files}, FileName: {filename}")

        if os.path.exists("KB_Clean/"+filename+".txt"):
            print("File already cleaned!")
            continue

        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            pdf_reader = PyPDF2.PdfReader(file_path)

            total_no_pages = len(pdf_reader.pages)
            for _pg_count, page in enumerate(pdf_reader.pages, start=1):
                print(f">>>> Cleaning page {_pg_count}/{total_no_pages}")
                
                raw_data = page.extract_text()
                cleaned_data = llm.clean_data_from_docs(raw_data)

                with open(f"KB_Clean/{filename}.txt", 'a') as new_file:
                    new_file.write(cleaned_data)


upload_and_parse_folder()
