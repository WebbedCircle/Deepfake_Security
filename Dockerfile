# --- FILE: Dockerfile ---
FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install flask flask-login pycryptodome
EXPOSE 5000
CMD ["python", "run.py"]
