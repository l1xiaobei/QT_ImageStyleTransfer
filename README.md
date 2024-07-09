# QT_ImageStyleTransfer

---

图像风格迁移软件，学校课程大作业。

如遇报错：
```
NVIDIA GeForce RTX 3060 Laptop GPU with CUDA capability sm_86 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_37 sm_50 sm_60 sm_61 sm_70 sm_75 compute_37.
If you want to use the NVIDIA GeForce RTX 3060 Laptop GPU GPU with PyTorch, please check the instructions at https://pytorch.org/get-started/locally/
```
可尝试执行：
- `conda install -c conda-forge cudatoolkit=11.1`  
确保cudatoolkit版本为11.1应当能有效解决问题，可以使用`conda list cudatoolkit`查看版本。