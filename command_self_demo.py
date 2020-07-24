from flask import Flask
import click

app = Flask(__name__)


@app.cli.command()
def h():
    click.echo('Hi, baby!')
