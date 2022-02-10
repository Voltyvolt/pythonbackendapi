#Dockerfile, Images, Container
FROM python:3.10.2
ADD app.py .
RUN pip install Flask werkzeug mysql-connector-python --upgrade
RUN pip install flask-cors --upgrade
RUN set FLASK_ENV=development
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"]