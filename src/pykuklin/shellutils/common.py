from typing import List

def list_of_shell_args_to_str(cmd: List[str]) -> str:
    """
    Converts ['echo', 'Hello world'] to 'echo "Hello world"'
    """

    args_with_apostroves_where_necessary = []

    for e in cmd:
        if e.find(' ') == -1:
            args_with_apostroves_where_necessary.append(e)
        else:
            args_with_apostroves_where_necessary.append('"' + e + '"')

    return " ".join(args_with_apostroves_where_necessary)