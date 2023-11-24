FROM jjonesperez/pucp-madgraph-pythia-delphes:0.7

# Update pip and install requirements
WORKDIR /Collider/

# # Install python3 as default python
# RUN dnf install -y python-is-python3

# Install python packages
RUN python3 -m venv env \
    && source env/bin/activate \
    && pip3 install --upgrade pip 

# Pass entrypoint script
COPY entrypoint.sh /Collider/entrypoint.sh
RUN chmod +x /Collider/entrypoint.sh
ENTRYPOINT ["/Collider/entrypoint.sh"]
