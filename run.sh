sudo docker build --tag=sensor-rest-api .
sudo docker run --net=host -d -p 5000:5000 sensor-rest-api