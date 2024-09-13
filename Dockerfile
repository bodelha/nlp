FROM rasa/rasa:3.6.20-full

WORKDIR /app

RUN rasa init --no-prompt

COPY . /home/isabela/Projects/NLP

# EXPOSE 5005

# CMD ["rasa", "run"]