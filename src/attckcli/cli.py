import click
import json
from pyattck import Attck
from rich import print

from .download import download_json
from .database import load_database


attack = Attck()


class SharedOptions(click.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.insert(
            0,
            click.core.Option(
                (
                    "-u",
                    "--url",
                ),
                envvar="ATTCK_BASEURL",
                default="https://raw.githubusercontent.com/mitre/cti/master/",
                help="URL to use when download ATT&CK data.",
            ),
        )


def load_matrices(base_url):
    matrices = [
        {
            "name": "enterprise",
            "url_ending": "enterprise-attack/enterprise-attack.json",
        },
        {
            "name": "mobile",
            "url_ending": "mobile-attack/mobile-attack.json",
        },
        {
            "name": "ics",
            "url_ending": "ics-attack/ics-attack.json",
        },
    ]
    for matrix in matrices:
        print(f"Downloading JSON for {matrix['name']}.")
        download_url = f"{base_url}{matrix['url_ending']}"
        matrix["download_url"] = download_url
        matrix["json"] = download_json(download_url)
        matrix["objects"] = matrix["json"]["objects"]

    return matrices


@click.group()
def cli():
    pass


@cli.command(cls=SharedOptions)
@click.option(
    "-d",
    "--data_dir",
    envvar="ATTCK_DATADIR",
    default="./data",
)
def download(url, data_dir):

    matrices = load_matrices(url)
    for matrix in matrices:
        with open(f"{data_dir}/{matrix['name']}-attack.json", "w") as output_jsonfile:
            json.dump(matrix["json"], output_jsonfile)


@cli.command(cls=SharedOptions)
def setup(url):

    matrices = load_matrices(url)
    load_database(matrices)


@cli.command()
@click.option("-m", "--matrix", envvar="ATTCKCLI_MATRIX", default="enterprise")
@click.option("--references/--no-references", default=False)
def list(matrix, references):
    techniques = []

    for technique in getattr(attack, matrix).techniques:
        # for technique in attack.enterprise.techniques:
        technique_info = {
            "id": technique.id,
            "name": technique.name,
            "reference": technique.reference,
        }
        if len(technique.subtechniques) > 0:
            technique_info["subtechniques"] = []
            for subtechnique in technique.subtechniques:
                technique_info["subtechniques"].append( {
                    "id": subtechnique.id, 
                    "name": subtechnique.name,
                    "reference": subtechnique.reference,
                })

        techniques.append(technique_info)

    print(techniques)


if __name__ == "__main__":
    cli()
