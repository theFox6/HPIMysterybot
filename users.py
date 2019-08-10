all = {} 

def create(id, name):
    all[id] = {
        'name': name
    }

def migrateUser(oldID, newID):
    all[newID] = all[oldID]
    del all[oldID]
