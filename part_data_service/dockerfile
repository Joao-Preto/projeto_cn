FROM python:3
WORKDIR /run_dir
COPY . /run_dir
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "server.py" ]