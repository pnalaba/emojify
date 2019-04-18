FROM centos:7.4.1708

#install SCL (software collections)
RUN yum install -y -d1 centos-release-scl
#install python3
RUN yum install -y -d1 rh-python36

RUN yum install -y -d1 openssl sudo screen git
RUN useradd -rm -d /home/mapr -s /bin/bash -G wheel -p "$(openssl passwd -1 mapr)"  mapr         
USER mapr
WORKDIR /home/mapr
RUN mkdir emojify
WORKDIR /home/mapr/emojify
ADD serve_emojifier.py emojifier_model.tar.gz requirements.txt emo_utils.py run.sh ./

RUN source scl_source enable rh-python36  && pip3 install --user -r requirements.txt
ENV PATH="/home/mapr/.local/bin:${PATH}"
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8
ENV FLASK_APP=serve_emojifier.py

CMD ["bash","./run.sh"]
