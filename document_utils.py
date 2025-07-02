import PyPDF2
import docx

def extract_text_from_files(files):
    texts = []
    for file in files:
        if file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''
            texts.append(text)
        elif file.name.endswith('.docx'):
            doc = docx.Document(file)
            text = '\n'.join([para.text for para in doc.paragraphs])
            texts.append(text)
        elif file.name.endswith('.txt'):
            text = file.read().decode('utf-8')
            texts.append(text)
    return texts 