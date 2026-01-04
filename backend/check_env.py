import sys
import time

print(f"Python executable: {sys.executable}")
try:
    import jupyter_client
    print(f"jupyter_client version: {jupyter_client.__version__}")
    
    print("Attempting to start kernel...")
    km = jupyter_client.KernelManager(kernel_name='python3')
    km.start_kernel()
    print("Kernel started.")
    kc = km.client()
    kc.start_channels()
    kc.wait_for_ready(timeout=10)
    print("Kernel ready.")
    km.shutdown_kernel()
    print("Kernel shutdown.")
    
except Exception as e:
    print(f"Error: {e}")
