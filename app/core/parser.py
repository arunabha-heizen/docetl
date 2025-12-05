from docling.document_converter import DocumentConverter
import tempfile
import os

class Parser:
    def __init__(self):
        self.converter = DocumentConverter()

    def parse_file(self, file_path: str) -> str:
        """
        Parses a file using Docling and returns the markdown content.
        """
        result = self.converter.convert(file_path)
        # Docling returns a conversion result which can be exported to markdown
        return result.document.export_to_markdown()
