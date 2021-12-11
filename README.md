# [Django 書籍検索](https://django-bookapi.herokuapp.com/)

## デプロイ

[heroku](https://django-bookapi.herokuapp.com/)

## セットアップ

### 楽天 API 発行

https://webservice.rakuten.co.jp/app/create

.env_temp を.env にファイル名変更して APIKEY を設定

### 環境構築

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

### サーバ起動

python manage.py runserver

venv 環境から抜けるときは
deactivate

## 参考

Django 書籍検索システム構築チュートリアル レッスン 1

https://www.youtube.com/watch?v=WvGQ8gmXZgM
