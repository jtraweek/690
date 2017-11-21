
from flask_uploads import UploadSet
from werkzeug.datastructures import FileStorage
from wtforms.validators import StopValidation


class ExtensionAllowed(object):
    """
    A form validator.
    Takes an iterable or upload set and checks that an uploaded file is
    of a supported file format.
    """
    def __init__(self, upload_set, message=None):
        if isinstance(upload_set, UploadSet):
            self.extensions = set(upload_set.extensions)
        else:
            self.extensions = set(upload_set)
        self.message = message

    def __call__(self, form, field):

        if not (isinstance(field.data, FileStorage) and field.data):
            return

        filename    = field.data.filename.lower()
        extensions  = set( map(str.lower, self.extensions) )

        if any(filename.endswith('.' + x) for x in extensions):
            return

        message = ( self.message or
                        field.gettext(
                            'File does not have an approved extension: ' +
                            str.join(', ', extensions)) )
        #
        raise StopValidation( message )
