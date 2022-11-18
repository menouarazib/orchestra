
from docker import APIClient
import os
import logging


class DockerCreator:
    """A class in order to create a DockerFile, docker image and docker container 
    """

    def __init__(self):
        self.content = ''
        self.client = None

    def add_empty_line(self):
        self.content += '\n'

    def add_from(self, python_image):
        self.add_empty_line()
        self.content += 'FROM '+python_image

    def add_workdir_copy(self, work_dir):
        self.add_empty_line()
        self.content += 'WORKDIR '+work_dir
        self.add_empty_line()
        self.content += 'COPY . ./'

    def add_run(self, script):
        self.add_empty_line()
        self.content += 'RUN '+script

    def add_exec(self, cmds):
        self.add_empty_line()
        self.content += 'ENTRYPOINT '+cmds

    def add_env(self, env):
        self.add_empty_line()
        self.content += 'ENV '+env

    def write_docker_file(self, repo):
        dockerfile_path = os.path.join(repo, "Dockerfile")
        text_file = open(dockerfile_path, "w")
        text_file.write(self.content)
        text_file.close()

    def init_docker_client(self):
        self.client = APIClient(base_url='unix://var/run/docker.sock')

    def build_image(self, path_to_dockerfile, tag):
        try:
            res = self.client.build(
                path=path_to_dockerfile, tag=tag, rm=True, decode=False)
            return res
        except Exception as e:
            logging.error(e)
            raise e

    def create_container(self, image, command, output_dir):
        volumes = [output_dir]

        host_config = self.client.create_host_config(binds={
            "/home/orchestra/tasksoutput/"+output_dir: {
                'bind': output_dir,
                'mode': 'rw'
            }
        })

        container = self.client.create_container(
            image=image, command=command, detach=True, volumes=volumes, host_config=host_config)
        container_id = container.get('Id')
        logging.info("Docker's Container is Starting...")
        self.client.start(container_id)
        streamer = self.client.logs(
            container=container_id,  stream=True, tail=1)
        return streamer
