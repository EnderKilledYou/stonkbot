# stonkbot

## Clone or unzip

clone the app (git clone https://github.com/EnderKilledYou/stonkbot/ /app) or just download the zip and unzip it in /app

You can replace /app with any folder it won't matter. Do not change /app in the docker-compose file that references the internal app

## Project start as back ground

```
cd /app (or what ever)
sudo docker-compose up --build -d
```

## Project stop

```
cd /app
sudo docker-compose down
```

Edit
[docker-compose.yml](docker-compose.yml) in /

Set the

```
    volumes:
      - /var/www/html:/app/dist
```

path on the host to where php is served


Edit environment to set what server the python host is on and what port

```dotenv
    environment:
      VUE_APP_PYTHON_HOST_URL: "http://34.72.37.1:5000"
```

This can not be localhost it will need to be domain or ip.

Also if you want to change the port, look up docker-compose port forwarding

it's the line

```dockerfile
"5000:5000"
```

in docker-compose.yml where the first 5000 is the host port and the the second 5000 is the docker port.

You would change the first 5000 to anything like 4444 and then your host will now have port 4444 available on the web,
baring fw. 


