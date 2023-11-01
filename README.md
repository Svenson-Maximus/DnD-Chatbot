# D&D Helper Chatbot 🐉

A powerful chatbot designed to aid Dungeon Masters and players in their epic D&D adventures. Using OpenAI's `gpt-3.5-turbo` engine, our chatbot offers fast and dynamic responses to assist with rules, lore, and storytelling.

## Features

- 🎲 Rule clarifications
- 📖 Lore explanations
- 🧙 Character and NPC generation
- 🗺️ World-building suggestions
- 🤖 Seamless integration with both Python and JavaScript

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Integrating the API](#integrating-the-api)
- [License](#license)

## Installation

### Prerequisites

- Python 3.x
- Node.js and npm (for the JavaScript version)

### Steps

1. Clone the repository:
```
git clone https://github.com/Svenson-Maximus/DnD-Chatbot.git
cd DnD-Chatbot
```

Install the Python dependencies, including `python-dotenv`:
```
pip install -r requirements.txt
pip install python-dotenv
```

(For the JavaScript version) Install the necessary npm packages:
```
npm install
```

    
## Usage
### Python
```bash
python dnd_helper.py
```
    
### JavaScript
```bash
npm start
```
    
Follow the on-screen instructions to interact with the chatbot.

## Integrating the API
Create a .env file in the root directory.
Add the following line, replacing YOUR_API_KEY with your actual API key:
```bash
OPENAI_API_KEY=YOUR_API_KEY
```
NOTE: Never commit your API key or make it public!



## License
This project is licensed under the MIT License. 

Crafted with ❤️ by Svenson Maximus. Embark on a journey with us in the fantastical realm of Dungeons & Dragons!

*Note: Always ensure you adhere to OpenAI's use-case policy when leveraging the API for any project.*
