#Python 3.9のイメージを使用
FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src

#必要なMySQL依存パッケージをインストール
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    python3-dev

RUN pip install PyJWT
#pipを使ってpoetryをインストール
RUN pip install poetry
RUN pip install --upgrade pip
#poetryの定義ファイルをコピー
COPY pyproject.toml poetry.lock* ./

#poetryの設定を行い、依存関係をインストール前にlockファイルを更新
RUN poetry config virtualenvs.in-project true
RUN poetry update --lock

#依存関係をインストール
RUN poetry install --no-root --no-dev

#uvicornのサーバーを立ち上げるためのエントリポイントを設定
ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]