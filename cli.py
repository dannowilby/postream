import sys
import os
import toml
from dotenv import dotenv_values

# Could use the CMD to make this code less verbose, but as it is it works
# Todo: separate servers into separate folders

config = toml.load("postream.config.toml")

def help():
    print("This is the Postream CLI.")
    print("Use it to set up, run the application, or build your website with this CMS.\n")
    print("Commands")
    print("------------------------")
    print("./postream.sh setup")
    print("Sets up the Postream application using the details specified in the `postream.config.toml` file.")
    print("")
    print("./postream.sh run")
    print("Makes sure the PostgreSQL server is running and starts the Streamlit frontend interface.")
    print("")
    print("./postream.sh build")
    print("Makes sure the PostgreSQL server is running and executes the specified build command for the build server.")

def run(args):
    # start the postgres server
    os.system("docker run --name my_postgres -p 5432:5432 -v $(pwd)/data/data:/var/lib/postgresql/data --env-file ./data/postgres.env -d postgres")
    # start the streamlit frontend
    os.system("cd frontend && streamlit run src/app.py")

def build(args):
    # start the postgres server
    os.system("docker run --name my_postgres -p 5432:5432 -v $(pwd)/data/data:/var/lib/postgresql/data --env-file ./data/postgres.env -d postgres")
    # run the build command
    os.system(f"cd build-server && {config['build-server']['build_command']}")

def setup(args):
    # set the postgres, build server, and streamlit frontend postgres connection details / build command

    # read .env file
    secrets = dotenv_values(config['secrets_file'])

    write_streamlit_secrets(secrets)
    write_env_file("data/postgres.env", secrets)
    write_env_file("build-server/.env", secrets)

    # add build command to streamlit
    write_build_script_file(config['build-server']['build_command'])
    # todo: configure ports on streamlit and postgres servers

def write_build_script_file(command):
    with open("frontend/build-server.sh", "w") as file:
        file.write(command)

def write_env_file(path, secrets):
    with open(path, "w") as file:
        lines = []
        for (key, value) in secrets.items():
            lines.append(f"{key}={value}\n")
        file.writelines(lines)

def write_streamlit_secrets(secrets):
    with open("frontend/.streamlit/secrets.toml", "w") as file:
        lines = []
        for (key, value) in secrets.items():
            lines.append(f"{key} = \"{value}\"\n")
        file.writelines(lines)

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print("Usage: ./postream.sh [OPTION]...")
        print("Try './postream.sh help' for more information.")
        sys.exit(0)

    match args[1]:
        case 'help':
            help()
        case 'run':
            run(args)
        case 'build':
            build(args)
        case 'setup':
            setup(args)
        case _:
            print("Unknown command.")
            print("Try './postream.sh help' to see a list of commands and their descriptions.")
    sys.exit(0)
