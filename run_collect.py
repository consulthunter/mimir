# run_tool.py

import asyncio
from mimir.main import run_command, build_command_parser

parser = build_command_parser()
args = parser.parse_args(["collect-info", "--config" ,"config\\default_config.json"])


if __name__ == "__main__":
    asyncio.run(run_command(args))
