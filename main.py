# main.py
import os
import asyncio
from datetime import datetime
from argparse import ArgumentParser

from mimir.runner.collect_info import CollectInfoRunner
from mimir.services.configuration.configuration import Configuration
from mimir.services.logger.logger import Logger

def build_create_config_parser(subparsers):
    # Subcommand to create a default config
    create_config_parser = subparsers.add_parser(
        "create-config", help="Create the default configuration file"
    )
    create_config_parser.add_argument(
        "--config",
        type=str,
        default=os.path.join("config", "default_config.json"),
        help=f"Path to the config file (default: '{os.path.join("config", "default_config.json")}')",
    )

def build_collect_info_parser(subparsers):
    # Subcommand to run the tool
    collect_info_parser = subparsers.add_parser(
        "collect-info", help="Collect tests with the specified configuration file"
    )
    collect_info_parser.add_argument(
        "--target",
        type=str,
        default=os.path.join("temp", "example-repo"),
        help=f"Path to the target repo: '{os.path.join("temp", "example-repo")}')",
    )
    collect_info_parser.add_argument(
        "--config",
        type=str,
        default=os.path.join("config", "default_config.json"),
        help=f"Path to the config file (default: '{os.path.join("config", "default_config.json")}')",
    )

def build_command_parser():
    # Set up the argument parser
    parser = ArgumentParser(
        prog='mimir',
        description="Tool for analyzing code repositories and mapping tests.",

    )

    # Create subparsers for subcommands
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    build_create_config_parser(subparsers)
    build_collect_info_parser(subparsers)

    return parser


async def main():

    # get the run time
    runtime = datetime.now()

    # Format the date and time
    current_day = runtime.strftime("%Y-%m-%d")

    parser = build_command_parser()

    # Parse the arguments
    args = parser.parse_args()

    # create the default config
    if args.command == "create-config":
        create_config_logger = Logger("logs", current_day, "create-config")
        Configuration.create_default_config(
            os.path.join("config", "default_config.json"),
            create_config_logger
        )
    # collect information from the specified target repo
    elif args.command == "collect-info":
        collect_info_logger = Logger("logs", current_day, "collect-info")
        collect_info_config = Configuration(args.config, collect_info_logger)
        collect_info_runner = CollectInfoRunner(collect_info_config, collect_info_logger)
        await collect_info_runner.run_mimir_runner()

    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
