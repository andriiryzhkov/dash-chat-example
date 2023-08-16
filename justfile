set dotenv-load := false

# Create a new python environment
venv:
    python -m venv venv
    . venv/bin/activate

# Install  pip requirements.
install:
    pip install -r requirements.txt

# Run Dash app locally
run:
    python app.py
