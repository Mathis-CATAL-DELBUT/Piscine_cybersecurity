NAME = inquisitor
CLIENT_DIR = ./ftp-client/
SERVER_DIR = ./ftp-server/
INQUISITOR_DIR = ./inquisitor/

all: $(NAME)

$(NAME): clean $(CLIENT_DIR)Dockerfile $(SERVER_DIR)Dockerfile $(INQUISITOR_DIR)Dockerfile
		docker compose up --build -d

exec_inquisitor:
		docker exec -it inquisitor /bin/bash

exec_client:
		docker exec -it ftp-client /bin/bash

exec_server:
		docker exec -it ftp-server /bin/bash

clean:
		@if [ -n "$$(docker ps -aq)" ]; then docker stop $$(docker ps -aq); fi
		@if [ -n "$$(docker ps -aq)" ]; then docker rm $$(docker ps -aq); fi

fclean: clean
		@if [ -n "$$(docker images -q)" ]; then docker rmi $$(docker images -q); fi

re: clean all
						
