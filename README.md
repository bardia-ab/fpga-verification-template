# Introduction
This project provides a structured approach for creating verification tests using UVVM and VUnit.
- All RTL files must be stored in `src` directory
- All testbenches files must be stored in `sim` directory
- The `wave.do` must be stored in `sim` directory

```
.
├── config.py
├── ip
├── README.md
├── requirements.txt
├── run.py
├── scripts
│   ├── env.py
│   ├── uvvm_utils.py
│   └── vivado_utils.py
├── sim
├── src
└── vivado_project

```

# Configuration
1. An environment file must be created in the root directory. This file contains the path to the followinf directories:
```
UVVM_DIR=/home/user/UVVM/UVVM
COMPILED_SIM_LIB_DIR=/home/user/compile_simlib/questa
XILINX_GLBL_DIR=/home/user/Xilinx/2025.1
```
2. The following variables in the `config.py` must be set:
    - MODULE_NAME
    - PROJECT_FILE
    - UVVM_LIBRARIES