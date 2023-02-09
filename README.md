# Python FastAPI backend for Stable Diffusion

Example of an API for Stable Diffusion inference using FastAPI and Hugging Face.

## Documentation

- [Python FastAPI backend for Stable Diffusion](#python-fastapi-backend-for-stable-diffusion)
  - [Documentation](#documentation)
    - [Installing](#installing)
    - [Tutorials](#tutorials)
    - [API Reference](#api-reference)

### Installing

1. Clone the repository locally

   ```bash
   git clone git@github.com:mvfolino68/python-fastapi-stabile-diffusion-backend.git
   ```

2. Create a virtual environment for Python and activate it. Install requirements

   ```bash
   python3 venv -m api
   source api/bin/activate
   pip install -r requirements.txt
   ```

3. create .env file using the `.env.example` provided. 
   1. Create an API key from Hugging Face. [More information](https://huggingface.co/docs/hub/security-tokens)
      1. paste the API key into the environment file.
   2. Sign up for a free MongoDB account, create a cluster, database and collection. [More information](https://www.mongodb.com/docs/atlas/)
      1. paste the connection values into the environment file.


4. Start the API

   ```bash
   uvicorn image.main:app --reload --lifespan=on --use-colors --loop uvloop --http httptools
   ```

5. Make Test API Request

   You will see a url displayed in your terminal. Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to try the API.

6. Make a request to the API

   ```bash
   curl --location --request POST 'http://localhost:8000/api/v1/image-generator' \
   --header 'Content-Type: application/json' \
   --data-raw '{
   "prompt": "this is a sample image prompt",
   "num_inference_steps": 0,
   "negative_prompt": "this is a sample for a negative image prompt."
   }'
   ```

[Image prompt help](https://towardsdatascience.com/a-beginners-guide-to-prompt-design-for-text-to-image-generative-models-8242e1361580)

### Tutorials

todo

### API Reference

todo
