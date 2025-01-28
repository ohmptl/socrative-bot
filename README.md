# Socrative Bot

An AI-powered bot designed to answer Socrative questions automatically.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Technologies Used](#technologies-used)
- [License](#license)

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

## Usage

Run the bot with the following command:

```bash
python main.py
```

### Example

1. Launch the bot and provide your Socrative session details.
2. Watch as the bot automatically answers questions in real-time.

## Configuration

- **AI Model:** Configure the AI model (e.g., OpenAI's GPT, Hugging Face) in the `config.json` file.
- **Socrative Session Details:** Provide session credentials in a secure manner (e.g., environment variables).

Ensure you follow any API usage policies for services used.

## Technologies Used

- **Python**: Core programming language.
- **OpenAI API**: For AI-powered question answering.
- **BeautifulSoup/Selenium**: For web scraping and interaction.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This project is intended for educational purposes only. Ensure compliance with Socrative's terms of service and use responsibly.
