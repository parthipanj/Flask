class DocumentService:

    def __init__(self, db, collection):
        self.collection = db[collection]

    def find(self, query=None, projection=None, skip: int = 0, limit: int = 0):
        return list(self.collection.find(query, projection).skip(skip).limit(limit))

    def find_one(self, query, projection=None):
        return self.collection.find_one(query, projection)

    def count(self, query=None):
        return self.collection.find(query).count()

    def insert_one(self, document):
        return self.collection.insert_one(document)

    def update_one(self, filter_query, update):
        return self.collection.update_one(filter_query, {'$set': update})

    def delete_one(self, filter_query):
        return self.collection.delete_one(filter_query)
