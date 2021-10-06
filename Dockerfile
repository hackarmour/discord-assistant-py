From python:3.9
LABEL maintainer="0xbirdie@gmail.com"

ADD . .
RUN pip install discord.py requests dpymenus disrank numpy pandas discord-components==1.1.4 easy-pil==0.0.2

CMD [ "python3", "./main.py" ]
