# Usa una imagen oficial de Python como base
FROM python:3-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del microservicio (incluyendo main.py y la carpeta app)
COPY . .

# Expone el puerto en el que correrá la app (FastAPI por defecto usa 8000)
EXPOSE 8000

# Comando para iniciar el servidor Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
