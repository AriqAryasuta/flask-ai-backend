import vertexai

class VertexModel:
    def __init__(self):
        self.projectid = "perceptive-ivy-388"
        self.region = "us-central1"

        vertexai.init(project=self.projectid, location=self.region)

ai = VertexModel()