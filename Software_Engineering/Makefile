IMAGE_URL=bt3101/pii

build:
	docker build -t $(IMAGE_URL):latest .

run:
	docker run --rm -p 5000:80 $(IMAGE_URL):latest
