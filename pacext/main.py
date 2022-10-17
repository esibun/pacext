import click

from pacext.delete import delete
from pacext.db import ensure_container
from pacext.fs import prepare_pacroot, unmount_all
from pacext.sync import sync, upgrade


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


@click.command(help="Install (upgrade) a package from file")
@click.argument('args', nargs=-1)
@click.pass_context
def upgrade_op(ctx, args):
    container = ctx.obj['container']
    upgrade(container, args)


@click.command(help="Delete a SYSEXT container")
@click.pass_context
def delete_op(ctx):
    container = ctx.obj['container']
    delete(container)


@click.command(help="Cleanup mounts")
@click.pass_context
def cleanup_op(ctx):
    unmount_all()

@click.command(help="Mount container for further operations")
@click.pass_context
def mount_op(ctx):
    container = ctx.obj['container']
    container_info = ensure_container(container)
    prepare_pacroot(container_info)


cli.add_command(sync_op, name="-S")
cli.add_command(upgrade_op, name="-U")
cli.add_command(delete_op, name="-D")
cli.add_command(cleanup_op, name="-C")
cli.add_command(mount_op, name="-M")

if __name__ == '__main__':
    cli()
