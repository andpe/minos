FROM debian:latest

RUN apt-get update && apt-get install -y nginx-extras libnginx-mod-nchan

CMD ["nginx", "-g", "daemon off;"]