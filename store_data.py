import json


class StoreData:
    """
    Store data.
    """

    def __init__(self, ai_game) -> None:
        """
        Initialize store data.
        """
        self.settings = ai_game.settings
        self.storage = self.settings.storage_path

    
    def store_top_score(self, score):
        """
        Store top score to a json file.
        """
        with open(self.storage) as json_data:
            data = json.load(json_data)
            data["top_score"] = score

        with open(self.storage, "w") as json_data:
            json.dump(data, json_data)

    
    def read_top_score(self):
        """
        Read and return top score from DB.
        """
        with open(self.storage) as json_data:
            data = json.load(json_data)
        return data["top_score"]