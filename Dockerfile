FROM jjonesperez/pucp-madgraph-pythia-delphes:0.7

# Set environment variables
ENV PATH=/Collider/ROOT/installROOT/bin/:/Collider/MG5_aMC_v3_1_0/bin/:$PATH
ENV LD_LIBRARY_PATH=/Collider/LHAPDF/lib/:$LD_LIBRARY_PATH
ENV PASSWORD=Feynman2023
ENV PYTHONPATH="${PYTHONPATH}:/Collider/hep_pheno_tools"

# Update pip and install requirements
WORKDIR /Collider/

# Install python3
RUN dnf install -y python-is-python3

# Install python packages
RUN python -m venv env \
    && source env/bin/activate \
    && pip install --upgrade pip 

# Update bashrc
RUN echo "PS1='\[\033[0;32m\]\u \[\033[0;35m\]\w\[\033[0m\]\$ '" >> /etc/bashrc \
    && echo "source /Collider/ROOT/installROOT/bin/thisroot.sh" >> /etc/bashrc \
    && echo "source /Collider/env/bin/activate" >> /etc/bashrc \
    && echo "LD_LIBRARY_PATH=/Collider/LHAPDF/lib/:$LD_LIBRARY_PATH" >> /etc/bashrc \
    && echo 'export PYTHONPATH="${PYTHONPATH}:/Collider/uniandes_framework"' >> /etc/bashrc

# Pass entrypoint script
COPY entrypoint.sh /Collider/entrypoint.sh
RUN chmod +x /Collider/entrypoint.sh
ENTRYPOINT ["/Collider/entrypoint.sh"]

