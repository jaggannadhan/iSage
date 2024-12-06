import os
import re
from docx import Document
from pdfminer.high_level import extract_text
from langchain.text_splitter import RecursiveCharacterTextSplitter


def parse_cleaned_data(folder_path="Fitness/Fitness_KB_Clean"):
    """
    Parse all supported files in a given folder.
    
    Args:
        folder_path (str): Path to the folder containing files.
        
    Returns:
        dict: A dictionary with filenames as keys and preprocessed text as values.
    """
    supported_formats = ['.txt', '.pdf', '.docx']
    parsed_files = {}
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)
            if ext.lower() in supported_formats:
                raw_text = convert_to_text(file_path)
                preprocessed_text = preprocess_text(raw_text)
                parsed_files[filename] = preprocessed_text
                
    return parsed_files


def convert_to_text(file_path):
    """
    Convert a document to plain text.
    
    Args:
        file_path (str): Path to the uploaded document.
        
    Returns:
        str: Extracted plain text.
    """
    _, ext = os.path.splitext(file_path)
    text = ""
    
    if ext.lower() == '.pdf':
        text = extract_text(file_path)
    elif ext.lower() == '.docx':
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    elif ext.lower() == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        raise ValueError("Unsupported file format.")
    
    return text


def preprocess_text(raw_text):
    """
    Preprocess text by cleaning and normalizing.
    
    Args:
        raw_text (str): Raw extracted text.
        
    Returns:
        str: Preprocessed text.
    """
    # text = raw_text.lower()  # Convert to lowercase
    # text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', raw_text).strip()  # Remove extra spaces
    return text


def split_into_chunks(text, chunk_size=1000, chunk_overlap=500):
    """
    Split text into smaller chunks.
    
    Args:
        text (str): Preprocessed text.
        chunk_size (int): Size of each chunk in tokens.
        
    Returns:
        list: List of text chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)

    return chunks

def process_parsed_files(parsed_files):
    """
    Process parsed files by splitting their text into chunks.
    
    Args:
        parsed_files (dict): Dictionary with filenames as keys and preprocessed text as values.
        
    Returns:
        dict: A dictionary with filenames as keys and lists of text chunks as values.
    """
    chunks_dict = {}
    for filename, text in parsed_files.items():
        chunks = split_into_chunks(text)
        chunks_dict[filename] = chunks
    return chunks_dict
