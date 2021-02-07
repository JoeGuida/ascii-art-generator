from asciiartgenerator import AsciiArtGenerator
import click

@click.command()
@click.option('--url', default=None, help='image url')
@click.option('--local-url', default=None, help='local image file address')
@click.option('--bw', default=4, help='block width')
@click.option('--bh', default=5, help='block height')
@click.option('--file', default='output.txt', help='output filename')
def generate(url, local_url, bw, bh, file):
    generator = AsciiArtGenerator()
    generator.block_width = bw
    generator.block_height = bh

    if(local_url != None):
        generator.load_image(file, local_url)
    elif(url != None):
        generator.load_image(file, None, url)
    elif(local_url == None and url == None):
        click.echo('No image supplied, use --url to add an image URL or --local-url to add a local url')

if __name__ == '__main__':
    generate()