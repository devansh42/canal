import yaml
import logging


class YamlLoadable:
    # __load__, is the method which loads class attributes from given dictionary
    def __load__(self, d: dict):
        pass


"""
Represents stage in pipeline
"""


class Stage(YamlLoadable):
    def __init__(self, name: str):
        self.name = name

    def __load__(self, d: dict):
        d.setdefault("post", [])
        d.setdefault("pre", [])

        self.type = d["type"]
        self.agent = d["agent"]
        self.post = d["post"]
        self.pre = d["pre"]


class BuildStage(Stage):
    def __init__(self):
        self.images: [DockerImage] = []

    def __load__(self, d: dict):
        super().__load__(d)
        d.setdefault("images", {})

        for x in d["images"].keys():
            i = DockerImage(x)
            i.__load__(d["images"][x])
            self.images.append(i)


class DockerImage:
    def __init__(self, name):
        self.name: str = name

    def __load__(self, d: dict):
        d.setdefault("tag", "latest")
        d.setdefault("file", "Dockerfile")
        d.setdefault("args", [])
        self.tag = d["tag"]
        self.file = d["file"]
        self.args = d["args"]


"""
Represents a pipeline
"""


class Pipeline:

    """
    stream is the stream containing yaml stream
    """

    def __init__(self, stream):
        self.yamlstream = stream
        self.stages: [Stage] = []
        self.build_stages: [BuildStage] = []
        self.test_stages = []
        self.deploy_stages = []
        self.arbitrary_stage = []

    def parse(self):
        # Parses the yaml stream supplied
        p = yaml.load(self.yamlstream, Loader=yaml.FullLoader)
        for stage_name in p["stages"]:
            stage_dump = p[stage_name]
            stage = Stage(stage_name)
            stage.__load__(stage_dump)
            self.stages.append(stage)
            if stage.type == "build":  # Appening Build stage
                build_stage = BuildStage()
                build_stage.name = stage.name
                build_stage.__load__(stage_dump)
                self.build_stages.append(build_stage)
