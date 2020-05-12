import yaml
import logging

class YamlLoadable:
    # __load__, is the method which loads class attributes from given dictionary
    def __load__(self, d: dict):
        pass

class StageEvent(YamlLoadable):
    def __init__(self, type="any"):
        self.type: str = type

    def __load__(self, d: dict):
        d.setdefault("commands", [])
        self.commands: [str] = d["commands"]


class StageEventPass(StageEvent):
    def __init__(self):
        super().__init__("pass")

    def __load__(self, d: dict):
        super().__load__(d)


class StageEventFail(StageEvent):
    def __init__(self):
        super().__init__("fail")

    def __load__(self, d: dict):
        super().__load__(d)


"""
Represents stage in pipeline
"""


class Stage(YamlLoadable):
    def __init__(self, name: str):
        self.name = name

    def __load__(self, d: dict):
        d.setdefault("post", [])
        d.setdefault("pre", [])
        d.setdefault("continue", "auto")
        d.setdefault("essential", True)
        d.setdefault("commands", [])
        d.setdefault("status", {})

        self.type: str = d["type"]
        self.agent: str = d["agent"]
        self.post: [str] = d["post"]
        self.pre: [str] = d["pre"]
        self.essential: str = d["essential"]
        self.continue_method: str = d["continue"]
        self.commands: [str] = d["commands"]
        self.status: [StageEvent] = []
        for status_event in d["status"].keys():
            eve: StageEvent = StageEvent()
            if status_event == "pass":
                eve = StageEventPass()
            elif status_event == "fail":
                eve = StageEventFail()
            # just me make code coherent
            eve.__load__({"commands": d["status"][status_event]})
            self.status.append(eve)


"""
DockerImage, represents docker image part of the style
"""
class DockerImage:
    def __init__(self, name):
        self.name: str = name

    def __load__(self, d: dict):
        d.setdefault("tag", "latest")
        d.setdefault("file", "")
        d.setdefault("args", [])
        d.setdefault("runargs", [])
        d.setdefault("commands", [])

        self.tag = d["tag"]
        self.file = d["file"]
        self.args = d["args"]
        self.runargs = d["runargs"]
        # commands, behaves according to the stage it has put in
        self.commands = d["commands"]


"""
It's the base class for all the classes, using DockerImage in their configuration
It will work as super class for test and build stage
"""


class DockerImageUsingStage(Stage):
    def __init__(self):
        self.images: [DockerImage] = []

    def __load__(self, d: [dict]):
        super().__load__(d)
        d.setdefault("images", {})

        for x in d["images"].keys():
            i = DockerImage(x)
            i.__load__(d["images"][x])
            self.images.append(i)


class DockerComposeService(YamlLoadable):
    def __init__(self):
        pass

    def __load__(self, d: dict):
        d.setdefault("args", [])
        d.setdefault("runargs", [])
        # Dfault compose file commands
        d.setdefault("file", "docker-compose.yml")
        self.args: [str] = d["args"]
        self.runargs: [str] = d["runargs"]
        self.file: str = d["file"]


"""
BuildStage represents a build stage
"""


class BuildStage(DockerImageUsingStage):
    def __init__(self, name: str):
        self.name = name
        super().__init__()

    def __load__(self, d: dict):
        super().__load__(d)


"""
TestStage represents a test stage
"""


class TestStage(DockerImageUsingStage):
    def __init__(self, name):
        self.name = name
        super().__init__()

    def __load__(self, d: dict):
        super().__load__(d)
        d.setdefault("compose", {})
        self.compose = DockerComposeService()
        self.compose.__load__(d["compose"])


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
        # self.build_stages: [BuildStage] = []
        # self.test_stages = []
        # self.deploy_stages = []
        # self.arbitrary_stage = []
        self.continue_method = "auto"

    def parse(self):
        # Parses the yaml stream supplied
        p = yaml.load(self.yamlstream, Loader=yaml.FullLoader)

        if "continue" in p:
            # overriding default behaviour
            self.continue_method = p["continue"]

        for stage_name in p["stages"]:
            stage_dump: dict = p[stage_name]
            stage_dump.setdefault("type", "any")
            stage: Stage = Stage(stage_name)
            if stage_dump["type"] == "build":  # Appening Build stage
                stage = BuildStage(stage_name)
            elif stage_dump["type"] == "test":  # Appending Test Stage
                stage = TestStage(stage_name)
            stage.__load__(stage_dump)
            self.stages.append(stage)
