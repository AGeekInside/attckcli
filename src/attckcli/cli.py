import click
from pyattck import Attck
from rich import print

from .download import download_json


attack = Attck()


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass


@cli.command()
@click.option('-u', '--url', envvar="ATTCK_BASEURL", default="https://raw.githubusercontent.com/mitre/cti/master/")
def download(url):

    matrices = [
        {
            'name': 'enterprise',
            'url_ending': 'enterprise-attack/enterprise-attack.json',
        },
        {
            'name': 'mobile',
            'url_ending': 'mobile-attack/mobile-attack.json',
        },
        {
            'name': 'ics',
            'url_ending': 'ics-attack/ics-attack.json',
        },
    ]

    for matrix in matrices:
        print(f"Downloading JSON for {matrix['name']}.")
        matrix['json'] = download_json(f"{url}{matrix['url_ending']}")
        objects = matrix['json']['objects']

        id_lookup = {}
        tactics = {}
        attack_patterns = {}

        for object in objects:
            attck_id = object['id']
            obj_type = object['type']
            id_lookup[attck_id] = object
            if obj_type == 'x-mitre-tactic':
                tactics[attck_id] = object
            elif obj_type == 'attack-pattern':
                attack_patterns[attck_id] = object
        
        matrix['id_lookup'] = id_lookup
        matrix['tactics'] = tactics
        matrix['attack_patterns'] = attack_patterns

        print(f"Found {len(matrix['id_lookup']):,} ids.")
        print(f"Found {len(matrix['tactics']):,} tactics.")
        print(f"Found {len(matrix['attack_patterns']):,} attack patterns.")

    


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