from typing import List, Dict, Any
from pymongo.cursor import Cursor
from pymongo.collection import Collection
from app.utils.convert_bson_id_str import convert_objectids_list


async def check_has_pre_next(
    collection: Collection,
    query: Dict[str, Any],
    content_per_page: int,
    current_page: int,
) -> Dict[str, bool]:
    document_cursor = collection.find(query)
    total_number_of_documents = await document_cursor.to_list()

    current_count = current_page * content_per_page

    has_next = True if current_count < len(total_number_of_documents) else None
    has_pre = True if current_page > 1 else None
 
    result = {
       
        "has_previous": has_pre,
        "has_next": has_next,
        "total" : len(total_number_of_documents)
    }

    return result


async def paginate_query(
    query: Dict[str, Any],
    exclude_fields: Dict[str, int],
    page: int,
    per_page: int,
    collection: Collection,
) -> List[Dict[str, Any]]:
    """
    returns paginated response of a collection
    """
    skip = (page - 1) * per_page
    document_cursor_obj = (
        collection.find(query, exclude_fields).skip(skip).limit(per_page)
    )
    document_list = await document_cursor_obj.to_list(length=per_page)
    

    data = await convert_objectids_list(document_list)
    has_next_or_prev = await check_has_pre_next(
        query=query, collection=collection, content_per_page=per_page, current_page=page
    )
    response = {**has_next_or_prev, "data": data}
    return response
