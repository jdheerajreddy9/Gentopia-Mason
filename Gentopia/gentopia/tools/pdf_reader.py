import requests
import PyPDF2
from io import BytesIO
from gentopia.tools.basetool import BaseTool

class PDFReader(BaseTool):
    name = "pdf_reader"
    description = "A tool to read and summarize PDFs from a URL or local file."

    def _run(self, **kwargs) -> str:
        filepath = kwargs.get('filepath') or kwargs.get('__arg1')
        if not filepath:
            return "Error: No filepath provided"

        # Check if the input is a URL or a local file
        if filepath.startswith("http://") or filepath.startswith("https://"):
            try:
                response = requests.get(filepath)
                response.raise_for_status()  # Check for HTTP errors
                file_data = BytesIO(response.content)
                reader = PyPDF2.PdfReader(file_data)
            except Exception as e:
                return f"Error reading PDF from URL: {str(e)}"
        else:
            try:
                with open(filepath, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
            except Exception as e:
                return f"Error reading PDF: {str(e)}"

        # Extract and return the content of the PDF
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()

        return pdf_text

    async def _arun(self, **kwargs) -> str:
        raise NotImplementedError("Async reading is not supported.")