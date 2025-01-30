# Socrative Bot

An AI-powered bot designed to answer Socrative questions automatically.

## Table of Contents

- [Example](#example)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Disclaimer](#disclaimer)

### Example

1. Launch the bot and provide your Socrative session details.
2. Watch as the bot automatically answers questions in real-time.

## Technologies Used

- **Python**: Core programming language.
- **Gemini API**: For AI-powered question answering.
- **Selenium**: For web scraping and interaction.

## Installation

To get started with the Socrative Bot, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/ohmptl/socrative-bot.git
   cd socrative-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the necessary API keys or configuration files as described in the [Configuration](#configuration) section.

## Configuration

You'll need to set up a few environment variables:

* `ROOM_NAME`: Your Socrative room.
* `STUDENT_NAME`: Your name as per instructor guidelines.
* `GEMINI_API_KEY`: The Gemini API Key to run the AI.
* `POLLING_INTERVAL`: The polling rate of the bot (default is 5).
* `LOG_FILE`: The complete filepath to where you want your log to be saved

Do this by creating a `.env` file in the root of the project as follows:

```env
ROOM_NAME=
STUDENT_NAME=
GEMINI_API_KEY=
POLLING_INTERVAL=
LOG_FILE=
```

Ensure you follow any API usage policies for services used.

## Usage

Run the bot with the following command:

```bash
python main.py
```

## Disclaimer

This project is intended for educational purposes only. 
The creators of this software are not responsible or liable for any illegal, unethical, or violative activities conducted using this tool. 
By using this software, you agree to comply with all applicable laws and Socrative's terms of service. 
This tool is not intended to be used for cheating, academic dishonesty, or any other form of misconduct. 
Use responsibly and at your own risk.
