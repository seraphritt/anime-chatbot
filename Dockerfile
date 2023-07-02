FROM python:3.10
LABEL authors="Isaque, Edgar, Ruan Petrus, Maria Eduarda, Samuel, Davi Fuzo, Rafael Hamu, Luiz Carlos, Moisés"
RUN pip install --upgrade pip
EXPOSE 5000
WORKDIR /Projeto_Disciplina
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["top", "-b"]