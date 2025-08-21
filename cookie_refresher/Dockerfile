FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app
COPY refresh_cookies.py /app/refresh_cookies.py

# Install the playwright Python package and browsers
RUN pip install playwright && playwright install --with-deps

CMD ["python", "/app/refresh_cookies.py"]
