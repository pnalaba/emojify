FROM centos/python-36-centos7

#install SCL (software collections)
#RUN yum install -y -d1 centos-release-scl
#install python3
#RUN yum install -y -d1 rh-python36


ADD serve_emojifier.py emojifier_model.tar.gz requirements.txt emo_utils.py run.sh ./

RUN pip install -r requirements.txt
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8
ENV FLASK_APP=serve_emojifier.py

CMD ["bash","./run.sh"]
