
# The scope of this repository is to provide easy guide to replicate fedprox paper

Link to arxiv paper: [Federated Optimization in Heterogeneous Networks](https://arxiv.org/pdf/1812.06127)

Link to the original code: [litian96/FedProx](https://github.com/litian96/FedProx)


# How to run the code

### Building the docker image

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

### Running the docker image

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

### Running tests automatically

In the patches folder i provided utility scripts to run the tests automatically. 

To test if all is working correctly you can run the following command:
(all commands are to be run inside the docker container in `/root/FedProx` folder)

```bash
./test_run.sh
```

To automatically run all the synthetic tests of the paper you can run the following command:
```bash
./synth_run.sh
```


# Code patches

The original code had a mechanism to gather metrics and save them in a file, but it was incomplete and not working.
I added a patch (which you can find in the `patches` folder) that fixes the issue and allows to save the metrics in a file.
as default the metrics are saved in the `.shared` folder. (this is to easily access the results from the host machine and to work seamlessly with the docker container volume).

### How to create a patch 

To patch a file from the original code you just need to add the new file in the `patches` folder and rebuild the docker image.

for exampl to fix the fedprox trainer you create a file `patches/flearn/trainers/fedprox.py` 
that file will replace the original file `flearn/trainers/fedprox.py` in the original code.

you can also add new files and folders in the `patches` folder and they will be copied in the original code.


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








