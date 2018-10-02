import csv
from tormor.connection import execute_sql_file
from tormor.schema import enablemodules, migrate
import os


SHORTOPTS = "?d:h:p:U:P:"
PGOPTMAP = {
    "-d": ("dbname", "PGDATABASE"), 
    "-h": ("host", "PGHOST"), 
    "-p": ("port", "PGPORT"), 
    "-U": ("user", "PGUSER"),
    "-P": ("password", "PGPASSWORD")
}

HELPTEXT = """Tormor -- Migration management

    tormor [opts] command [args]

opts are one or more of:

    -?                      Print this text
    -h hostname             Postgres host
    -d database             Database name
    -U username             Database username (role)
    -p port                 Database port
    -P password             Database password (Not recommended, use environment variable PGPASSWORD instead)

Command is one of:
    enable-modules mod1 [mod2 [mod3 ...]]
        Enable the modules.

    help
        Show this text

    include filename
        Find commands (one per line) in the specified file and run them

    migrate
        Run all migrations.

    sql filename
        Load the filename and present the SQL in it to the database for
        execution. This is useful for choosing migrations scripts to run.

"""


def makedsn(opts, args):
    dsnargs = {}
    for arg, (opt, env) in PGOPTMAP.items():
        if arg in opts:
            dsnargs[opt] = opts[arg]
        elif os.getenv(env):
            dsnargs[opt] = os.getenv(env)
    return " ".join(["%s='%s'" % (n, v) for n, v in dsnargs.items()])


def include(cnx, filename):
    with open(filename, newline="") as f:
        lines = csv.reader(f, delimiter=" ")
        for line in lines:
            if len(line) and not line[0].startswith("#"):
                command(cnx, *[p for p in line if p])


COMMANDS = {
    "enable-modules": enablemodules,
    "migrate": migrate,
    "include": include,
    "sql": execute_sql_file,
}


class UnknownCommand(Exception):
    pass


def command(cnx, cmd, *args):
    if cmd in COMMANDS:
        COMMANDS[cmd](cnx, *args)
    else:
        raise UnknownCommand(cmd)

