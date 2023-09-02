FROM python:3.9.13

# TODO: Change user-name
RUN adduser --disabled-password --gecos '' user-name

WORKDIR /opt/core

ARG PIP_EXTRA_INDEX_URL

ADD ./core /opt/core
RUN pip install --upgrade pip
RUN pip install -r /opt/core/requirements.txt

RUN chmod +x /opt/core/run.sh
# TODO: Change user-name and group-name
RUN chown -R user-name:user-name ./

# TODO: Change user-name
USER user-name

EXPOSE 8001

CMD ["bash", "./run.sh"]
