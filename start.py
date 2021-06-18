import subprocess, os
cmd = f"cd .{os.sep}BlackPearl-7788{os.sep}"
subprocess.run(cmd, shell=True)
subprocess.run("python run.py", shell=True)