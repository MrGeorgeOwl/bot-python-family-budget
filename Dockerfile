FROM python:3.8.6

COPY . ./code
WORKDIR $HOME/code
RUN ["python3", "-m", "pip", "install", "-U", "pip"]
RUN ["python3", "-m", "pip", "install", "-r", "requirements.txt"]
CMD ["python3", "bot/main.py"]
