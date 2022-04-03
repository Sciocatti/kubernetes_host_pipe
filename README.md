# kubernetes_host_pipe
When using K3S for deployment of code, sometimes you want access to the host from within a container. Here wo solve this using named pipes.

## Minimum steps to get started:
We are going to get started with everything on the host machine, then expand from there.

1. Choose a directory on the OS that will be shared between the host and the container. In other words where the FIFO pipes will be made. In this case a folder `named_pipes` inside this repo.

2. Edit `named_pipe_executor.sh` to reflect this folder.
```bash
PIPE_DIR="named_pipes"
```

3. Give the script executable permission
```bash
chmod +x named_pipe_executor.sh
```

4. Change the `COMMAND` in `main.py` to something testable
```python
COMMAND = "ls"
```

5. Run the main file
```bash 
$ python3 main.py
```
You should get something like this printed out:
```bash 
named_pipes/pipe_1648996150
Command sent: 'ls'
Response received: 'LICENSE\nREADME.md\nmain.py\nnamed_pipe_executor.sh\nnamed_pipes\nsrc\n'
LICENSE
README.md
main.py
named_pipe_executor.sh
named_pipes
src
```

6. Adapt this for your use case. The `PIPE_DIR` folder gets mounted between the container and the host, the bash script must run on the host, and the python script runs inside the container.