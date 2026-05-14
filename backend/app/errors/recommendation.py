class ColdStartError(Exception):
    def __init__(self, min_samples: int):
        self.min_samples = min_samples
        super().__init__(f"Not enough rated vehicles (min {min_samples})")
