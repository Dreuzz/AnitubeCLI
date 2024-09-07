import requests
import click

BASE_URL = "https://anitube-api.vercel.app/"  # Base URL for the Consumet API

@click.group()
def cli():
    """Consumet CLI Tool"""
    pass

@cli.command()
@click.argument('query')
def anime(query):
    """Search for anime."""
    response = requests.get(f"{BASE_URL}/anime/gogoanime/{query}")
    data = response.json()
    for anime in data.get("results", []):
        click.echo(f"Title: {anime['title']} - {anime['id']}")
        click.echo(f"Status: {anime['releaseDate']}")
        click.echo('-' * 60)

@cli.command()
@click.argument('id')
@click.option('--episode', prompt='episode')
def watch(id, episode):
    """Watch the anime (id)."""
    response = requests.get(f"{BASE_URL}/anime/gogoanime/watch/{id}-episode-{episode}")
    data = response.json()
    referer = data.get("headers", {}).get("Referer")
    if referer is not None:
        click.launch(f'{referer}')
        click.pause()
    else:
        click.echo(f"\nEpisode does not exist!")

@cli.command()
@click.argument('id')
def total(id):
    """See how many episodes an anime has (id)."""
    response = requests.get(f"{BASE_URL}/anime/gogoanime/info/{id}")
    data = response.json()
    total = data.get('totalEpisodes')
    if total:
        click.echo(f"Total Episodes: {total}")
        

@cli.command()
@click.argument('query')
def manga(query):
    """Search for manga."""
    response = requests.get(f"{BASE_URL}/meta/anilist/{query}?type=manga")
    data = response.json()
    for manga in data.get("results", []):
        click.echo(f"Title: {manga['title']['romaji']}")
        click.echo(f"Status: {manga['status']}")
        click.echo('-' * 40)

if __name__ == '__main__':
    cli()
