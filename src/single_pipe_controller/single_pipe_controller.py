

import os
import time
import errno

class SinglePipeController:
    """
        Sends a message over a FIFO pipe, and listen for the response on another pipe.
        This class creates both pipes, and deletes them when done.

        NOTE: It will block if the output cannot be read from the pipe.
    """
    def __init__(self, pipe_name: str or None = None, pipe_directory: str = "named_pipes") -> None:
        """
            Inits a `SinglePipeController`.
            ### params
            - `pipe_name`: The name of the pipe to write to. If `None` it will default to `pipe_{unix_timestamp}`.
                           The pipe to read from will be `{pipe_name}_response`.
            - `pipe_directory`: The directory to create the pipes in. Defaults to `named_pipes` in the folder the
                                script is run from.

            ### returns
            None
        """
        if pipe_name is None:
            pipe_name = f"pipe_{str(int(time.time()))}"
        if not os.path.isdir(pipe_directory):
            os.mkdir(pipe_directory)
        # We are going to be writing to this pipe
        self.pipe_name_write = f"{pipe_directory}/{pipe_name}"
        # and reading the results from this one.
        self.pipe_name_read = f"{pipe_directory}/{pipe_name}_response"
        self._create_pipe_if_not_exists(self.pipe_name_write)
        self._create_pipe_if_not_exists(self.pipe_name_read)

    def send_message(self, message: str) -> str:
        """
            Sends a message through the pipe and returns the response.
            NOTE: This will block if nothing reads from the other end of 
                  the write pipe or nothing writes to the read pipe

            ### params
            - `message`: The message to send through the write pipe.

            ### returns
            A string for the response from the read pipe. 
        """
        self._write_message(message)
        response = self._read_message()
        print(f"Response received: {repr(response)}")
        self._delete_pipe_if_exists(self.pipe_name_write)
        self._delete_pipe_if_exists(self.pipe_name_read)
        return response

    def _create_pipe_if_not_exists(self, pipe_name):
        """
            Creates a pipe if it does not exist.
        """
        try:
            os.mkfifo(pipe_name)
        except OSError as e:
            if e.errno == errno.EEXIST:
                # The pipe already exists
                return
            raise e
        except Exception as e:
            # TODO Custom application error logging/handling here
            raise e

    def _delete_pipe_if_exists(self, pipe_name):
        """
            Deletes a pipe if it does exist.
        """
        try:
            os.remove(pipe_name)
        except Exception as e:
            # TODO Custom application error logging/handling here
            raise e

    def _write_message(self, message, newline = False):
        """
            Writes `message` to the outgoing pipe.
        """
        with open(self.pipe_name_write, 'wb') as fifo:
            print(self.pipe_name_write)
            message = message.strip()
            message = (message + "\r\n") if newline else message
            fifo.write(message.encode())
            print(f"Command sent: {repr(message)}")

    def _read_message(self):
        """
            Reads what is available from the incoming pipe.
        """
        response = ""
        with open(self.pipe_name_read, 'r') as fifo:
            while True:
                data = fifo.read()
                if len(data) == 0:
                    break 

                for d in data:
                    response += str(d)

        return response
