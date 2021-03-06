import io
import os
import uuid
import mimetypes

import falcon
import msgpack

from .RandomTestApp import ReturnFileName

#waitress-serve --port=8000 look:app.api

class Resource(object):

    _CHUNK_SIZE_BYTES = 4096

    
    def __init__(self, storage_path):
        self._storage_path = storage_path


    def on_get(self, req, resp):
        resp.body = ReturnFileName()
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        ext = mimetypes.guess_extension(req.content_type)
        name = '{char}{ext}'.format(char="temp", ext=ext)
        image_path = os.path.join(self._storage_path, name)

        with io.open(image_path, 'wb') as image_file:
            while True:
                chunk = req.stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        resp.status = falcon.HTTP_201
        resp.location = '/images/' + name