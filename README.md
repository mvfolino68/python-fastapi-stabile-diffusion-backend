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

3. create .env file and update `HUGGINGFACE_API` environment variable. Replace the `<huggingface-api>` text with your own API from Hugging Face. [More information](https://huggingface.co/docs/hub/security-tokens)

   ```bash
   touch .env && echo 'HUGGINGFACE_API=<huggingface-api' > .env
   ```

4. Start the API

   ```bash
   uvicorn main:app --reload
   ```

5. Make Test API Request

   You will see a url displayed in your terminal. Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to try the API.

6. Build a frontend to the API

   `http://127.0.0.1:8000/image/?prompt=${prompt}?negative_prompt=${negativePrompt}&num_inference_steps=${inferenceSteps}`

### Tutorials

todo

### API Reference

todo
