FROM continuumio/miniconda3

# Copy minimal files required for installing dependencies
COPY ../dependencies/release/requirements.txt dependencies/release/constraints.txt /app/
COPY ../pyproject.toml setup.py /app/

# Install dependencies
RUN mkdir src && pip install --no-cache-dir -e . -r requirements.txt -c constraints.txt

# Then copy other files that are more frequently updated
COPY ../src /app/src/