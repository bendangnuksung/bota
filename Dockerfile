# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.6
COPY . /dotabot
WORKDIR /dotabot
ENTRYPOINT ["python3"]
CMD ["main.py"]