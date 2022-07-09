FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV REQUIREMENTS base.txt
ENV USERNAME bot
ENV PATH "/home/${USERNAME}/.local/bin:${PATH}"

RUN python -m pip install --upgrade pip
RUN useradd -m $USERNAME
USER $USERNAME

COPY --chown=$USERNAME:$USERNAME requirements/$REQUIREMENTS /requirements.txt
RUN python -m pip install --user -r /requirements.txt

ADD --chown=$USERNAME:$USERNAME . /home/$USERNAME/app
WORKDIR /home/$USERNAME/app

CMD ["python", "-m", "znamotobot.bot"]
