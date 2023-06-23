FROM python:3.10
LABEL authors="Isaque"
RUN pip install --upgrade pip
EXPOSE 5000
WORKDIR /Projeto_Disciplina
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["top", "-b"]