import subprocess, os
cmd = f"cd .{os.sep}BlackPearl-7788{os.sep}"
subprocess.run(cmd, shell=True)
subprocess.run("py -3 run.py", shell=True)