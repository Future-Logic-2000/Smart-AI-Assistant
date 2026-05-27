# Tiny Assistant (Online)

**Tiny Assistant** is a lightweight, smart AI programming assistant built with **Python** using a modern user interface provided by the **CustomTkinter** library. It is cloud-connected to the **Gemini 2.5 Flash** model to deliver instant programming solutions and explanations.

---

## Features

- **Full Multi-Language Support:** Efficiently supports Arabic, English, and other languages with automatic text direction adjustment (RTL/LTR) to prevent text and number overlap.
- **Smart and Exceptional Formatting:** Processes text to convert Markdown syntax into bold headers and clean bulleted lists, ensuring a clean appearance free of broken markdown symbols.
- **Code Reviewer and Fixer:** Allows direct uploading of code files to inspect them in the cloud, fix errors, and provide comprehensive explanations.
- **Simplified Chat Memory:** Retains conversational context during the session to provide consistent and logical responses.

---

## Tech Stack

- **Language:** Python 3.x
- **GUI Library:** CustomTkinter (Dark Mode Theme)
- **AI Engine:** Google Generative AI (Gemini 2.5 Flash API)
- **Regex Processing:** Built-in re module for advanced text and language detection.

---

## How to Run

1. Clone the repository to your local machine:
2. Do not share your API key with anyone, including other AI models.
3. Install the required dependencies:  pip install customtkinter google-generativeai
4. Open the code and set your private API key in the api_key_from_system variable.
5. Run the application:python main.py
   ```bash
   git clone [https://github.com/Future-Logic-2000/Future-Logic.git](https://github.com/Future-Logic-2000/Future-Logic.git)
##Application Preview
1. The application runs within a clean, dark-themed user interface designed for a comfortable visual experience. It includes:
2. A smart text box that renders responses in a neat and smooth format.
3. A quick input entry field supporting both the Submit button and the Upload File button.
