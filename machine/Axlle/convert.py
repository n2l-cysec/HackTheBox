import argparse
import os
import shutil

def convert_dll_to_xll(input_dll, output_xll):
    # Ensure the input DLL file exists
    if not os.path.exists(input_dll):
        print(f"Error: Input DLL file '{input_dll}' not found.")
        return
    
    # Copy the DLL to the output XLL file (simulated conversion for example)
    shutil.copyfile(input_dll, output_xll)
    print(f"Converted '{input_dll}' to '{output_xll}' successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert DLL to XLL using Xyrella")
    parser.add_argument('--input', '-i', required=True, help="Input DLL file path")
    parser.add_argument('--output', '-o', required=True, help="Output XLL file path")

    args = parser.parse_args()

    input_dll = args.input
    output_xll = args.output

    convert_dll_to_xll(input_dll, output_xll)