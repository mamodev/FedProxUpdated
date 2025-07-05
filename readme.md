
# The scope of this repository is to provide easy guide to replicate fedprox paper

Link to arxiv paper: [Federated Optimization in Heterogeneous Networks](https://arxiv.org/pdf/1812.06127)

Link to the original code: [litian96/FedProx](https://github.com/litian96/FedProx)


# How to run the code

In order to make the code easely to run I created a `DockerFile` that setup everything needed to run the code.
In order to make the docker image works you will need to have `nvida gpu drivers` and `nvidia-container-toolkit` installed on your host machine.

First of all you need to dowload and place the `cudnn` library inside the root of the repository.
The code uses `cuDNN v7.3.0 (Sept 19, 2018), for CUDA 10.0` so you need to download the correct version of it.
You can download it from the nvidia website, but you need to have a nvidia account to download it (free registration).
you can find the link to the archive here: [cuDNN Archive](https://developer.nvidia.com/rdp/cudnn-archive)
if link is not working you can search for "cuDNN Archive" on google and find the updated link.

You need to download the version for linux and ensure that the file is named `cudnn-10.0-linux-x64-v7.3.0.29.tgz` and place it in the root of the repository.

```bash
mv ~/Downloads/cudnn-10.0-linux-x64-v7.3.0.29.tgz ./
```


To build the docker image you can run the following command in the root of the repository:

```bash
docker build -t fedprox .
```

It can be usefull to create persistent storage in order to save the results of tests.
to do this you can create a local folder called .shared 

you can run container with no shared folder with the following command:

```bash
docker run -it --gpus all --rm fedprox
```

or with a shared folder with the following command:

```bash
docker run -it --gpus all --rm -v $(pwd)/.shared:/root/FedProx/.shared fedprox
```

# Notes for manually running the code

The code uses old tensorflow version (1.xx) so is not compatible with any modern version of python.
I tested many version and the one that seams to work is python 3.7.17 and tensorflow 1.15.5.
In order to use such version of tensorflow brotobuf need to be downgraded to 3.20.3.

Inside the `requirements.txt` file you can find the list of packages that need to be installed.

If you do not need gpu support you can install the cpu version of tensorflow you can sobstitute:
`tensorflow-gpu==1.15.5` with `tensorflow==1.15.5`

Notice that in order to run tensorflow 1.15.5 you need to have CUDA 10.0 and cuDNN 7 installed.

The code uses `cuDNN v7.3.0 (Sept 19, 2018), for CUDA 10.0` so you need to download the correct version of it.
You can download it from the nvidia website, but you need to have a nvidia account to download it (free registration).
you can find the link to the archive here: [cuDNN Archive](https://developer.nvidia.com/rdp/cudnn-archive)
if link is not working you can search for "cuDNN Archive" on google and find the updated link.








