from pathlib import Path

def add_lib_src_files(vu_inst, uvvm_dir, lib_name, vvc_parent_dir=None, vvc=False):
    parent_dir = vvc_parent_dir if vvc_parent_dir else uvvm_dir
    lib = vu_inst.add_library(lib_name, allow_duplicate=True)
    lib.add_source_files((parent_dir / lib_name/ 'src').glob('*.vhd'))

    if vvc:
        lib.add_source_files((uvvm_dir / 'uvvm_vvc_framework' / 'src_target_dependent').glob('*.vhd'))

    return lib

def add_uvvm_libraries(vu_inst, uvvm_dir, library_list):

    for lib in library_list:
        add_lib_src_files(vu_inst, uvvm_dir, **lib)