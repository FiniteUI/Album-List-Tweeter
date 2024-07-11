#docker stop album-list-tweeter
#docker rm album-list-tweeter

#docker build -f Dockerfile.dockerfile --no-cache . -t album-list-tweeter-image
#docker run --name album-list-tweeter -v album-list-tweeter-data:/app/Data --restart=unless-stopped album-list-tweeter-image

FROM python:3.12-slim

WORKDIR "/app"

COPY .env .
COPY google-api.json .

COPY AlbumListTweets.py .
COPY config.py .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-u", "AlbumListTweets.py"]