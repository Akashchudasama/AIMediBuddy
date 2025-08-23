import fitz  # PyMuPDF
import docx

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        return " ".join(page.get_text() for page in doc)
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    elif file_path.endswith(".txt"):
        with open(file_path, "r") as file:
            return file.read()
    else:
        raise ValueError("Unsupported file type")