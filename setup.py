##setup.py:
from setuptools import setup, find_packages

setup(
    name="pdf_translator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pdf2image",
        "Pillow",
        "opencv-python",
        "opennmt-py",
        "numpy",
        "pytesseract",
        "pdfminer.six"
    ],
    entry_points={
        "console_scripts": [
            "pdf_translator = main:main"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A PDF translator using OCR and deep learning",
    license="MIT",
    keywords="pdf translator ocr deep-learning",
    url="https://github.com/yourusername/pdf_translator",
)
