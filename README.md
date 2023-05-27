# AlPacino

This repo contains a production-grade endpoint for the Alpacino model. It implements a small Sanic webserver to provide inference from the Alpacino model via the the HuggingFace transformers library and packages it up into a dockerfile that can be deployed on your cloud of choice.
The amazing Alapacino model is created by digitous: https://huggingface.co/digitous/Alpacino30b
Template generously provided by OctoML: https://github.com/octoml/octocloud-templates

### Build a Docker image using the Dockerfile
Make sure you are on a GPU instance with at least 180 GB of root storage. This model is a heckin' chonker.

```sh
DOCKER_REGISTRY="XXX" # Put your Docker Hub username here
cd alpacino
docker build -t "$DOCKER_REGISTRY/alpacino30b-pytorch-sanic" -f Dockerfile .
```

### Test the image locally
Run this Docker image locally to test that it can run inferences as expected:

```sh
docker run -d --rm \
    -p 8000:8000 --env SERVER_PORT=8000 \
    --name "alpacino30b-pytorch-sanic"
  	"$DOCKER_REGISTRY/alpacino30b-pytorch-sanic" 
```

..and in a separate terminal run:

```sh
curl -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    --data '{"prompt":"What famous line does Tony Montana say when he enters the courtyard?","max_length":100}'
```

### Push the image to a cloud registry

Push your Docker image to Docker Hub with:
```sh
docker push "$DOCKER_REGISTRY/alpacino30b-pytorch-sanic"
```
