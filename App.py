import falcon
import mimetypes
import io
import uuid
import os


class ResourceClass(object):
    
    _CHUNK_SIZE_BYTES = 4096
    
    def __init__(self, storage_path):
        self._storage_path= storage_path
    
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = ("-recognized character-")

    def on_post(self, req, resp):
        ext = mimetypes.guess_extension(req.content_type)
        name = '{uuid}{ext}'.format(uuid=uuid.uuid4(),ext = ext)
        image_path = os.path.join(self._storage_path, name)

        with io.open(image_path,'wb') as image_file:
            while True:
                chunk = req.stream.read(self._CHUNK_SYZE_BYTES)
                if not chunk:
                    break
                
                image_file.write(chunk)

            resp.status = falcon.HTTP_201
            resp.location = '/images/' + name

api = falcon.API()
testing = ResourceClass()
api.add_route('/', ResourceClass())