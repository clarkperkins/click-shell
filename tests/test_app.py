# -*- coding: utf-8 -*-

import click
import click_shell


@click_shell.shell(prompt='prompt > ')
def main():
    pass


@main.command()
def command_test():
    click.echo('This line is returned.')


if __name__ == '__main__':
    main()
