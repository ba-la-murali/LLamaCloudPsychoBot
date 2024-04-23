 
 
# Llama 2 7B based PsychoBot

## Overview
This repository contains code for a Psychology Bot built using Streamlit and Replicate API. The bot acts as a helpful psychologist, offering compassionate support and guidance to users regarding their mental health and well-being.

## Features
- Seamless integration with Streamlit for building interactive web applications.
- Utilizes Replicate API for generating responses based on user input and context.
- Allows users to interact with the bot by providing prompts and receiving personalized responses.
- Supports multiple Llama2 models for generating responses with varying complexity and accuracy.

## Getting Started
### Prerequisites
- Python 3.10 or later
- Docker (optional, for containerized deployment)

### Installation
1. Clone this repository:
   ```
   git clone https://github.com/your_username/psychology-bot.git
   cd psychology-bot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage
- To run the application locally:
  ```
  streamlit run app.py
  ```
  Access the app via your browser at `http://localhost:8501`.

- To deploy the application using Docker:
  ```
  docker build -t psychology-bot .
  docker run -p 8080:8080 psychology-bot
  ```
  Access the app via your browser at `http://localhost:8080`.

## Configuration
- Set your Replicate API token in the `replicate_api` variable in `app.py`.
- Customize the Streamlit app's appearance and behavior by modifying the code in `app.py`.

 
