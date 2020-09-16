# -*- coding: utf-8 -*-

def response_dictionary(status=None, msg=None, results=None):
    """
    Generamos los diferentes valores de la request a devolver para todas las apis
    """
    data = {}
    if status is not None and msg is not None and results is not None:
        data = {
            'status': status,
            'msg': msg,
            'results': results,
        }

    return data