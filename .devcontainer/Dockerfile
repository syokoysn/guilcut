# 公式からpython3.7 on alpine linuxイメージをpull
FROM python:3.7-slim-buster

# 作業ディレクトリを設定
WORKDIR /usr/src/

# 環境変数を設定
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    wget \
    git \
    gnupg2

RUN  pip install \
    pandas \
    selenium \
    beautifulsoup4 \
    boto3 \
    sqlalchemy \
    autopep8 \
    flake8 \
    black
