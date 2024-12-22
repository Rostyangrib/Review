FROM python:3.8-slim


COPY . .

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    software-properties-common \
    && apt-get clean

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update && apt-get install -y google-chrome-stable

RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip


COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN pip install selenium webdriver_manager flask bs4





