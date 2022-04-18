import click
import json
from pyattck import Attck
from rich import print

from .download import download_json


attack = Attck()
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


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    pass


@cli.command(cls=SharedOptions)
@click.option(
    "-d",
    "--data_dir",
    envvar="ATTCK_DATADIR",
    default="./data",
)
def download(url, data_dir):

    for matrix in matrices:
        print(f"Downloading JSON for {matrix['name']}.")
        matrix["json"] = download_json(f"{url}{matrix['url_ending']}")
        objects = matrix["json"]["objects"]

        with open(f"{data_dir}/{matrix['name']}-attack.json", "w") as output_jsonfile:
            json.dump(matrix["json"], output_jsonfile)


@cli.command()
@click.option("-m", "--matrix", envvar="ATTCKCLI_MATRIX", default="enterprise")
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
                technique_info["subtechniques"].append(
                    {"id": subtechnique.id, "name": subtechnique.name}
                )

        techniques.append(technique_info)

    print(techniques)


if __name__ == "__main__":
    cli()
