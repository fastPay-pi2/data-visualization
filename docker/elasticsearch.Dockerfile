FROM docker.elastic.co/elasticsearch/elasticsearch:7.3.0

RUN mkdir backup

RUN chown -R elasticsearch:elasticsearch backup

# COPY analytics/setup_elastic.py analytics/setup_elastic.py

HEALTHCHECK --interval=5m --timeout=3s  --start-period=40s\
  CMD curl -f http://localhost:9200/ || exit 1