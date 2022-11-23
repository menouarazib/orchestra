
import git
import logging
import os
from pathlib import Path
import json

import sqlite3
from .create_docker import DockerCreator
from .constant import __json_data_key__, METADATA_JSON_FILE_NAME, __json_info__, __json_type_key__, __json_warning__,\
    __DB_COLUMN_DESCRIPTION__, __DB_COLUMN_ID__, __DB_COLUMN_NAME__, __DB_COLUMN_TAG__, __DB_COLUMN_VERSION__,\
    __TASK_COLUMN_ID__, __MODULE_COLUMN_ID__, __STATUS_COLUMN__, __OUTPUT_FOLDER_NAME_COLUMN__, __ARG_START__, __ARG_STOP__, Status, \
    __DB_COLUMN_DEFAULTS_ARG_START__, __DB_COLUMN_DEFAULTS_ARG_STOP__,\
    __DB_COLUMN_OUTPUT_TYPE__, __DB_COLUMN_OUTPUT_FILENAME__, __MODEL_VERSION__, __PRE_PROCESS__, __POST_PROCESS__,\
    __PYTHON_VERSION__, __EXECUTABLE__, __FILES__, __REQUIREMENTS__, __DEFAULTS__, __OUTPUT__, __ANNEXES_OUTPUT__, \
    __INSTALL__, __OUTPUT_FILES__, __json_error__, __GIT_REPO_URL__

# Usefull constant
__select_var__ = "SELECT * FROM {} WHERE {}={};"


class Module():
    """Class which represetns orchestra Module
    """

    def __init__(self, name, version, description, defaults, output, annexes_outputs, install, git_url):
        self.name = name
        self.version = version
        self.description = description
        self.defaults = defaults
        self.output = output
        self.annexes_outputs = annexes_outputs
        self.install = install
        self.git_url = git_url

    def __str__(self) -> str:
        return "Name : {}, Version : {}".format(self.name, self.version)

    def get_default_start(self):
        return self.defaults[__DB_COLUMN_DEFAULTS_ARG_START__]

    def get_default_stop(self):
        return self.defaults[__DB_COLUMN_DEFAULTS_ARG_STOP__]

    def get_model_version(self):
        return self.install[__MODEL_VERSION__]

    def get_python_version(self):
        return self.install[__PYTHON_VERSION__]

    def get_requirements(self):
        return self.install[__REQUIREMENTS__]

    def get_files(self, stringfy=False):
        if stringfy:
            return json.dumps(self.install[__FILES__])
        return self.install[__FILES__]

    def get_executable(self):
        return self.install[__EXECUTABLE__]

    def get_pre_process(self, stringfy=False):
        if stringfy:
            return json.dumps(self.install[__PRE_PROCESS__])
        return self.install[__PRE_PROCESS__]

    def get_post_process(self, stringfy=False):
        if stringfy:
            return json.dumps(self.install[__POST_PROCESS__])
        return self.install[__POST_PROCESS__]

    def get_image_tag(self):
        return self.name.lower()+":"+self.version

    def get_output_type(self):
        return self.output[__DB_COLUMN_OUTPUT_TYPE__]

    def get_output_filename(self):
        return self.output[__DB_COLUMN_OUTPUT_FILENAME__]


