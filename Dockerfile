# Dockerfile for FUSION: Functional Unit State Identification and Navigation in WSI
#docker build 
FROM python:3.11

LABEL maintainer="Suhas KC, CMI Lab <katarichalusuhas@ufl.edu>"

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

ENV DSA_URL='https://dsa.rc.ufl.edu/api/v1/'
ENV DSA_USER='suhas'
ENV DSA_PWORD='suhaspassword'

WORKDIR /

RUN git clone -b dsa_hpg https://github.com/SarderLab/FUSION.git
RUN echo "Listing contents:" && ls -al /

WORKDIR /FUSION
RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN python3 -m pip freeze > pip_installed_packages.txt

EXPOSE 8201

ENTRYPOINT [ "python3" ]
CMD ["fusion/FUSION/FUSION_Main.py"]