# Mini-Rag App

## Overview

This is a simple mini-RAG (Retrieval-Augmented Generation) application that uses the LangChain framework to combine a vector store with a language model. The app allows users to ask questions and receive answers based on the content of a PDF document.

## Features

- Upload a PDF document to the app.
- The app extracts text from the PDF and stores it in a vector store using OpenAI embeddings.
- Users can ask questions, and the app retrieves relevant information from the vector store to generate answers using OpenAI's language model.
- The app provides a simple web interface for interaction.
- The app is built using Streamlit, a popular framework for building web applications in Python.
- The app is designed to be easy to use and understand, making it suitable for educational purposes and quick prototyping.
- The app is designed to be run locally, but can be easily adapted for deployment on cloud platforms or other environments.

- The app is designed to be modular, allowing for easy customization and extension. For example, you can easily swap out the vector store or language model for different implementations.
- The app is designed to be lightweight and efficient, making it suitable for small-scale applications and quick experiments.

- The app is designed to be easily extensible, allowing for the addition of new features and functionality as needed.

## Requirements

- Python 3.7 or higher
- FastAPI
- uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mini-rag-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd mini-rag-app
   ```
3. Create a new conda environment (optional but recommended):

   ```bash
   conda create -n mini-rag python=3.8
   conda activate mini-rag
   pip install -r requirements.txt
   ```

### Usage

1. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your_openai_api_key'
   ```
   Replace `your_openai_api_key` with your actual OpenAI API key.
