FROM pytorch/pytorch

RUN apt-get update
RUN pip install transformers flask

COPY ./api /api

CMD [ "python", "/api/api.py"]