class DBManager:
    """Manager of the database
    """

    def __init__(self, db_path):
        self.db = None
        self.table_projcets = "project"
        self.table_tasks = "tasks"
        self.annexes_outputs = "annexes_outputs"
        if self.db is None:
            self.db = sqlite3.connect(db_path, check_same_thread=False)
            self.cur = self.db.cursor()
            self.create_table_projects()
            self.create_table_tasks()
            self.create_table_annexes_outputs()

    def create_table_projects(self):
        logging.info("Creating a project Table")
        sql = "CREATE TABLE if not exists {} ( {} INTEGER PRIMARY KEY AUTOINCREMENT,\
             {} NOT NULL, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(self.table_projcets, __DB_COLUMN_ID__,
                                                                                              __DB_COLUMN_NAME__, __DB_COLUMN_VERSION__,
                                                                                              __DB_COLUMN_TAG__, __DB_COLUMN_DESCRIPTION__,
                                                                                              __DB_COLUMN_DEFAULTS_ARG_START__, __DB_COLUMN_DEFAULTS_ARG_STOP__,
                                                                                              __DB_COLUMN_OUTPUT_TYPE__, __DB_COLUMN_OUTPUT_FILENAME__,
                                                                                              __MODEL_VERSION__, __PYTHON_VERSION__,
                                                                                              __EXECUTABLE__, __PRE_PROCESS__,
                                                                                              __POST_PROCESS__, __FILES__, __REQUIREMENTS__, __GIT_REPO_URL__)
        self.cur.execute(sql)

    def create_table_tasks(self):
        logging.info("Creating a task Table")
        sql = "CREATE TABLE if not exists {} ( {} INTEGER PRIMARY KEY AUTOINCREMENT, {} NOT NULL, {}, {}, {}, {} ,{})".format(self.table_tasks,
                                                                                                                              __TASK_COLUMN_ID__,
                                                                                                                              __MODULE_COLUMN_ID__, __STATUS_COLUMN__, __OUTPUT_FOLDER_NAME_COLUMN__,
                                                                                                                              __ARG_START__, __ARG_STOP__, __OUTPUT_FILES__)
        self.cur.execute(sql)

    def create_table_annexes_outputs(self):
        logging.info("Creating a annexes outputs Table")
        sql = "CREATE TABLE if not exists {} ({}, {}, {})".format(
            self.annexes_outputs, __MODULE_COLUMN_ID__, __DB_COLUMN_OUTPUT_TYPE__, __DB_COLUMN_OUTPUT_FILENAME__)
        self.cur.execute(sql)

    def add_module(self, module: Module):
        logging.info("Add a new Module with id = {}".format(module))
        try:
            sql = "INSERT INTO {} ({}, {},  {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) \
            VALUES ('{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', '{}',  '{}');".format(self.table_projcets,
                                                                                                                  __DB_COLUMN_NAME__, __DB_COLUMN_VERSION__,
                                                                                                                  __DB_COLUMN_TAG__, __DB_COLUMN_DESCRIPTION__,
                                                                                                                  __DB_COLUMN_DEFAULTS_ARG_START__, __DB_COLUMN_DEFAULTS_ARG_STOP__,
                                                                                                                  __DB_COLUMN_OUTPUT_TYPE__, __DB_COLUMN_OUTPUT_FILENAME__,
                                                                                                                  __MODEL_VERSION__, __PYTHON_VERSION__,
                                                                                                                  __EXECUTABLE__, __PRE_PROCESS__,
                                                                                                                  __POST_PROCESS__, __FILES__, __REQUIREMENTS__, __GIT_REPO_URL__,
                                                                                                                  module.name, module.version,
                                                                                                                  module.get_image_tag(),  module.description,
                                                                                                                  module.get_default_start(),  module.get_default_stop(),
                                                                                                                  module.get_output_type(),  module.get_output_filename(),
                                                                                                                  module.get_model_version(),  module.get_python_version(),
                                                                                                                  module.get_executable(),  module.get_pre_process(stringfy=True),
                                                                                                                  module.get_post_process(
                                                                                                                      stringfy=True),  module.get_files(stringfy=True),
                                                                                                                  module.get_requirements(), module.git_url)
            self.cur.execute(sql)
            self.db.commit()
            moudle_id = self.cur.lastrowid
            if module.annexes_outputs:
                data = []
                for e in module.annexes_outputs:
                    data.append(
                        (moudle_id, e[__DB_COLUMN_OUTPUT_TYPE__], e[__DB_COLUMN_OUTPUT_FILENAME__]))
                self.cur.executemany("INSERT INTO {} VALUES(?, ?, ?)".format(
                    self.annexes_outputs), data)
                self.db.commit()
            return {__json_data_key__: "The Module is Succecefuly Build and Saved", __json_type_key__: __json_info__}
        except Exception as e:
            return {__json_data_key__: str(e), __json_type_key__: __json_error__}

    def check_if_model_exists(self, name, version):
        sql = "SELECT * FROM {}  WHERE {}='{}' AND {}='{}';".format(
            self.table_projcets, __DB_COLUMN_NAME__, name, __DB_COLUMN_VERSION__, version)
        res = self.cur.execute(sql)
        return res.fetchone() is not None

    def get_modules(self):
        logging.info("Get All Modules")
        sql = "SELECT * FROM {} ;".format(self.table_projcets)
        res = self.cur.execute(sql)
        colnames = self.cur.description
        res = res.fetchall()

        output = []
        for m in range(len(res)):
            module_id = -1
            for i in range(len(colnames)):
                col_name = colnames[i][0]
                if col_name == __DB_COLUMN_ID__:
                    module_id = res[m][i]
                    break
            # add annexes_output
            annexes, annexes_colnames = self.get_annexes_output(module_id)

            module_temp = format_module(
                res=res[m], colnames=colnames, annexes=annexes, annexes_colnames=annexes_colnames)
            output.append(module_temp)

        return output

    def get_module(self, id):
        logging.info("Get the Module with id = {}".format(id))
        sql = __select_var__ .format(
            self.table_projcets, __DB_COLUMN_ID__, id)
        res = self.cur.execute(sql)
        res = res.fetchone()
        if res is None:
            msg = "The model with id {} does not exist in the database".format(
                id)
            raise Excep(msg)

        colnames = self.cur.description
        # add annexes_output
        annexes, annexes_colnames = self.get_annexes_output(id)
        output = format_module(res=res, colnames=colnames,
                               annexes=annexes, annexes_colnames=annexes_colnames)

        return output

    def delete_module(self, id):
        logging.info("Deleting a module with id = {}".format(id))
        sql = "DELETE FROM {} WHERE {} = {};".format(
            self.table_projcets, __DB_COLUMN_ID__, id)
        self.cur.execute(sql)
        self.db.commit()
        sql1 = "DELETE FROM {} WHERE {} = {};".format(
            self.annexes_outputs, __MODULE_COLUMN_ID__, id)
        self.cur.execute(sql1)
        self.db.commit()

    def get_annexes_output(self, module_id):
        sql = __select_var__ .format(
            self.annexes_outputs, __MODULE_COLUMN_ID__, module_id)
        res = self.cur.execute(sql)
        return res.fetchall(),  self.cur.description

    def add_task(self, module_id, start, stop, output_dir, output_flies):
        sql = "INSERT INTO {} ({}, {},  {}, {}, {}, {}) VALUES ('{}', '{}','{}','{}', '{}','{}');".format(self.table_tasks,
                                                                                                          __MODULE_COLUMN_ID__, __STATUS_COLUMN__,
                                                                                                          __OUTPUT_FOLDER_NAME_COLUMN__, __ARG_START__,
                                                                                                          __ARG_STOP__, __OUTPUT_FILES__, module_id,
                                                                                                          Status.IDLE.value, output_dir, start, stop, output_flies)
        self.cur.execute(sql)

        self.db.commit()
        return self.cur.lastrowid

    def get_last_task_id(self):
        sql = "select max({}) from {};".format(
            __DB_COLUMN_ID__, self.table_tasks)
        res = self.cur.execute(sql)
        res = res.fetchone()

        if res[0]:
            return res[0]
        return 0

    def get_task(self, id):
        logging.info("Get task with id = {}".format(id))
        sql = __select_var__ .format(
            self.table_tasks, __TASK_COLUMN_ID__, id)
        res = self.cur.execute(sql)
        if res is None:
            raise Excep("The requested id = {} of task does not exist")
        colnames = self.cur.description
        output = {}
        res = res.fetchone()
        for i in range(len(colnames)):
            col_name = colnames[i][0]
            if col_name == __DB_COLUMN_ID__:
                output[col_name] = res[i]
            if col_name == __MODULE_COLUMN_ID__:
                output[col_name] = res[i]
            if col_name == __STATUS_COLUMN__:
                output[col_name] = res[i]
            if col_name == __OUTPUT_FOLDER_NAME_COLUMN__:
                output[col_name] = res[i]
            if col_name == __ARG_START__:
                output[col_name] = res[i]
            if col_name == __ARG_STOP__:
                output[col_name] = res[i]
            if col_name == __OUTPUT_FILES__:
                output[col_name] = res[i]
        return output

    def update_task_status(self, status, id):
        sql = "UPDATE {} SET {} = '{}' WHERE {} = {};".format(
            self.table_tasks, __STATUS_COLUMN__, status, __TASK_COLUMN_ID__, id)
        self.cur.execute(sql)
        self.db.commit()

    def delete_tasks_table(self):
        sql = "DROP TABLE {};".format(self.table_tasks)
        self.cur.execute(sql)

    def close_connection(self):
        self.db.close()


