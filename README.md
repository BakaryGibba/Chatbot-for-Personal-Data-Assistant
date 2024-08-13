# Chatbot-for-Data-Surmarise
This project is an AI-powered personal data assistant designed to analyze PDF documents and respond to user queries based on the content. It leverages the power of LangChain, Hugging Face models, and Flask to provide an interactive and intelligent user experience.

## Table of Contents
- Features
- Getting Started
  - Prerequisites
  - Installation
  - Running Project
- Project Directory Structure
- Usage
- Contributing
- License
- Acknowledgments

## Features

- **PDF Document Analysis**: Upload a PDF document and get insights and answers based on the content.
- **Natural Language Processing**: Utilizes Hugging Face models to process and understand user queries.
- **Interactive Web Interface**: Built with Flask, offering a user-friendly interface for interaction.
- **Historical Chat Memory**: Maintains a history of the conversation to provide context-aware responses.

## Getting Started

### Prerequisite
Ensure you have the follwoing installed on your local machine:
- Python 3.8 or higher
- Pip
- A Hugging Face API token

### Installation
1. Clone the Repository:
   
            git clone https://github.com/BakaryGibba/personal-data-assistant.git cd personal-data-assistant

2.  Create a Virtual Environment:

        python -m venv venv
        source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install the Required Dependencies:

         pip install -r requirements.txt

4. Set Up Environment Variables:
   Create a **'.env'** file in the root directory and add your Hugging Face API token:

           HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token

## Running the Project
1. **Start the Flask Server:**

           python server.py

2. **Access the Web Interface:**
   Open your web browser and navigate to **'http://127.0.0.1:8000'**

## Project Structure

<img width="532" alt="Screenshot 2024-08-13 221845" src="https://github.com/user-attachments/assets/fdc4fbaf-b319-44f1-96ef-23d25aeaeb1d">
