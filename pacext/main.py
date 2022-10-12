import click

from pacext.delete import delete
from pacext.fs import unmount_all
from pacext.sync import sync


@click.group()
@click.argument('container')
@click.pass_context
def cli(ctx, container):
    ctx.ensure_object(dict)
    ctx.obj['container'] = container


@click.command(help="Install (sync) a package from repo")
@click.argument('packages', nargs=-1)
@click.pass_context
def sync_op(ctx, packages):
    container = ctx.obj['container']
    sync(container, packages)


@click.command(help="Delete a SYSEXT container")
@click.pass_context
def delete_op(ctx):
    container = ctx.obj['container']
    delete(container)


@click.command(help="Cleanup mounts")
@click.pass_context
def cleanup_op(ctx):
    unmount_all()


cli.add_command(sync_op, name="-S")
cli.add_command(delete_op, name="-D")
cli.add_command(cleanup_op, name="-C")

if __name__ == '__main__':
    cli()
