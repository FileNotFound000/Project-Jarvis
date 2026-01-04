import queue
import time
import jupyter_client
from typing import Dict, Any

class CodeInterpreterService:
    def __init__(self):
        self.km = None
        self.kc = None
        self._start_kernel()

    def _start_kernel(self):
        """Starts a new Jupyter kernel."""
        try:
            self.km = jupyter_client.KernelManager(kernel_name='python3')
            self.km.start_kernel()
            self.kc = self.km.client()
            self.kc.start_channels()
            # Wait for kernel to be ready
            self.kc.wait_for_ready(timeout=10)
            print("Code Interpreter Kernel started.")
        except Exception as e:
            print(f"Failed to start Code Interpreter Kernel: {e}")
            self.km = None
            self.kc = None

    def execute_code(self, code: str, timeout: int = 10) -> Dict[str, Any]:
        """
        Executes Python code in the kernel and returns the result.
        Returns a dict with 'output' (stdout/stderr) and 'result' (last expression value).
        """
        if not self.kc:
            self._start_kernel()
            if not self.kc:
                return {"error": "Kernel not available"}

        try:
            msg_id = self.kc.execute(code)
            
            output = ""
            result = None
            error = None
            
            while True:
                try:
                    msg = self.kc.get_iopub_msg(timeout=timeout)
                    msg_type = msg['header']['msg_type']
                    content = msg['content']
                    
                    if msg_type == 'stream':
                        output += content['text']
                    elif msg_type == 'execute_result':
                        result = content['data'].get('text/plain', '')
                    elif msg_type == 'error':
                        error = f"{content['ename']}: {content['evalue']}\n" + "\n".join(content['traceback'])
                    elif msg_type == 'status' and content['execution_state'] == 'idle':
                        # Execution finished
                        break
                except queue.Empty:
                    return {"error": "Execution timed out"}
                except Exception as e:
                    return {"error": f"Error reading kernel message: {str(e)}"}

            final_output = output
            if error:
                final_output += f"\nError:\n{error}"
            
            return {
                "output": final_output.strip(),
                "result": result
            }

        except Exception as e:
            return {"error": f"Execution failed: {str(e)}"}

    def restart_kernel(self):
        """Restarts the kernel."""
        if self.km:
            self.km.restart_kernel()
            self.kc = self.km.client()
            self.kc.start_channels()
            self.kc.wait_for_ready()
            print("Code Interpreter Kernel restarted.")

    def shutdown(self):
        """Shuts down the kernel."""
        if self.km:
            self.km.shutdown_kernel()
            print("Code Interpreter Kernel shutdown.")
