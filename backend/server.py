
from flask import Flask, request, redirect, copy_current_request_context, url_for
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from flask.globals import request
import logging
import os
import json
from threading import Thread
from pathlib import Path
from src.utils.utils import DBManager, clone_repo, DockerCreator, test_upload_module
from src.utils.constant import __docker_message__, __import_build__, __db_message__, __json_data_key__,\
    __stream_docker_key__, __json_info__, __json_warning__, __json_type_key__, __import_build_url__,\
    __DB_COLUMN_DESCRIPTION__, __DB_COLUMN_ID__, __DB_COLUMN_NAME__, __DB_COLUMN_TAG__, \
    __DB_COLUMN_VERSION__, __running_message__, __task_id__, Status, __ARG_START__, __ARG_STOP__, __OUTPUT__, __STATUS_COLUMN__,\
    __DB_COLUMN_OUTPUT_FILENAME__, __MODULE_COLUMN_ID__, __OUTPUT_FOLDER_NAME_COLUMN__, __DB_COLUMN_TAG__, __OUTPUT_FILES__, __TypeError__, __json_error__,\
    __rebuild__, __GIT_REPO_URL__


orchestra_path = Path(".").resolve().parents[0]
__database_path__ = os.path.join(orchestra_path, "data/database.db")
__tasks_output_path__ = os.path.join(orchestra_path, "tasksoutput")

db_manger = DBManager(__database_path__)


# Initializing flask app
app = Flask(__name__, static_folder=__tasks_output_path__,
            static_url_path=__tasks_output_path__)

app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'

CORS(app)
socketIo = SocketIO(app, cors_allowed_origins="*")

logging.info("Static Folder of the App is {}".format(app.static_url_path))


@socketIo.on(__docker_message__)
def handle_message_from_client(msg):
    """Handle a recieved message from a connected client using socket, this routine listens on the __docker_message__


    Args:
        msg (_type_): recieved message 

    Returns:
        json: None
    """
    send(msg, broadcast=True)
    return None


@socketIo.on(__running_message__)
def handle_message_from_client_(msg):
    """Handle a recieved message from a connected client using socket, this routine listens on the __running_message__


    Args:
        msg (_type_):  recieved message 

    Returns:
        json: None
    """
    send(msg, broadcast=True)
    return None


def emit_messages_to_client(streamer):
    """Emit messages to all connected clients who are listening on __docker_message__


    Args:
        streamer (CancellableStream): the streamer returned by docker building image process
    """
    for chunk in streamer:
        for line in chunk.decode("utf-8").splitlines():
            step = json.loads(line)

        if __stream_docker_key__ in step:
            msg = step[__stream_docker_key__]
            type_msg = __json_info__
            if __json_warning__ in msg:
                type_msg = __json_warning__
            if __TypeError__ in msg:
                type_msg = __json_error__
            emit(__docker_message__, {__json_data_key__: msg, __json_type_key__: type_msg},
                 namespace='/', broadcast=True)


@app.route('/'+__import_build__+'/')
def clone_process():
    """Clone the git repositiry of current module and build its docker image


    Returns:
        json: response either it fails or it success
    """
    url = request.args.get(__import_build_url__, None)
    logging.info("The Git Url to Clone is {}".format(url))
    emit(__docker_message__, {__json_data_key__: "Git Clone Process is Starting...", __json_type_key__: __json_info__},
         namespace='/', broadcast=True)
    response = clone_repo(url, db_manger, orchestra_path)
    emit(__docker_message__, {__json_data_key__: "Git Clone Process is Ending...", __json_type_key__: __json_info__},
         namespace='/', broadcast=True)
    if response[__json_type_key__] == __json_info__:
        streamer, module = response[__json_data_key__]
        try:
            logging.info("Docker Building Image Starts...")
            emit_messages_to_client(streamer)
            logging.info("Docker Building Image Ends...")
        except Exception as e:
            logging.error(e)
            return {__json_data_key__: str(e), __json_type_key__: __json_error__}

        return db_manger.add_module(module)
    else:
        return response


@app.route('/'+__rebuild__+'/<id>')
def rebuild_module(id):
    """Rebuild the module 
    Args:
        id (_type_): module id

    Returns:
        json: response either it fails or it success
    """
    logging.info("Prepare for Rebuilding the module with id {}".format(id))
    module = db_manger.get_module(id)
    git_url = module[__GIT_REPO_URL__]
    db_manger.delete_module(id)
    return redirect(url_for("clone_process", url=git_url))


