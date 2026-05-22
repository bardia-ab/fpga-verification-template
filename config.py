from pathlib import Path

SIM_LIB_PATH = Path("/home/user/compile_simlib/questa")
UVVM_DIR = Path("/home/user/UVVM/UVVM")
XILINX_GLBL_DIR = Path("/tools/Xilinx/2025.1/data/verilog/src")

MODULE_NAME = ""
LIB_NAME = "xil_defaultlib"

ROOT_DIR = Path(__file__).parent

PROJECT_FILE = ROOT_DIR / "vivado_project" / ".xpr"
SRC_DIR = ROOT_DIR / "src"
TB_DIR = ROOT_DIR / "sim"
IP_DIR = ROOT_DIR / "ip"
MODELSIM_CWD = ROOT_DIR / "vunit_out" / "modelsim"
COMPILE_ORDER_FILE = MODELSIM_CWD / "compile_order.txt"
WAVE_FILE = str(TB_DIR / 'wave.do')

VSIM_FLAGS = [
    "-t", "1fs",
    '-voptargs="+acc"',
    "-lib", LIB_NAME,
    f"{LIB_NAME}.glbl"
]

UVVM_LIBRARIES = [
    {"lib_name": "uvvm_util"},
    {"lib_name": "uvvm_vvc_framework"},
    {"lib_name": "bitvis_vip_clock_generator", "vvc": True},
    # {"lib_name": "bitvis_vip_axistream", "vvc": True},
    # {"lib_name": "bitvis_vip_error_injection"},
    # {"lib_name": "ARIA_vip_phase_detector", "vvc_parent_dir": TB_DIR / MODULE_NAME, "vvc": True}
]