From python:3.8
LABEL maintainer="0xbirdie@gmail.com"

ADD . .
RUN apt update && apt install -y ffmpeg
RUN pip install discord.py[voice] requests dpymenus youtube_dl disrank numpy pandas discord-components

CMD [ "python3", "./main.py" ]
