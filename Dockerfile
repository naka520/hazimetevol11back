#Python 3.9のイメージを使用
FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY . .

#pipを使ってpipenvをインストール
RUN pip install --upgrade pip
RUN pip install pipenv

#PipfileとPipfile.lockをコピー
COPY Pipfile Pipfile.lock ./

#依存関係をインストール
RUN pipenv install --system --deploy

#uvicornのサーバーを立ち上げるためのエントリポイントを設定
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]
