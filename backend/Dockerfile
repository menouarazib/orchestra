FROM python:3.10-alpine
RUN apk update
RUN apk add git
ENV GIT_PYTHON_REFRESH=quiet
ENV PYTHONUNBUFFERED=1

WORKDIR /orchestra/backend
# Copy app files
COPY . .
# ==== Install =====
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
