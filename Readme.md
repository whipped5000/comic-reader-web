# comic-reader-web

This is a comic reader that works on cbr and cbz files that are stored on a filesystem.
You will need a docker environment setup to use it. Installing Docker is beyond the scope of this readme.

## Installation

Clone the repository and cd into it.

Create a file called docker-compose.yml using the template below, replacing /local/path/that/has/your/comics/ with the path to your comics directory.

```
version: '3.7'

services:
  web:
    build: ./services/web
    command: gunicorn --bind 0.0.0.0:5000 manage:app
    volumes:
      - ./services/web/:/usr/src/app/
      - /local/path/that/has/your/comics/:/comics/
    ports:
      - 5000:5000
    env_file:
      - ./.env.dev
    restart: unless-stopped

```

Execute the following command (This will take a little while as it compiles Pillow)
```bash
sudo docker-compose build
```

Then to run the container, execute
```bash
sudo docker-compose up -d
```

Browse to http://<server_ip>:5000/ and you should see a directory listing. Use it to select and open a comic in the browser.


## 3rd Party Libraries
Makes use of [PhotoSwipe](https://github.com/dimsemenov/PhotoSwipe)


## License
[MIT](https://choosealicense.com/licenses/mit/)
