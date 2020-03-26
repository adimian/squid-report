import click

from squidreport import read_config
from squidreport.report import report


@click.command()
@click.argument("config")
@click.option("--disable", "-x", multiple=True)
def main(config, disable):
    config = read_config(config_file=config, DISABLE_RULES=disable)
    report(config)


if __name__ == "__main__":
    main()
