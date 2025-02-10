from bson import ObjectId



async def convert_str_object_id(ids:list):
    return [ ObjectId(id) for id in ids]