@app.route('/testmetadatajson')
def test_umpload_metadata():
    return test_upload_module(db_manger)


@app.route('/modules')
def get_modules():
    """Get the installed modules from the database


    Returns:
        list: list of all modules
    """

    modules = db_manger.get_modules()
    return modules


@app.route('/modules/<id>')
def get_module_info(id):
    """Get a module from the database based on a given id


    Args:
        id (int): module id

    Returns:
        Module: module
    """
    return db_manger.get_module(id)


@app.route('/modules/<id>/run')
def run(id):
    """Prepare the module associated with a given id for running

    Args:
        id (int): id of module to be run

    See:
        run_module

    Returns:
        json: a task 
    """
    # get module for given id
    module = db_manger.get_module(id)

    @copy_current_request_context
    def run_module_inner(task):
        db_manger.update_task_status(Status.RUNNING.value, task)
        logging.info(
            "The Module associated with task, id = {} is running".format(task))
        run_module(task)

    start = request.args.get(__ARG_START__, None)
    stop = request.args.get(__ARG_STOP__, None)
    output_dir = "output"+str(db_manger.get_last_task_id()+1)
    output_files = module[__OUTPUT__][__DB_COLUMN_OUTPUT_FILENAME__]
    task_id = db_manger.add_task(id, start, stop, output_dir, output_files)
    logging.info("A new task is created, id = {}".format(task_id))

    response = {}
    response[__task_id__] = task_id
    response[__STATUS_COLUMN__] = Status.IDLE.value
    response[__OUTPUT__] = [output_files]

    thread = Thread(target=run_module_inner, kwargs={__task_id__: task_id})
    thread.start()
    return response


def format_task(task):
    response = {}
    response[__task_id__] = task[__DB_COLUMN_ID__]
    response[__STATUS_COLUMN__] = task[__STATUS_COLUMN__]
    response[__OUTPUT__] = [task[__OUTPUT_FILES__]]
    return response


def run_module(task_id):
    """Run a module associated with given task  id

    Args:
        task_id (int): task id

    See:
        run
    """
    dc = DockerCreator()
    dc.init_docker_client()
    logging.info("Initializing a Docker Client...")
    task_from_db = db_manger.get_task(task_id)

    output_dir_task = "/{}".format(task_from_db[__OUTPUT_FOLDER_NAME_COLUMN__])

    command = " {} --{} {} --{} {}".format(output_dir_task, __ARG_START__,
                                           task_from_db[__ARG_START__], __ARG_STOP__, task_from_db[__ARG_STOP__])

    module_id = task_from_db[__MODULE_COLUMN_ID__]
    module = db_manger.get_module(module_id)
    logging.info("Creating a Docker Container...")
    streamer = dc.create_container(
        module[__DB_COLUMN_TAG__], command=command, output_dir=output_dir_task)
    for chunk in streamer:
        for line in chunk.decode("utf-8").splitlines():
            key = __json_info__
            if __TypeError__ in line:
                key = __json_error__
                logging.error(line)
            emit(__running_message__, {__json_data_key__: line, __json_type_key__: key},
                 namespace='/', broadcast=True)

    db_manger.update_task_status(Status.DONE.value, task_id)

    emit(__running_message__, {__json_data_key__: "The Model was Successfully Run", __json_type_key__: __json_warning__},
         namespace='/', broadcast=True)

# use this after_this_request


@app.route('/tasks/<id>')
def get_task(id):
    """Get Task for given id

    Args:
        id (int): task id

    Returns:
        json: task
    """
    task = db_manger.get_task(id)
    return format_task(task)


@app.route('/tasks/<id>/output')
def get_task_output(id):
    """Get the result of task 

    Args:
        id (int): task id

    Returns:
        file: file containing the result of the task
    """
    task_from_db = db_manger.get_task(id)
    path = task_from_db[__OUTPUT_FOLDER_NAME_COLUMN__] + \
        "/"+task_from_db[__OUTPUT_FILES__]
    logging.info('The File to be Downloaded is {}'.format(path))
    try:
        return app.send_static_file(path)
    except Exception as e:
        logging.error(e)
        return {__json_data_key__: str(e), __json_type_key__: __json_error__}


@app.route("/")
def root():
    return redirect("http://localhost:3000/", code=302)


# Running app
if __name__ == '__main__':
    socketIo.run(app)
