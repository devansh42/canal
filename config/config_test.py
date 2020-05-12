import logging
import os.path as path
import unittest
from config import Pipeline,BuildStage


class PipelineParserTestCase(unittest.TestCase):
    def setUp(self):
        abs = path.join(path.dirname(__file__), "final.yaml")
        with open(abs) as f:
            self.pipeline = Pipeline(f)
            self.pipeline.parse()

    def testParsing(self):
        p = self.pipeline
        for x in p.build_stages:
            for y in x.images:
                logging.info(y.file)
            logging.info(x.images)
            logging.info(x.type)
            logging.info(x.pre)
            logging.info(x.post)
            logging.info(x.name)


if __name__ == "__main__":
    unittest.main()
