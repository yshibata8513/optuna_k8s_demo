FROM ubuntu:20.04
WORKDIR /home/projects

RUN apt-get update && apt-get install -y \
  vim \
  gcc \
  g++ \
  curl

RUN apt install -y python3-pip

RUN pip3 install numpy \
    subprocess.run \ 
    optuna 


COPY closed_test.cpp .
RUN  g++ closed_test.cpp

COPY optuna_test.py .
