from typing import List

def list_of_shell_args_to_str(cmd: List[str]) -> str:
    """
    Converts ['echo', 'Hello world'] to 'echo "Hello world"'
    """

    args_with_apostroves_where_necessary = []

    for e in cmd:
        args_with_apostroves_where_necessary.append(with_apostroves_if_necessary(e))

    return " ".join(args_with_apostroves_where_necessary)

def with_apostroves_if_necessary(str_in: str) -> str:
    """
    Returns the same string, surrounded with apostrophes, only if it contains whitespaces.
    """

    if str_in.find(' ') == -1:
        return str_in
    else:
        return '"' + str_in + '"'