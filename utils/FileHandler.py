import re


class TextHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.finding_result = []

    # def __del__(self):
    #     self.f.close()

    def find(self, pattern):
        with open(self.file_path, "r") as f:
            self.content = f.read()
        self.finding_result = re.findall(pattern, self.content)
        return self.finding_result

    def append(self, content):
        content = "\n" + content
        with open(self.file_path, "a") as f:
            f.write(content)
        self.content += content

    def update(self, origin, content):
        with open(self.file_path, "w") as f:
            f.write(self.content.replace(origin, content))

    def delete(self, origin):
        self.update(origin, "")
