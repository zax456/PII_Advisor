IMAGE_URL=bt3101/pii

build:
	docker build -t $(IMAGE_URL):latest .

run:
	docker run -it --rm \
		--publish 5000:80 \
		--volume $$(pwd)/data:/dst \
		$(IMAGE_URL):latest