def rmdir(pth):
    """Delete a folder

    Args:
        pth (str): path of the folder
    """
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rmdir(child)
    pth.rmdir()


def read_json_file(path: Path):
    """Read json file

    Args:
        path (Path): file path

    Returns:
        json: data of the file 
    """
    with path.open() as data_file:
        data = json.load(data_file)
        return data


def clone_repo(url, db_manager: DBManager, orchestra_path):
    """Git clone and dokcer building

    Args:
        url (str): git repo url to be clone
        db_manager (DBManager): database manager
        orchestra_path (str): orchestra path where the database is stored and...

    Returns:
        json: response either it fails or it success
    """
    try:
        logging.info("Git Clone Starts...")
        repo_temp = os.path.join(orchestra_path, "repo_temp")
        if Path(repo_temp).exists():
            rmdir(repo_temp)
        git.Repo.clone_from(url, repo_temp)
        logging.info("Git Clone Ends...")
        for p in Path(repo_temp).iterdir():
            if p.name == METADATA_JSON_FILE_NAME:
                logging.info("Reading {}...".format(METADATA_JSON_FILE_NAME))
                data = read_json_file(p)
                data[__GIT_REPO_URL__] = url
                logging.info("Verification of {} Starts...".format(
                    METADATA_JSON_FILE_NAME))
                data = verify_metadata_json(data)
                logging.info("Verification of {} Ends...".format(
                    METADATA_JSON_FILE_NAME))
                return create_docker_file(data, db_manager, repo_temp)

        return {__json_data_key__: "{} is missing".format(METADATA_JSON_FILE_NAME), __json_type_key__: __json_error__}
    except Exception as e:
        logging.error(e)
        return {__json_data_key__: str(e), __json_type_key__: __json_error__}


