IMAGE_URL=bt3101/pii

# builds the image
build:
	docker build -t $(IMAGE_URL):latest .

# starts the development environment
start:
	docker-compose -f ./docker-compose.yml up -V

# starts the service only - use when the service dies within the docker compose network
start_app:
	docker-compose -f ./docker-compose.yml start web

# runs the image in isolation
run:
	docker run -it --rm \
		--publish 5000:80 \
		--volume $$(pwd)/data:/dst \
		$(IMAGE_URL):latest

# rebuilds all the images
reset:
	docker-compose -f ./docker-compose.yml up --build -V

goto_read_db:
	mysql -ureader -ppassword -h127.0.0.1 -P13306 read
goto_write_db_1:
	mysql -uwriter -ppassword -h127.0.0.1 -P23306 write
goto_write_db_2:
	mysql -ushh -ppassword -h127.0.0.1 -P33306 results
