import logging
import os
import argparse

from elasticsearch import Elasticsearch

parser = argparse.ArgumentParser(description='configures elastic')
parser.add_argument('--task', '-t', default='setup',
                    choices=['setup', 'delete'],)
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

es = Elasticsearch([os.getenv('ELASTICSEARCH_URL', 'elasticsearch:9200')])

settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
      "purchases": {
        "mappings": {
          "properties": {
            "cart": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "date": {
              "type": "date"
            },
            "purchase_id": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "purchased_products": {
              "properties": {
                "categoryname": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "productbrand": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "productimage": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "productname": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "productprice": {
                  "type": "float"
                },
                "rfid": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                },
                "subcategoryname": {
                  "type": "text",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                      "ignore_above": 256
                    }
                  }
                }
              }
            },
            "state": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "user_id": {
              "type": "long"
            }
          }
        }
      }
    }
}


param = {
    "include_type_name": "true"
}

index_name = 'purchases'

if __name__ == '__main__':
    if args.task == 'setup':
        try:
            if not es.indices.exists(index_name):
                logger.debug(es.indices.create(index=index_name, ignore=400,
                                               params=param,
                                               body=settings))
                logger.info('Created Index')
            else:
                logger.info('Index {} already exists'.format(index_name))
        except Exception as ex:
            logger.error(str(ex))

    elif args.task == 'delete':
        logger.debug(es.indices.delete(index=index_name, ignore=[400, 404]))
        logger.info('Index deleted')
