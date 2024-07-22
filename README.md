# Facebook Auto Posting Bot

## Overview

This repository contains a bot designed for automating bulk posting on Facebook groups and different accounts using Selenium. The bot supports uploading videos, images, and text posts to multiple groups and accounts. It utilizes cookies for account login to streamline the authentication process.

## Features

- **Bulk Posting**: Post to multiple Facebook groups and accounts simultaneously.
- **Video Uploads**: Upload videos along with text and image posts.
- **Scheduled Posts**: Configure posting schedules to automate updates.
- **Selenium Automation**: Uses Selenium for web automation tasks.
- **Cookie-based Login**: Utilizes cookies to log in to Facebook accounts, avoiding repeated logins.

## Prerequisites

- Python 3.x
- [Google Chrome](https://www.google.com/chrome/) or [Firefox](https://www.mozilla.org/firefox/)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) or [GeckoDriver](https://github.com/mozilla/geckodriver/releases) (matching your browser version)
- Facebook Developer Account
- Facebook App with access token

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/facebook-auto-posting-bot.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd facebook-auto-posting-bot
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Download the appropriate WebDriver:**

    - For Chrome: [ChromeDriver](https://sites.google.com/chromium.org/driver/)
    - For Firefox: [GeckoDriver](https://github.com/mozilla/geckodriver/releases)

    Place the WebDriver executable in a directory included in your system’s PATH or specify its location in the script.

5. **Configure the bot:**

    - Open `config.py` and add your Facebook App credentials, group IDs, and account details.
    - Set up your posting schedule and content.
    - **Setup Cookies**: Save the cookies after a successful login using the script provided and update the `cookies.pkl` file.

### Sample Video
[![asciicast](https://asciinema.org/videos/Video_240716095857.mp4)](https://asciinema.org/a/113463)


## Usage

1. **Save Cookies**: Run the `save_cookies.py` script to log in to Facebook and save your session cookies.

    ```bash
    python save_cookies.py
    ```

    Follow the instructions to log in and save cookies.

2. **Run the bot:**

    ```bash
    python main.py
    ```

3. **Monitor the logs:**

    Check the `logs/` directory for any error messages or status updates.



## Contributing

If you'd like to contribute to the project, please fork the repository and create a pull request with your changes.




