FROM python:3
RUN mkdir -p ./axonius
WORKDIR /axonius
COPY . .
RUN pip install -r ./requirements.txt
RUN playwright install --with-deps
CMD ["pytest"]