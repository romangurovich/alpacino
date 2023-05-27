"""HTTP Inference serving interface using sanic."""
import os

import model
from sanic import Request, Sanic, response

_DEFAULT_PORT = 8000
"""Default port to serve inference on."""
_DEFAULT_NUM_WORKERS = 1
"""Default number of workers to spawn for inference

Typical best practice is to make this number some function 
of the # of CPU cores that the server has access to and should use.
"""


# Load and initialize the model on startup globally, so it can be reused.
model_instance = model.Model()
"""Global instance of the model to serve."""

server = Sanic("server")
"""Global instance of the web server."""


@server.route("/healthcheck", methods=["GET"])
def healthcheck(_: Request) -> response.JSONResponse:
    """Responds to healthcheck requests.

    :param request: the incoming healthcheck request.
    :return: json responding to the healthcheck.
    """
    return response.json({"healthy": True})


@server.route("/predict", methods=["POST"])
def predict(request: Request) -> response.JSONResponse:
    """Responds to inference/prediction requests.

    :param request: the incoming request containing inputs for the model.
    :return: json containing the inference results.
    """
    inputs = request.json
    output = model_instance.predict(inputs)
    return response.json(output)


def main():
    """Entry point for the server."""
    port = int(os.environ.get("SERVING_PORT", _DEFAULT_PORT))
    num_workers = int(os.environ.get("NUM_WORKERS", _DEFAULT_NUM_WORKERS))
    server.run(host="0.0.0.0", port=port, workers=num_workers)


if __name__ == "__main__":
    main()
