@echo off
echo Building Docker image...
docker build -t case2ka-app .

echo Running Docker container...
docker run -d -p 5000:5000 --name case2ka-container case2ka-app

echo Container started. Access the app at http://localhost:5000
echo To view logs: docker logs case2ka-container
echo To stop: docker stop case2ka-container
echo To remove: docker rm case2ka-container