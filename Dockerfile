FROM jjonesperez/pucp-madgraph-pythia-delphes:0.7

# Update pip and install requirements
WORKDIR /Collider/

# Install python3
RUN dnf install -y python-is-python3

# Install python packages
RUN python -m venv env \
    && source env/bin/activate \
    && pip install --upgrade pip 

# Pass entrypoint script
COPY entrypoint.sh /Collider/entrypoint.sh
RUN chmod +x /Collider/entrypoint.sh
ENTRYPOINT ["/Collider/entrypoint.sh"]

