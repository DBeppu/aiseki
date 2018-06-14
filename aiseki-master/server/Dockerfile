FROM amazonlinux:2

ADD crawl.py .
RUN amazon-linux-extras install python3
RUN yum install -y gcc python3-devel lxml libxml2-devel libxslt1-devel python3-dev python3-lxml 
RUN pip3 install lxml
RUN pip3 install requests
RUN pip3 install boto3
RUN pip3 install beautifulsoup4

ENTRYPOINT python3 crawl.py
