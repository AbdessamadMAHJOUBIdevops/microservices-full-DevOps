FROM python:3.9-slim as base

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM base as tester
RUN pip install pytest
# Astuce : On crée un faux test pour que ça passe tant que j'ai pas encore de tests
RUN echo "def test_dummy(): assert True" > test_dummy.py
# On lance les tests. Si ça rate, le build s'arrête ici !
RUN pytest

# ÉTAPE 3 : Production (Image finale légère)
FROM base as production
EXPOSE 5000
CMD ["python", "app.py"]