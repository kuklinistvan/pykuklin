from pykuklin.git import gitignore as kgitignore
from . import cli_entry

import click

@cli_entry.group()
def gitignore():
    pass

@gitignore.command()
def ls():
    """
    Gets a list of the available templates.
    """
    print("Templates: ")
    for i in kgitignore.ls():
        print("* " + i)

    print("Template groups: ")
    for i in kgitignore.ls_group():
        print("* g/" + i)

@gitignore.command()
@click.argument('templates', nargs=-1)
def dump(templates):
    """
    Writes the templates specified to stdout.
    """

    for t in templates:
        if str(t).startswith("g/"):
            groupname = t[2:]
            print("## Group: " + groupname)
            for template in kgitignore.get_group_members(groupname):
                print(_format_template(template))

            print("## EndGroup: " + groupname + "\n")
            
        else:
            print(_format_template(t))        
        
def _format_template(template: str) -> str:
    return "# " + template + "\n" + kgitignore.get(template)+"\n"
