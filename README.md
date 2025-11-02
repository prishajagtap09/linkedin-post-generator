# 🤖 LinkedIn Post Generator

This project is a web application built with Streamlit that generates custom LinkedIn posts using AI. Users can select a topic, desired post length, and language (English or Hinglish), and the app will use a Large Language Model (via Groq) to create a new post.

This app also includes a data preprocessing pipeline that reads raw JSON posts, uses an LLM to extract and unify metadata (like tags), and saves the processed data to be used by the main application.

## ✨ Features

* **Interactive Web UI:** Built with Streamlit for a simple and clean user interface.
* **Dynamic Topics:** Select from a list of topics (e.g., "Job Search", "Motivation", "Scams") that are dynamically pre-processed from a JSON data file.
* **Customizable Output:** Choose the desired post length (Short, Medium, Long) and language (English or Hinglish).
* **Fast AI Generation:** Generates content using the high-speed Llama 3.1 model via the Groq API.

## 🛠️ Technologies Used

* **Python**
* **Streamlit:** For the web application interface.
* **LangChain:** For prompt templates and interacting with the LLM.
* **Groq:** For access to the Llama 3.1 LLM.
* **python-dotenv:** For managing the API key.

📂 File Structure
.
├── data/
│   ├── raw_posts.json        # Your raw input data
│   └── processed_posts.json  # The cleaned & enriched output data
├── .env                      # (To be created) Stores your secret API key
├── .gitignore                # Tells Git to ignore venv, .env, etc.
├── llm_helper.py             # Configures and exports the Groq LLM
├── few_shots.py              # Reads processed_posts.json to get tags
├── main.py                   # The main Streamlit application
├── preprocess.py             # Script to process the raw JSON data
└── README.md                 # This file