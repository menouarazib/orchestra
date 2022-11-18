from enum import Enum


METADATA_JSON_FILE_NAME = "metadata.json"

__docker_message__ = "docker"
__running_message__ = "running"
__db_message__ = "db"
__import_build__ = "build"
__rebuild__ = "rebuild"
__import_build_url__ = "url"
__json_info__ = "INFO"
__json_warning__ = "WARNING"
__json_error__ = "ERROR"
__json_data_key__ = "data"
__json_type_key__ = "type"
__stream_docker_key__ = "stream"
__task_id__ = "task"

__ARG_START__ = "start"
__ARG_STOP__ = "stop"

__DEFAULTS__ = "defaults"
__OUTPUT__ = "output"
__ANNEXES_OUTPUT__ = "annexes_outputs"
__INSTALL__ = "install"
__MODEL_VERSION__ = "model_version"
__PYTHON_VERSION__ = "python_version"
__REQUIREMENTS__ = "requirements"
__EXECUTABLE__ = "executable"
__PRE_PROCESS__ = "pre_process"
__POST_PROCESS__ = "post_process"
__FILES__ = "files"


__DB_COLUMN_ID__ = "id"
__DB_COLUMN_NAME__ = "name"
__DB_COLUMN_DESCRIPTION__ = "description"
__DB_COLUMN_TAG__ = "image_docker_tag"
__DB_COLUMN_VERSION__ = "version"
__DB_COLUMN_DEFAULTS_ARG_START__ = __ARG_START__
__DB_COLUMN_DEFAULTS_ARG_STOP__ = __ARG_STOP__
__DB_COLUMN_OUTPUT_TYPE__ = "type"
__DB_COLUMN_OUTPUT_FILENAME__ = "filename"


__TASK_COLUMN_ID__ = "id"
__MODULE_COLUMN_ID__ = "moduleId"
__STATUS_COLUMN__ = "status"
__OUTPUT_FOLDER_NAME_COLUMN__ = "output_dir"
__OUTPUT_FILES__ = "output_files"
__GIT_REPO_URL__ = "git_url"

__TypeError__ = "TypeError"


class Status(Enum):
    """Status Class for task

    Args:
        Enum (str): task status
    """
    DONE = "done"
    RUNNING = "running"
    FAIL = "fail"
    IDLE = "idle"
