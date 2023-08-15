
def update_cached_data(mongoDataBase):
    query = {'_id': 0, 'testimonials': 1}
    return mongoDataBase.get_document(database_name='site', collection_name='portfolio',
                                      query=query)