def create_docker_file(metadata, db_manager, repo_temp):
    module = Module(metadata[__DB_COLUMN_NAME__], metadata[__DB_COLUMN_VERSION__], metadata[__DB_COLUMN_DESCRIPTION__],
                    metadata[__DEFAULTS__], metadata[__OUTPUT__], metadata[__ANNEXES_OUTPUT__], metadata[__INSTALL__], metadata[__GIT_REPO_URL__])

    logging.info("Creating a DockerFile...")
    docker_creator = DockerCreator()

    python_version = module.get_python_version()
    python_image = 'python:'+python_version  # + '-alpine'

    docker_creator.add_from(python_image)
    docker_creator.add_env('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python')
    docker_creator.add_run('pip install --upgrade pip')
    docker_creator.add_workdir_copy('/usr/src/app')
    docker_creator.add_run(
        'pip install --no-cache-dir -r ./{}'.format(module.get_requirements()))  # requirements.txt

    exec_file = module.get_executable()
    docker_creator.add_exec('["python" , "./'+exec_file + '.py" ]')

    docker_creator.write_docker_file(repo_temp)
    try:
        docker_creator.init_docker_client()
    except Exception as e:
        return {__json_data_key__: str(e), __json_type_key__: __json_error__}

    version = module.version
    name = module.name

    if db_manager.check_if_model_exists(name, version):
        msg = "The module already exists"
        logging.warn(msg)
        return {__json_data_key__: msg, __json_type_key__: __json_warning__}

    try:
        streamer = docker_creator.build_image(
            repo_temp, tag=module.get_image_tag())
    except Exception as e:
        logging.error(e)
        return {__json_data_key__: str(e), __json_type_key__: __json_error__}

    return {__json_data_key__: (streamer, module), __json_type_key__: __json_info__}


