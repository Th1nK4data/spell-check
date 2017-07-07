FROM python:3

COPY . /usr/src/app
# RUN pip3 install -i http://pypi-sh.emotibot.com:3141/deployer/dev --trusted-host=pypi-sh.emotibot.com -r /usr/src/app/requirements.txt
RUN pip3 install -r /usr/src/app/requirements.txt
# RUN python3 -m compileall /usr/src/app/correction 
# RUN find /usr/src/app/correction -type f -name '*.py' -exec echo {} \; -exec rm {} \;

WORKDIR "/usr/src/app"
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
