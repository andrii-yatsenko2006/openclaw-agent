import os

# Using try-except for imports ensures the app won't crash
# if a specific document library is missing on another machine.
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    import docx
except ImportError:
    docx = None

class DocumentReader:
    """
    Reads text from various document formats (.txt, .pdf, .docx).
    Acts as the 'Document Eyes' for the agent.
    """
    def __init__(self):
        pass

    def read_file(self, file_path: str) -> str:
        """
        Detects the file type based on its extension and extracts text from it.
        Returns the extracted text or an error message.
        """
        if not os.path.exists(file_path):
            return f"Error: File not found at path '{file_path}'."

        # Extract the file extension (e.g., '.pdf')
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        try:
            if ext == '.txt':
                return self._read_txt(file_path)
            elif ext == '.pdf':
                return self._read_pdf(file_path)
            elif ext in ['.doc', '.docx']:
                return self._read_docx(file_path)
            else:
                return f"Error: Unsupported file extension '{ext}'. Only .txt, .pdf, and .docx are supported."

        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"

    def _read_txt(self, file_path: str) -> str:
        """Reads plain text files."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _read_pdf(self, file_path: str) -> str:
        """Reads PDF files using pypdf."""
        if PdfReader is None:
            return "Error: 'pypdf' library is not installed."

        reader = PdfReader(file_path)
        text = ""
        # Iterate through all pages and concatenate the text
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    def _read_docx(self, file_path: str) -> str:
        """Reads Microsoft Word documents using python-docx."""
        if docx is None:
            return "Error: 'python-docx' library is not installed."

        doc = docx.Document(file_path)
        # Extract text from each paragraph and join with newlines
        text = [paragraph.text for paragraph in doc.paragraphs]
        return "\n".join(text).strip()