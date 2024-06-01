# Using Stockholm

To use Stockholm, follow these steps:

## 1. Installation

- Make sure you have Docker installed on your machine.
- Clone the repository from GitHub.
- Navigate to the project directory: `cd path-to-the-repo`.

## 2. Building and running the Docker container

- Run the `make` command to build and run the Stockholm Docker container.
- You can access the container shell by running `make exec`.

## 3. Using Stockholm

- To generate files, use the `make file` command.
- To encrypt files, use the `python3 stockholm.py` command.
- To decrypt files, use the `python3 stockholm.py -r` command.
- To clean up generated files and docker, use `make clean`.
- To completely remove the Docker environment and files, use `make fclean`.
- To rebuild the project, use `make re`.

## 4. Command line options

Stockholm supports several command line options:
- `-s` or `--silent` to run the program in silent mode.
- `-v` or `--version` to display the Stockholm version.
- `-r` or `--reverse` to decrypt encrypted files.


