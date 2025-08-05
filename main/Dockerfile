FROM pytorch/pytorch:2.3.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# One install step
RUN pip install --no-cache-dir \
        transformers accelerate \
        fastapi uvicorn[standard]

# Copy code
COPY chatgpt.py app.py ./

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]