# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.6-slim



# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
RUN mkdir ./ncp-app
WORKDIR /ncp-app
RUN pip install --upgrade pip


# Install pip requirements
COPY requirements.txt ./ncp-app
RUN pip install -r requirements.txt


COPY . /ncp-app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found. Please enter the Python path to wsgi file.
EXPOSE 8000
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pythonPath.to.wsgi"]
CMD ["python", "manage.py","runserver","0.0.0.0:8000"]
