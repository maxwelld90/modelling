#
# Log processing script for CSCW data
# Revision 2
#
# Author: David Maxwell
# Date: 2020-08-05
#

import sys
from log_processor.processor import main
from log_processor.helpers import load_config_dict, get_groups, get_topics, get_database_connection

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python -m log_processor <config_file>", file=sys.stderr)
        print("Where:", file=sys.stderr)
        print("    <config_path>: Path to configuration file", file=sys.stderr)
        sys.exit(1)

    config = load_config_dict(sys.argv[1])
    groups = get_groups(config)
    topics = get_topics(config)
    database = get_database_connection(config)

    main(config, groups, topics, database)