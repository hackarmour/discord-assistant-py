From python:3.9
LABEL maintainer="0xbirdie@gmail.com"

ADD . .
RUN pip install discord.py requests dpymenus youtube_dl disrank numpy pandas discord-components

CMD [ "python3", "./main.py" ]
