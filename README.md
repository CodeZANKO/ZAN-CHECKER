# ZAN-CHECKER
# ZAN+ Checker - Universal Account Verification Tool
https://img.shields.io/badge/Python-3.8%252B-blue.svg
https://img.shields.io/badge/GUI-CustomTkinter-green.svg
https://img.shields.io/badge/Web-Automation-orange.svg

A modern, feature-rich account checker application with a beautiful GUI interface built with CustomTkinter. This tool allows you to verify account credentials across multiple popular services including Netflix, Spotify, Steam, Discord, and more.

# Features
+ 🎨 Modern GUI: Beautiful dark/light theme interface with CustomTkinter

+ 🌐 Multi-Platform Support: Check accounts on 10+ popular services

+ ⚡ Dual Checking Methods: Selenium-based browser automation

+ 🔄 Proxy Support: Rotate proxies with various protocol options

+ 📊 Real-time Statistics: Live tracking of valid/invalid accounts

+ 💾 Results Export: Save valid accounts to text files

+ 🔔 Telegram Notifications: Get instant alerts for valid accounts

+ 🎯 Customizable Settings: Adjust threads, timeouts, and delays

+ 🖥️ Cross-Platform: Works on Windows, macOS, and Linux

# Supported Services
+ MidasBuy

+ Netflix

+ Spotify

+ Steam

+ Discord

+ Amazon

+ PayPal

+ Microsoft

+ Apple ID

+ Crunchyroll

# Installation
### Prerequisites
+ Python 3.8 or higher

+ Google Chrome browser

+ Stable internet connection

# Step-by-Step Installation
1. Clone or download this repository

2. Install required dependencies:

```
pip install -r requirements.txt
```
Alternatively, install dependencies manually:


```
pip install customtkinter selenium webdriver-manager requests undetected-chromedriver pillow
```
3. Download ChromeDriver (automatically handled by webdriver-manager)

4. Configure your Telegram bot token and chat ID in the script (optional)

# Usage
1. Launch the application:


```
python zan_checker.py
```
2. Load account combos: Click "Load Combos" and select a text file with email:password combinations

3. Load proxies (optional): Click "Load Proxies" to add proxy support

4. Select target sites: Choose which services to check from the Site Selection tab

5. Configure settings: Adjust threads, timeout, and delay in the Configuration tab

6. Start checking: Click "Start Check" to begin verification

7. Monitor progress: View real-time results in the Results tab

# File Formats
### Combos file format:

Combo.txt
```
email:password
user@example.com:password123
anotheruser@domain.com:pass456
```
### Proxies file format:

Proxies.txt
```
ip:port
192.168.1.1:8080
proxy.example.com:3128
```
# Configuration
## Telegram Notifications
### To enable Telegram notifications:

1. Create a bot using [BotFather] (https://t.me/BotFather)

2. Get your bot token and replace the default one in the code:

python
```
token = 'YOUR_TELEGRAM_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'
```
# Appearance Settings
Customize the application's look and feel:

+ Choose between System, Light, or Dark mode

+ Select from multiple color themes (blue, green, dark-blue)

+ Settings are automatically saved between sessions

# Project Structure

```
zan_checker.py
├── ModernChecker class
│   ├── __init__(): Initialize GUI and variables
│   ├── setup_dashboard_tab(): Main control panel
│   ├── setup_site_selection_tab(): Service selection
│   ├── setup_configuration_tab(): Settings and options
│   ├── setup_results_tab(): Results display
│   ├── check_*_selenium(): Site-specific check methods
│   └── run_check(): Main checking logic
└── SITE_CONFIGS: Configuration for supported services
```
# Disclaimer
This tool is intended for educational purposes and legitimate account verification only. Always ensure you have permission to check any accounts. The developers are not responsible for misuse of this software.

# License
This project is for educational purposes. Please use responsibly and in compliance with all applicable laws and terms of service of the platforms accessed.

# Support
For issues and questions:

Ensure all dependencies are properly installed

Verify your Chrome browser is up to date

Check that your combos file is properly formatted

For proxy issues, verify your proxies are working

# Contributing
Contributions are welcome! Feel free to:

Add support for new services

Improve the GUI/UX

Optimize performance

Enhance error handling

Note: This tool requires technical knowledge to set up and use properly. Users are expected to understand basic Python and web automation concepts.
