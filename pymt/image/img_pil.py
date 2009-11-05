'''
PIL: PIL image loader
'''

__all__ = ('ImageLoaderPIL', )

from . import ImageLoaderBase, ImageData
from ..logger import pymt_logger

try:
    import PIL.Image
except:
    raise

# Use PIL to load image.
class ImageLoaderPIL(ImageLoaderBase):
    '''Image loader based on PIL library'''

    @staticmethod
    def extensions():
        '''Return accepted extension for this loader'''
        # retrieve from http://www.pythonware.com/library/pil/handbook/index.htm
        return ('bmp', 'bufr', 'cur', 'dcx', 'eps', 'fits', 'fl', 'fpx', 'gbr',
                'gd', 'gif', 'grib', 'hdf5', 'ico', 'im', 'imt', 'iptc', 'jpeg',
                'jpg', 'mcidas', 'mic', 'mpeg', 'msp', 'palm', 'pcd', 'pcx', 'pdf',
                'pixar', 'png', 'ppm', 'psd', 'sgi', 'spider', 'tga', 'tiff',
                'wal', 'wmf', 'xbm', 'xpm', 'xv')

    def load(self, filename):
        pymt_logger.debug('Load <%s>' % filename)
        try:
            im = PIL.Image.open(filename)
        except:
            pymt_logger.warning('Unable to load image <%s>' % filename)
            raise

        # image loader work only with rgb/rgba image
        if im.mode not in ('RGB', 'RGBA'):
            try:
                imc = im.convert('RGBA')
            except:
                pymt_logger.warning(
                    'Unable to convert image <%s> to RGBA (was %s)' %
                    filename, im.mode)
                raise
            im = imc

        # image are not in the good direction, flip !
        im = im.transpose(PIL.Image.FLIP_TOP_BOTTOM)

        # update internals
        self.filename = filename

        return ImageData(im.size[0], im.size[1],
            im.mode, im.tostring())
