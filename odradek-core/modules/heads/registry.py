import config

class Head:
    def __init__(self, name, description="", status="ready"):
        self.name = name
        self.description = description
        self.status = status

class HeadRegistry:
    """Registry of all Odradek head types."""

    def __init__(self):
        self.heads = {}
        self._register_defaults()
        self.current = self.heads.get(config.ACTIVE_HEAD, list(self.heads.values())[0])

    def _register_defaults(self):
        specs = {
            "camera": "RGB camera for object detection and tracking",
            "flashlight": "High-power field illumination",
            "lidar": "3D distance scanning",
            "satellite": "Positioning / comms uplink",
            "sampler": "Environmental sample collection",
            "hand": "Manipulator for handling gadgets",
            "head_7": "TBD", "head_8": "TBD", "head_9": "TBD",
            "head_10": "TBD", "head_11": "TBD", "head_12": "TBD",
        }
        for name, desc in specs.items():
            self.heads[name] = Head(name, desc)

    def select(self, name):
        if name in self.heads:
            self.current = self.heads[name]
            return True
        return False

    def list_heads(self):
        return list(self.heads.keys())

    def get(self, name):
        return self.heads.get(name)
