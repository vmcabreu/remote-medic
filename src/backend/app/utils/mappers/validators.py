def validate_json(data, required_fields=None):
    if not data:
        return False
    if required_fields:
        return all(field in data for field in required_fields)
    return True

def validate_pagination_params(page, per_page):
    return page > 0 and 1 <= per_page <= 100

