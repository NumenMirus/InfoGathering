import json

class MsTable:
    div_id = ""
    rows = []

    def __init__(self, div_id, rows):
        self.div_id = div_id
        self.rows = rows

    def __str__(self):
        return ("div_id: {div_id}\nrows: {rows}".format(div_id = self.div_id, rows = self.rows))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class MsTab:
    name = ""
    query_bit = ""
    searched = []

    def __init__(self, name, query_bit, searched):
        self.name = name
        self.query_bit = query_bit
        self.searched = searched

    def __str__(self):
        return ("name: {name}\nquery_bit: {query_bit}\nsearched: {searched}".format(name = self.name, query_bit = self.query_bit, searched = self.searched))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)