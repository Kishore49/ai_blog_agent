# AI Blog Agent

A Python-based agent that generates blog posts using a HuggingFace LLM and saves them locally.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    - Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env  # On Windows: copy .env.example .env
        ```
    - Edit `.env` and add your keys:
        - `HUGGINGFACEHUB_API_TOKEN`: Get from [HuggingFace Settings](https://huggingface.co/settings/tokens)

## Usage

**Generate and Save**:
```bash
python src/main.py "Your Blog Topic Here"
```
The blog post will be saved to the `output/` directory directly.

**Dry Run (Print to Console)**:
```bash
python src/main.py "Your Blog Topic Here" --dry-run
```