class Excep(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def verify_metadata_json(data):
    """Verify the data according to the reference 'metadata.json'

    Args:
        data (json): metadata.json of a module

    Raises:
        Excep: if a required field is missing

    Returns:
        json: a cleaned metadata.json
    """
    output = data
    missing = "is missing in {} ".format(METADATA_JSON_FILE_NAME)
    if __DB_COLUMN_NAME__ not in data:
        msg = "{} {}".format(__DB_COLUMN_NAME__, missing)
        logging.error(msg)
        raise Excep(msg)
    elif not data[__DB_COLUMN_NAME__].strip():
        msg = "{} is empty".format(__DB_COLUMN_NAME__)
        logging.error(msg)
        raise Excep(msg)

    if __DB_COLUMN_DESCRIPTION__ not in data:
        msg = "{} {}".format(__DB_COLUMN_DESCRIPTION__, missing)
        logging.warn(msg)
        output[__DB_COLUMN_DESCRIPTION__] = ""

    if __DB_COLUMN_VERSION__ not in data:
        msg = "{} {}".format(__DB_COLUMN_VERSION__, missing)
        logging.warn(msg)
        output[__DB_COLUMN_VERSION__] = "1.0.0"

    if __DEFAULTS__ not in data:
        msg = "{} {}".format(__DEFAULTS__, missing)
        logging.warn(msg)
        output[__DEFAULTS__] = {
            __ARG_START__: "2008-07-03T00:00:00",
            __ARG_STOP__: "2008-07-05T23:59:00"
        }

    if __OUTPUT__ not in data:
        msg = "{} {}".format(__OUTPUT__, missing)
        logging.error(msg)
        raise Excep(msg)

    if __ANNEXES_OUTPUT__ not in data:
        msg = "{} {}".format(__ANNEXES_OUTPUT__, missing)
        output[__ANNEXES_OUTPUT__] = []
        logging.warn(msg)

    if __INSTALL__ not in data:
        msg = "{} {}".format(__INSTALL__, missing)
        logging.error(msg)
        raise Excep(msg)
    else:
        if __MODEL_VERSION__ not in data[__INSTALL__]:
            output[__INSTALL__][__MODEL_VERSION__] = "1.0.0"
            msg = "{} {}".format(__MODEL_VERSION__, missing)
            logging.warn(msg)

        if __PYTHON_VERSION__ not in data[__INSTALL__]:
            msg = "{} {}".format(__PYTHON_VERSION__, missing)
            logging.error(msg)
            raise Excep(msg)

        if __REQUIREMENTS__ not in data[__INSTALL__]:
            output[__INSTALL__][__REQUIREMENTS__] = __REQUIREMENTS__+".txt"
            msg = "{} {}".format(__REQUIREMENTS__, missing)
            logging.error(msg)
            raise Excep(msg)
        else:
            if not data[__INSTALL__][__REQUIREMENTS__]:
                output[__INSTALL__][__REQUIREMENTS__] = __REQUIREMENTS__+".txt"
                msg = "{} {}".format(__REQUIREMENTS__, "Is empty")
                logging.warn(msg)

        if __FILES__ not in data[__INSTALL__]:
            output[__INSTALL__][__FILES__] = []
            msg = "{} {}".format(__FILES__, missing)
            logging.warn(msg)

        if __EXECUTABLE__ not in data[__INSTALL__]:
            msg = "{} {}".format(__EXECUTABLE__, missing)
            logging.error(msg)
            raise Excep(msg)

        if __PRE_PROCESS__ not in data[__INSTALL__]:
            output[__INSTALL__][__PRE_PROCESS__] = []
            msg = "{} {}".format(__PRE_PROCESS__, missing)
            logging.warn(msg)

        if __POST_PROCESS__ not in data[__INSTALL__]:
            output[__INSTALL__][__POST_PROCESS__] = []
            msg = "{} {}".format(__POST_PROCESS__, missing)
            logging.warn(msg)
    return output


def format_module(res, colnames, annexes, annexes_colnames):
    module_temp = {}
    output_module = {}
    defaults_module = {}
    install_module = {}
    annexes_module = []
    for i in range(len(colnames)):
        col_name = colnames[i][0]
        # output key
        if col_name == __DB_COLUMN_OUTPUT_TYPE__:
            output_module[col_name] = res[i]
        elif col_name == __DB_COLUMN_OUTPUT_FILENAME__:
            output_module[col_name] = res[i]

        # defaults key
        elif col_name == __DB_COLUMN_DEFAULTS_ARG_START__:
            defaults_module[col_name] = res[i]
        elif col_name == __DB_COLUMN_DEFAULTS_ARG_STOP__:
            defaults_module[col_name] = res[i]

        # install key
        elif col_name == __MODEL_VERSION__:
            install_module[col_name] = res[i]
        elif col_name == __PYTHON_VERSION__:
            install_module[col_name] = res[i]
        elif col_name == __REQUIREMENTS__:
            install_module[col_name] = res[i]
        elif col_name == __FILES__:
            install_module[col_name] = json.loads(res[i])
        elif col_name == __EXECUTABLE__:
            install_module[col_name] = res[i]
        elif col_name == __PRE_PROCESS__:
            install_module[col_name] = json.loads(res[i])
        elif col_name == __POST_PROCESS__:
            install_module[col_name] = json.loads(res[i])
        else:
            module_temp[colnames[i][0]] = res[i]

    if annexes:
        for a in range(len(annexes)):
            row = annexes[a]
            data_temp = {}
            for i in range(len(annexes_colnames)):
                col_name = annexes_colnames[i][0]
                if col_name == __DB_COLUMN_OUTPUT_TYPE__:
                    data_temp[col_name] = row[i]
                if col_name == __DB_COLUMN_OUTPUT_FILENAME__:
                    data_temp[col_name] = row[i]
            annexes_module.append(data_temp)

    module_temp[__OUTPUT__] = output_module
    module_temp[__DEFAULTS__] = defaults_module
    module_temp[__ANNEXES_OUTPUT__] = annexes_module
    module_temp[__INSTALL__] = install_module

    return module_temp


def test_upload_module(db_m: DBManager):
    metadata_json = {
        "name": "",
        "description": "relative path to description.md",
        "version": "",
        "args": [
            "start",
            "stop"
        ],
        "defaults": {
            "start": "2008-07-03T00:00:00",
            "stop": "2008-07-05T23:59:00"
        },
        "output": {
            "type": "TT",
            "filename": "TT.csv"
        },
        "annexes_outputs": [{
            "type": "TS",
            "filename": "TS.csv"
        }, {"type": "IMAGE",
            "filename": "IMAGE.png"}],
        "install": {
            "model_version": "500",
            "python_version": "3.12",
            "requirements": "requirements.txt",
            "files": [
                "a.py", "b.py"
            ],
            "executable": "run.py",
            "pre_process": [],
            "post_process": []
        }
    }

    metadata = verify_metadata_json(metadata_json)
    module = Module(metadata[__DB_COLUMN_NAME__], metadata[__DB_COLUMN_VERSION__], metadata[__DB_COLUMN_DESCRIPTION__],
                    metadata[__DEFAULTS__], metadata[__OUTPUT__], metadata[__ANNEXES_OUTPUT__], metadata[__INSTALL__])
    db_m.add_module(module)

    return db_m.get_modules()[-1]
