#!/bin/sh

echo "Building image..."
echo "=================================================================================="
echo " "

docker image build -t $docker_registry/$path/$image_name $path_to_dockerfile

echo " "
echo "Build done!"
echo " "

echo "Uploading to docker registry"
echo "=================================================================================="
echo " "

docker push $docker_registry/$path/$image_name

echo " "
echo "Push latest done!"
echo " "
