FROM registry.baidubce.com/paddlepaddle/paddle:3.2.0-gpu-cuda12.9-cudnn9.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]