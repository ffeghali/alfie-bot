# AlfieBot - Your Server's Personal Categorization Assistant

## Introduction
Meet **AlfieBot**, our trusty bot named after our lovable pup! Our server is a treasure trove of diverse content, from links and videos to home resources, books, and short-form posts. But how do we keep everything organized? Enter AlfieBot, your go-to **categorization expert** for managing content efficiently within your Discord server.

## Features
- **Categorization of Content**: Helps organize different types of content in the appropriate channels.
- **YouTube Video Summarization**: Uses AI models to provide summaries of YouTube videos.
- **Chat Interactions**: Engages with users through Discord commands.
- **Ollama Model Integration**: Uses the Ollama REST API for processing and classification.

## Future Enhancements
### 1. Implementing Tokenization for Long YouTube Videos
- Testing is underway using a **pretrained model from Hugging Face**.
- This will improve the summarization of long-form YouTube videos.

### 2. Advanced Classification for Categorization
- Users will be able to input a YouTube video using the `/categorize` slash command.
- AlfieBot will automatically post the video in the **most relevant Discord channel**.
- The classification method might leverage **AWS Multi-Agent Orchestrator** ([Multi-Agent Orchestrator](https://awslabs.github.io/multi-agent-orchestrator/)).

### 3. Fine-Tuning the Model
- The classification system may be fine-tuned using approaches like this guide: [Fine-Tuning LLaMA 2 for News Category Prediction](https://medium.com/@kshitiz.sahay26/fine-tuning-llama-2-for-news-category-prediction-a-step-by-step-comprehensive-guide-to-deeccf3e3a88).

## Resources & References
The development of AlfieBot has been inspired and guided by the following resources:
1. **YouTube Tutorial - Part 1**: [Watch Here](https://www.youtube.com/watch?v=Gs7yIMaaPoQ&t=6s)
2. **YouTube Tutorial - Part 2**: [Tweaked Version](https://youtu.be/wU4R9Lj-Mqs?si=o37D0y9_rLKIswc0)
   - Adapted to fit AlfieBot's needs.
   - Implemented a **different tokenization method using Hugging Face** for local execution.
3. **Discord.py Documentation**: [Reference](http://discord.py)
   - Used for setting up the bot with **cogs** and a structured **bot setup**.
4. **Ollama REST API**: [API Docs](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Installation & Setup
### Prerequisites
- Python 3.8+
- A virtual environment
- Dependencies listed in `requirements.txt`
- A Discord bot token

### Steps to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/ffeghali/alfie-bot.git
   cd alfie-bot
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with your **Discord bot token**.
5. Run the bot:
   ```bash
   python app.py
   ```

