from elasticsearch import Elasticsearch
from home import manager
import logging
from django.shortcuts import HttpResponse

ELASTIC_PATH = "http://localhost:9200"
ELASTIC_USERNAME = "hemal"
ELASTIC_PASSWORD = "justradawiwa675a74a'[][wanduawgd78]"

es = Elasticsearch(
    ELASTIC_PATH,
    verify_certs=False,
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD),
)


class ElasticSearch:
    def create_index(index_name, mappings):
        try:
            print("index_name", index_name)
            if index_name and mappings:
                es.indices.create(
                    index=index_name, body={"mappings": {"properties": mappings}}
                )
        except Exception as e:
            print("An error", e)
            manager.create_from_exception(e)
            logging.exception("Something went worng.")
            return HttpResponse("Something went wrong")
