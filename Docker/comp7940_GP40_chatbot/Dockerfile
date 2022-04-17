FROM python:3.7
COPY /app /app
COPY setup.sh setup.sh
RUN pip install pip update
RUN pip install -r /app/requirements.txt
ENV TELE_TOKEN=5181070858:AAGoMSSQGttiakoiKr3He7dhZdw8fw84cEs
ENV MYSQL_USER docker
ENV MYSQL_PWD 123456
ENV MYSQL_HOST mysql
ENV MYSQL_PORT 3306
ENV MYSQL_DB comp7940
CMD ["sh", "setup.sh"]