# Dockerfile

FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Install Python & dependencies
RUN apt-get update && apt-get install -y \
    git python3 python3-pip && \
    pip3 install --upgrade pip

# Install vLLM
RUN pip install vllm

# Download model (optional at runtime) - Downloading a model during build makes the image much bigger and slower to build.
# RUN python3 -c "from vllm import LLM; LLM(model='gpt2')"

# Expose port for API
EXPOSE 9000

# Run vLLM with GPT-2 on startup
CMD ["python3", "-m", "vllm.entrypoints.openai.api_server", "--model", "gpt2", "--host", "0.0.0.0", "--port", "9000"]
