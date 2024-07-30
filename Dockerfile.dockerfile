# Dockerfile for FUSION: Functional Unit State Identification and Navigation in WSI
#docker build 
FROM python:3.11

LABEL maintainer="Sam Border CMI Lab <samuel.border@medicine.ufl.edu"

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

ENV DSA_URL='https://dsa.rc.ufl.edu'
ENV DSA_USER='suhas'
ENV DSA_PWORD='suhaspassword'

WORKDIR /

RUN git clone https://github.com/spborder/FUSION.git
RUN echo "Listing contents:" && ls -al /

WORKDIR /FUSION
RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN python3 -m pip freeze > pip_installed_packages.txt

EXPOSE 8201

ENTRYPOINT [ "python3" ]
CMD ["FUSION_Main.py"]