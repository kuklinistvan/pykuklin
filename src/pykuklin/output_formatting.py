from contextlib import contextmanager
from typing import List
import os

# https://stackoverflow.com/a/17303428/4770338

class ConsoleColor:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   
@contextmanager
def ConsoleColored(modifiers: List[str]):
    """
    Puts a linebreak to the end!
    """

    print("".join(modifiers), end="")
    yield
    print(ConsoleColor.END)


def print_cut_here(title: str, modifiers: List[str]):
   width = os.get_terminal_size().columns
   dashes = width - len(title)
   dashes_before = int(dashes/2)
   dashes_after = dashes - dashes_before

   print("\n") # new line
   with ConsoleColored(modifiers):
      for _ in range(0, dashes_before-1):
         print("-", end="")
      print(" ", end="")
      
      print(title, end="")

      print(" ", end="")
      for _ in range(0, dashes_after-1):
         print("-", end="")
   print("") # new line