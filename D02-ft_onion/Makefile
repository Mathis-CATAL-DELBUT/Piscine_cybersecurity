NAME = onion

all: $(NAME)

$(NAME):
			docker build -t onion_image .
			docker run -d -p 4243:4242 --name onion_run onion_image

ssh:
			ssh root@localhost -p 4243

exec:
			docker exec -it onion_run /bin/bash

key:
			ssh-keygen -f "/mnt/nfs/homes/mcatal-d/.ssh/known_hosts" -R "[localhost]:4243"

fclean:
			if [ $$(docker ps -aq) ]; then docker stop $$(docker ps -aq); fi
			if [ $$(docker ps -aq) ]; then docker rm $$(docker ps -aq); fi
			if [ $$(docker images -q) ]; then docker rmi $$(docker images -q); fi
			docker system prune -af



re : 	fclean $(NAME)

.PHONY: all clean re
