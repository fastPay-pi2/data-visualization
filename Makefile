up:
	sudo docker-compose up kibana

setup_elastic:
	sudo docker-compose run --rm data-visualization python setup_elastic.py

popula:
	sudo docker-compose run --rm data-visualization python seed_elastic.py