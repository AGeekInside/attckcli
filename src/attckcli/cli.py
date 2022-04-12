import click
from pyattck import Attck
from rich import print


attack = Attck()


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass


@cli.command()
@click.option('-m', '--matrix', envvar="ATTCKCLI_MATRIX", default="enterprise")
def list(matrix):
    techniques = [] 
    
    for technique in getattr(attack, matrix).techniques:
    # for technique in attack.enterprise.techniques:
        technique_info = { 
            "id": technique.id,
            "name": technique.name,
        }
        if len(technique.subtechniques) > 0:
            technique_info["subtechniques"] = [] 
            for subtechnique in technique.subtechniques:
                technique_info["subtechniques"].append({
                    "id": subtechnique.id,
                    "name": subtechnique.name
                })

        techniques.append(technique_info)

    print(techniques)

if __name__ == "__main__":
    cli()