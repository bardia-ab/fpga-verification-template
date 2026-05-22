from pathlib import Path
from vunit_vivado.vivado import create_compile_order_file

def generate_compile_order(project_file, compile_order_file):
    compile_order_file.parent.mkdir(exist_ok=True, parents=True)
    if not compile_order_file.exists():
        create_compile_order_file(project_file, compile_order_file)

def read_compile_order(file_name, fail_on_non_hdl_files):
    """
    Read the compile order file and filter out duplicate files
    """
    compile_order = []
    unique = set()
    include_dirs = set()
    libraries = set()

    with Path(file_name).open("r", encoding="utf-8") as ifile:
        for line in ifile.readlines():
            library_name, file_type, file_name = line.strip().split(",", 2)

            if file_type not in ("Verilog", "VHDL", "VHDL 2008", "Verilog Header"):
                if fail_on_non_hdl_files:
                    pass
                    # raise RuntimeError(f"Unsupported compile order file: {file_name}")
                print(f"Compile order file ignored: {file_name}")
                continue

            libraries.add(library_name)

            # Vivado generates duplicate files for different IP:s
            # using the same underlying libraries. We remove duplicates here
            key = (library_name, Path(file_name).name)
            if key in unique:
                continue
            unique.add(key)

            if file_type == "Verilog Header":
                include_dirs.add(str(Path(file_name).parent))
            else:
                compile_order.append((library_name, file_name))

    return compile_order, libraries, list(sorted(include_dirs))

def add_from_compile_order_file(
    vunit_obj, compile_order_file, dependency_scan_defaultlib=True, fail_on_non_hdl_files=True
):  # pylint: disable=too-many-locals
    """
    Add Vivado IP:s from a compile order file
    """
    compile_order, libraries, include_dirs = read_compile_order(compile_order_file, fail_on_non_hdl_files)

    # Create libraries
    for library_name in libraries:
        vunit_obj.add_library(library_name, vhdl_standard="2008", allow_duplicate=True)
        # if library_name not in[l._library_name for l in vunit_obj.get_libraries()]:
        #     vunit_obj.add_external_library(library_name, sim_lib_path / library_name, vhdl_standard='2008')

    # Add all source files to VUnit
    source_files = []

    no_dependency_scan = []
    with_dependency_scan = []
    for library_name, file_name in compile_order:
        is_verilog = file_name.endswith(".v") or file_name.endswith(".vp")

        # Optionally use VUnit dependency scanning for everything in xil_defaultlib, which
        # typically contains unencrypted top levels that instantiate encrypted implementations.
        scan_dependencies = dependency_scan_defaultlib and library_name == "xil_defaultlib"
        source_file = vunit_obj.library(library_name).add_source_file(
            file_name,
            no_parse=not scan_dependencies,
            include_dirs=include_dirs if is_verilog else None,
        )

        if scan_dependencies:
            with_dependency_scan.append(source_file)
        else:
            no_dependency_scan.append(source_file)

        source_files.append(source_file)

    # Use hardcoded dependency for everthing outside of xil_defaultlib
    for idx in range(1, len(no_dependency_scan)):
        no_dependency_scan[idx].add_dependency_on(no_dependency_scan[idx - 1])

    # Add dependency of last item in non-dependency scanned files to the each scanned file
    if no_dependency_scan:
        for source_file in with_dependency_scan:
            source_file.add_dependency_on(no_dependency_scan[-1])

    return source_files

def add_standard_libraries(vu_inst, sim_lib_path):
    sim_lib_path = Path(sim_lib_path) if type(sim_lib_path) == str else sim_lib_path
    for library_name in ["unisim", "unimacro", "unifast", "secureip", "xpm"]:
        vu_inst.add_external_library(library_name, sim_lib_path / library_name)

