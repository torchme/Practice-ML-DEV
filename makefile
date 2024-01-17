docker-build:
	docker build -t itmo_case6 -f docker/Dockerfile .
	docker run -p 8000:8000 itmo_case6
