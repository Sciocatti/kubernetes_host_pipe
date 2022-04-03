#!/bin/bash

# NOTE: As the script creates/deletes the pipes from the container,
# NOTE: we must keep listening for changes inside the folder. The
# NOTE: easiest way to do this is a while loop. However, this means
# NOTE: multiple pipes will be handled sequencially, ie one pipe has
# NOTE: to wait for another to finish. This is important because if
# NOTE: a pipe does break and the file remains, then it will keep delaying
# NOTE: the execution of other pipes.

# TODO use timeout response (124) to delete pipes if exists

while true;
do
    # Find all files in named_pipes/
    FILES=$(ls named_pipes/ | xargs)
    # and for each file
    for FILE in $FILES
    do
        # if it is not the response pipe
        if [[ "$FILE" != *_response ]]
        # eval the input, feed the output to the response pipe
        then eval "$(timeout 5s cat named_pipes/${FILE})" > "named_pipes/${FILE}_response"
        fi
    done
done

# while true;
# do
#     OUTPUT=$(eval "$(cat named_pipes/test1)");
#     # if [[ "$OUTPUT" != *named_pipes/test1* ]]
#     #     then echo "${OUTPUT}"
#     # fi;
# done