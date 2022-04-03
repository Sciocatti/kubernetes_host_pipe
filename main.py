from src.single_pipe_controller import SinglePipeController

COMMAND = "ls"

def main():
    # Init the SinglePipeController
    pipe: SinglePipeController = SinglePipeController()
    # Send the command over the write pipe, wait for input
    # on the read pipe and return that
    response = pipe.send_message(COMMAND)
    # Print the output
    print(response)


if __name__ == "__main__":
    main()
    