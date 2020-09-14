import os
import sys
import subprocess

from migen.build.generic_programmer import GenericProgrammer

# This programmer requires OpenOCD with support for eos-s3
# it has not been merged with mainline yet, but is available at:
# https://github.com/antmicro/openocd/tree/eos-s3-support
class OpenOCD(GenericProgrammer):

    def __init__(self, flash_proxy_basename=None):
        GenericProgrammer.__init__(self, flash_proxy_basename)

    def load_bitstream(self, bitstream_file):
        bitstream_folder = os.path.dirname(bitstream_file)
        top_path = bitstream_folder + "/top.cfg"
        subprocess.call(["python", "-m", "quicklogic_fasm.bitstream_to_openocd", bitstream_file, top_path])
        try:
            openocd_proc = subprocess.Popen(["openocd", "-s", "tcl",
                                             "-f", "interface/ftdi/antmicro-ftdi-adapter.cfg",
                                             "-f", "interface/ftdi/swd-resistor-hack.cfg",
                                             "-f", "board/quicklogic_quickfeather.cfg",
                                             "-f", top_path])
            gdb_commands = ["tar rem :3333", "monitor reset halt", "monitor load_bitstream"]
            gdb_output_path = bitstream_folder + "/gdb.commands"
            with open(gdb_output_path, 'w') as f:
                f.write("\n".join(gdb_commands))
            path_env = os.environ['PATH'].split(":")
            import glob
            gdb = None
            for path in path_env:
                gdb_glob = glob.glob(path + '/arm-*-eabi-gdb')
                if len(gdb_glob):
                    gdb = gdb_glob[0].strip()
                    break;
            if gdb is None:
                raise Exception("No arm-*-eabi-gdb found in PATH")
            subprocess.call([gdb, "-x", gdb_output_path])
        except Exception as e:
            openocd_proc.kill()
            raise e

class JLinkProgrammer(GenericProgrammer):

    def __init__(self, flash_proxy_basename=None):
        GenericProgrammer.__init__(self, flash_proxy_basename)

    def load_bitstream(self, bitstream_file):
        bitstream_folder = os.path.dirname(bitstream_file)
        jlink_output_path = bitstream_folder + "/top.jlink"
        jlink_output_reset_path = bitstream_folder + "/top_reset.jlink"
        subprocess.call(["python", "-m", "quicklogic_fasm.bitstream_to_jlink", bitstream_file, jlink_output_path])
        with open(jlink_output_path, 'r') as f:
            with open(jlink_output_reset_path,'w') as f2: # add reset command at the beginning
                f2.write("r\n")
                f2.write(f.read())

        subprocess.call(["JLinkExe", "-Device", "Cortex-M4", "-If", "SWD", "-Speed", "4000", "-commandFile", jlink_output_reset_path])
