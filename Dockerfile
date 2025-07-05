# link provided by https://developer.nvidia.com/ 
# if any error occurs, please update link manually

FROM    ubuntu:18.04
LABEL   description =    "FedProx Docker image with CUDA and NVIDIA drivers"
LABEL   maintainer  =     "@mamodev"

ARG     CUDA_VERSION=10.0.130
ARG     NVIDIA_DRIVER_VERSION=410.48
ARG     PYTHON_VERSION=3.7.17

ENV     CUDA_SHORT_VERSION=10.0
ENV     DEBIAN_FRONTEND=noninteractive

# CORE 
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
    git \
    ca-certificates 

# download NVIDIA toolkit
RUN wget  https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda_10.0.130_410.48_linux

# install NVIDIA toolkit
RUN sh ./cuda_10.0.130_410.48_linux \
        --silent \
        --toolkit \
        --toolkitpath="/usr/local/cuda-10.0" \
        --samples \
        --samplespath="/usr/local/cuda-10.0/samples" \
        --override

# install NVIDIA path
RUN echo "export PATH=/usr/local/cuda-10.0/bin:\$PATH" >> /etc/bash.bashrc && \
    echo "export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64:\$LD_LIBRARY_PATH" >> /etc/bash.bashrc && \
    echo "export CUDA_HOME=/usr/local/cuda-10.0" >> /etc/bash.bashrc 

ENV PATH="/usr/local/cuda-10.0/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda-10.0/lib64:${LD_LIBRARY_PATH}"
ENV CUDA_HOME="/usr/local/cuda-10.0"

RUN nvcc --version

# PYENV DEPS
RUN apt-get install -y --no-install-recommends \
    zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev \
    tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    libncursesw5-dev libgdbm-dev libnss3-dev uuid-dev xz-utils  libssl-dev 


RUN curl https://pyenv.run | bash 

RUN echo 'export PYENV_ROOT="/root/.pyenv"' >> /etc/profile.d/pyenv.sh && \
    echo 'export PATH="/root/.pyenv/bin:$PATH"' >> /etc/profile.d/pyenv.sh && \
    echo 'eval "$(pyenv init --path)"' >> /etc/profile.d/pyenv.sh && \
    echo 'eval "$(pyenv init - bash)"' >> /etc/profile.d/pyenv.sh && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> /etc/profile.d/pyenv.sh && \
    chmod +x /etc/profile.d/pyenv.sh

SHELL ["/bin/bash", "-lc"]
RUN pyenv install $PYTHON_VERSION && \
    pyenv global $PYTHON_VERSION && \
    pyenv rehash


COPY ./cudnn-10.0-linux-x64-v7.3.0.29.tgz /tmp/cudnn.tgz
RUN cd /tmp && tar -xf /tmp/cudnn.tgz && cp -P cuda/include/* /usr/local/cuda-10.0/include/ &n& cp -P cuda/lib64/* /usr/local/cuda-10.0/lib64/ && \
    rm -rf /tmp/cudnn.tgz /tmp/cuda


# create python virtual environment
COPY requirements.txt /root/requirements.txt

RUN cd /root &&  python3 -m venv .venv && \
     echo "source /root/.venv/bin/activate" >> /etc/bash.bashrc && \
     echo "export VIRTUAL_ENV=/root/.venv" >> /etc/bash.bashrc && \
     source .venv/bin/activate && \
     pip install -r ./requirements.txt

RUN git clone https://github.com/litian96/FedProx.git /root/FedProx && chmod +x /root/FedProx/run_fedavg.sh &&  chmod +x /root/FedProx/run_fedprox.sh

CMD ["/bin/bash", "-c", "source /root/.venv/bin/activate && cd /root/FedProx && exec bash"]