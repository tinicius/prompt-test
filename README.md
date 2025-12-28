# Project Setup and Usage

## Prerequisites

You need to configure some Python packages before running the project. Here is an example using `venv`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

### Environment Variables

1. Export the OpenAI API key:

   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

2. Set the environment variable in a `.env` file:

   ```plaintext
   WEBHOOK_URL=http://localhost:5678/webhook/ai
   ```

### Generate Configuration

Generate the `promptfooconfig.yaml` using the following command:

```bash
python3 ./generate_promptfoo.py data/data.ods
```

Replace `data/data.ods` with the path to your data file if necessary. The table should have the following columns: `input` and `output`.

## Usage

### Run Tests

To run the test set:

```bash
npx promptfoo@latest eval
```

### View Results

To view the results:

```bash
npx promptfoo@latest view -y
```
