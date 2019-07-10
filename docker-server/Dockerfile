FROM alpine

RUN apk add --update python3

RUN mkdir /app

WORKDIR /app

COPY . /app


#Add route to UEs address space through the Bridge interface, CHANGE accordingly
CMD ip route add 10.0.2.0/24 via 192.168.1.230 ; ash
