import os
import requests
from elasticsearch import Elasticsearch, helpers
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)




purchase_api = os.getenv("PURCHASE_API") +  "api/purchase/"
product_api = os.getenv("PRODUCTS_API") +  "product/"
category_endpoint = os.getenv("PRODUCTS_API") + "category/"
subcategory_endpoint = os.getenv("PRODUCTS_API") + "subcategory/"



es = Elasticsearch([os.getenv('ELASTICSEARCH_URL', 'elasticsearch:9200')])


purchase_data = requests.get(purchase_api).json()
# product_data = requests.get(product_api).json()
# category_data = requests.get(category_endpoint).json()
# subcategory_data = requests.get(subcategory_endpoint).json()


def rename_key(iterable, oldkey, newKey):
    if type(iterable) is dict:
        for key in iterable.keys():
            if key == oldkey:
                iterable[newKey] = iterable.pop(key)
    return iterable


if __name__ == '__main__':
    for i, item in enumerate(purchase_data):
        try:
            item = rename_key(item, '_id', 'purchase_id')
            purchase_data[i] = item
            purchase_data[i]['date'] = datetime.strptime(purchase_data[i]['date'],
                                                        '%Y-%m-%d  %H:%M:%S.%f').strftime('%Y-%m-%d')
            res = es.index(index='purchases',doc_type='all_purchases',
                        body=item)
        except ValueError:
            purchase_data[i]['date'] = datetime.strptime(purchase_data[i]['date'],
                                                        '%Y-%m-%d  %H:%M:%S').strftime('%Y-%m-%d')
            res = es.index(index='purchases',doc_type='all_purchases',
                        body=item)
        # logging.info(res)