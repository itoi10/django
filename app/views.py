from django.shortcuts import render
from django.views.generic import View
from .forms import SearchForm
from django.conf import settings
import json
import requests
from typing import Dict

SEARCH_URL = f"https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId={settings.RAKUTEN_API_APP_ID}"

# 楽天APIコール
def get_api_data(params: Dict[str, str]):
    api = requests.get(SEARCH_URL, params=params).text
    result = json.loads(api)
    items = result["Items"]
    return items


# DjangoのViewはRailsでいうController相当
# 検索ページ
class IndexView(View):
    # GET /
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)
        return render(
            request,
            "app/index.html",
            {
                "form": form,
            },
        )

    # POST /
    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        if form.is_valid():
            keyword = form.cleaned_data["title"]
            params = {
                "title": keyword,
                "hits": 28,  # 検索数
            }
            # 書籍情報取得
            items = get_api_data(params)
            book_data = []
            for i in items:
                item = i["Item"]
                title = item["title"]
                image = item["largeImageUrl"]
                isbn = item["isbn"]
                query = {
                    "title": title,
                    "image": image,
                    "isbn": isbn,
                }
                book_data.append(query)
            # テンプレート描画
            # templateがRailsでいうView相当
            return render(
                request,
                "app/book.html",
                {
                    "book_data": book_data,
                    "keyword": keyword,
                },
            )

        return render(request, "app/index.html", {"form": form})


# 書籍詳細ページ
class DetailView(View):
    # GET detail/<ISBN番号>
    def get(self, request, *args, **kwargs):
        isbn = self.kwargs["isbn"]
        params = {"isbn": isbn}
        # ISBN(国際標準図書番号)で書籍情報取得
        items = get_api_data(params)
        item = items[0]["Item"]

        book_data = {
            "item": item,
            "title": item["title"],
            "image": item["largeImageUrl"],
            "author": item["author"],
            "itemPrice": item["itemPrice"],
            "salesDate": item["salesDate"],
            "publisherName": item["publisherName"],
            "size": item["size"],
            "isbn": item["isbn"],
            "itemCaption": item["itemCaption"],
            "itemUrl": item["itemUrl"],
            "reviewAverage": item["reviewAverage"],
            "reviewCount": item["reviewCount"],
            "average": float(item["reviewAverage"]) * 20,
        }

        return render(
            request,
            "app/detail.html",
            {
                "book_data": book_data,
            },
        )
