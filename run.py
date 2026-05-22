from pathlib import Path
from vunit import VUnit

from config import *
from scripts.uvvm_utils import add_uvvm_libraries
from scripts.vivado_utils import (
    add_standard_libraries,
    add_from_compile_order_file,
    generate_compile_order,
)

# -----------------------------------------------------------------------------
# VUnit setup
# -----------------------------------------------------------------------------
vu = VUnit.from_argv()
lib = vu.add_library(LIB_NAME)
# vu.add_com()

# -----------------------------------------------------------------------------
# RTL
# -----------------------------------------------------------------------------
lib.add_source_files((SRC_DIR).glob("*.vhd"))
lib.add_source_files((SRC_DIR).glob("*.v"))

# -----------------------------------------------------------------------------
# Testbench
# -----------------------------------------------------------------------------
lib.add_source_files((TB_DIR).glob("*.vhd"))

# -----------------------------------------------------------------------------
# UVVM
# -----------------------------------------------------------------------------
add_uvvm_libraries(vu, UVVM_DIR, UVVM_LIBRARIES)

# -----------------------------------------------------------------------------
# Vivado IP
# -----------------------------------------------------------------------------
generate_compile_order(PROJECT_FILE, COMPILE_ORDER_FILE)

add_standard_libraries(vu, COMPILED_SIM_LIB_DIR)
add_from_compile_order_file(vu, COMPILE_ORDER_FILE)

# -----------------------------------------------------------------------------
# glbl
# -----------------------------------------------------------------------------
lib.add_source_file(XILINX_GLBL_DIR / "glbl.v")

# -----------------------------------------------------------------------------
# Simulation options
# -----------------------------------------------------------------------------
for tb in lib.get_test_benches(allow_empty=True):
    tb.set_sim_option('modelsim.init_file.gui', WAVE_FILE)
    tb.set_sim_option("modelsim.vsim_flags", VSIM_FLAGS)

vu.main()