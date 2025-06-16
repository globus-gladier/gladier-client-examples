FROM python:3.12-slim

RUN apt-get update
RUN apt-get install gcc -y
RUN pip install "plotly[express]" kaleido pandas globus-compute-endpoint
RUN pip install tqdm
RUN apt-get clean

# Default command: launch an interactive Python shell.
CMD ["python3"]