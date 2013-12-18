import os
import os.path as op
import web
from sqlalchemy.orm import scoped_session, sessionmaker

PROJECT_ROOT = op.abspath(op.join(op.dirname(__file__), '..'))
DATABASE_NAME = 'metapolatordev'
DATABASE_USER = 'root'
DATABASE_PWD = ''

try:
    from localconfig import DATABASE_USER, DATABASE_PWD, DATABASE_NAME
except ImportError:
    pass

DATABASE_ENGINE = 'mysql+mysqldb://{0}:{1}@localhost/{2}'.format(DATABASE_USER, DATABASE_PWD, DATABASE_NAME)

from sqlalchemy import create_engine
engine = create_engine(DATABASE_ENGINE, echo=False)

### Url mappings
web.config.debug = False


def load_user(handler):
    import models
    try:
        web.ctx.user = models.User.get(id=session.user)
    except AttributeError:
        web.ctx.user = None
    return handler()


def load_sqla(handler):
    if not session.get('mfparser'):
        session.mfparser = 'controlpoints'
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.commit()
        raise

    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()
        # If the above alone doesn't work, uncomment
        # the following line:
        #web.ctx.orm.expunge_all()

app = web.auto_application()
app.add_processor(load_sqla)


session = web.session.Session(app, web.session.DiskStore('sessions'),
                              {'count': 0})
app.add_processor(load_user)


def is_loggedin():
    try:
        return web.ctx.user
    except AttributeError:
        pass


def buildfname(filename):
    try:
        basename, extension = filename.split('.')
    except:
        extension = "garbage"
        basename = ""
    return [basename, extension]


def working_dir(path=None, user=None):
    if web.ctx.user or user:
        directory = op.join(PROJECT_ROOT, 'users', str(user or web.ctx.user.username))
        if not op.exists(directory):
            os.makedirs(directory)

        if not path:
            return directory

        result_path = op.join(directory, path)
        if not op.exists(result_path):
            os.makedirs(result_path)

        return result_path
    return path


def working_url(path=None):
    if is_loggedin():
        directory = op.join('/', 'users', str(web.ctx.user.username))
        if not path:
            return directory
        return op.join(directory, path)
    return path


MFLIST = ['A', 'Agrave', 'Aacute', 'Acircumflex', 'Atilde', 'Adieresis', 'Aring', 'Amacron', 'Abreve', 'Aogonek', 'B', 'uni1E02', 'C', 'Ccedilla', 'Cacute', 'Ccircumflex', 'Cdotaccent', 'Ccaron', 'D', 'Dcaron', 'uni1E0A', 'E', 'Egrave', 'Eacute', 'Ecircumflex', 'Edieresis', 'Emacron', 'Edotaccent', 'Eogonek', 'Ecaron', 'F', 'uni1E1E', 'G', 'Gcircumflex', 'Gbreve', 'Gdotaccent', 'Gcommaaccent', 'H', 'Hcircumflex', 'I', 'Igrave', 'Iacute', 'Icircumflex', 'Idieresis', 'Itilde', 'Imacron', 'Iogonek', 'Idotaccent', 'J', 'Jcircumflex', 'K', 'Kcommaaccent', 'L', 'Lacute', 'Lcommaaccent', 'Lcaron', 'M', 'uni1E40', 'N', 'Ntilde', 'Nacute', 'Ncommaaccent', 'Ncaron', 'O', 'Ograve', 'Oacute', 'Ocircumflex', 'Otilde', 'Odieresis', 'Omacron', 'Ohungarumlaut', 'P', 'uni1E56', 'Q', 'R', 'Racute', 'Rcommaaccent', 'Rcaron', 'S', 'Sacute', 'Scircumflex', 'Scedilla', 'Scaron', 'uni1E60', 'T', 'Tcommaaccent', 'Tcaron', 'uni1E6A', 'U', 'Ugrave', 'Uacute', 'Ucircumflex', 'Udieresis', 'Utilde', 'Umacron', 'Ubreve', 'Uring', 'Uhungarumlaut', 'Uogonek', 'V', 'W', 'Wcircumflex', 'Wgrave', 'Wacute', 'Wdieresis', 'X', 'Y', 'Yacute', 'Ycircumflex', 'Ydieresis', 'Ygrave', 'Z', 'Zacute', 'Zdotaccent', 'Zcaron', 'AE', 'Eth', 'Oslash', 'Thorn', 'Dcroat', 'Hbar', 'Lslash', 'Eng', 'OE', 'Tbar', 'M.salt', 'uni1E40.salt', 'N.salt', 'Ntilde.salt', 'Nacute.salt', 'Ncommaaccent.salt', 'Ncaron.salt', 'X.salt', 'Idotaccent.smcp', 'uni03A9', 'mu', 'afii61289', 'a', 'agrave', 'aacute', 'acircumflex', 'atilde', 'adieresis', 'aring', 'amacron', 'abreve', 'aogonek', 'b', 'uni1E03', 'c', 'ccedilla', 'cacute', 'ccircumflex', 'cdotaccent', 'ccaron', 'c_h', 'c_k', 'c_t', 'd', 'dcaron', 'uni1E0B', 'e', 'egrave', 'eacute', 'ecircumflex', 'edieresis', 'emacron', 'edotaccent', 'eogonek', 'ecaron', 'f', 'uni1E1F', 'f_t', 'f_y', 'g', 'gcircumflex', 'gbreve', 'gdotaccent', 'gcommaaccent', 'h', 'hcircumflex', 'i', 'igrave', 'iacute', 'icircumflex', 'idieresis', 'itilde', 'imacron', 'iogonek', 'j', 'jcircumflex', 'k', 'kcommaaccent', 'l', 'lacute', 'lcommaaccent', 'lcaron', 'm', 'uni1E41', 'n', 'ntilde', 'nacute', 'ncommaaccent', 'ncaron', 'o', 'ograve', 'oacute', 'ocircumflex', 'otilde', 'odieresis', 'omacron', 'ohungarumlaut', 'p', 'uni1E57', 'q', 'r', 'racute', 'rcommaaccent', 'rcaron', 's', 'sacute', 'scircumflex', 'scedilla', 'scaron', 'uni1E61', 't', 'tcommaaccent', 'tcaron', 'uni1E6B', 't_t', 't_y', 'u', 'ugrave', 'uacute', 'ucircumflex', 'udieresis', 'utilde', 'umacron', 'ubreve', 'uring', 'uhungarumlaut', 'uogonek', 'v', 'w', 'wcircumflex', 'wgrave', 'wacute', 'wdieresis', 'x', 'y', 'yacute', 'ydieresis', 'ycircumflex', 'ygrave', 'z', 'zacute', 'zdotaccent', 'zcaron', 'ordfeminine', 'ordmasculine', 'germandbls', 'ae', 'eth', 'oslash', 'thorn', 'dcroat', 'hbar', 'dotlessi', 'kgreenlandic', 'lslash', 'eng', 'oe', 'tbar', 'florin', 'uniFB00', 'uniFB01', 'uniFB02', 'uniFB03', 'uniFB04', 'uniFB06', 'a.salt', 'agrave.salt', 'aacute.salt', 'acircumflex.salt', 'atilde.salt', 'adieresis.salt', 'aring.salt', 'amacron.salt', 'abreve.salt', 'aogonek.salt', 'b.salt', 'uni1E03.salt', 'd.salt', 'dcaron.salt', 'uni1E0B.salt', 'f.salt', 'uni1E1F.salt', 'g.salt', 'gcircumflex.salt', 'gbreve.salt', 'gdotaccent.salt', 'gcommaaccent.salt', 'm.salt', 'uni1E41.salt', 'n.salt', 'ntilde.salt', 'nacute.salt', 'ncommaaccent.salt', 'ncaron.salt', 'p.salt', 'uni1E57.salt', 'r.salt', 'racute.salt', 'rcommaaccent.salt', 'rcaron.salt', 't.salt', 'tcommaaccent.salt', 'tcaron.salt', 'u.salt', 'ugrave.salt', 'uacute.salt', 'ucircumflex.salt', 'udieresis.salt', 'utilde.salt', 'umacron.salt', 'ubreve.salt', 'uring.salt', 'uhungarumlaut.salt', 'uogonek.salt', 'x.salt', 'dcroat.salt', 'tbar.salt', 'a.smcp', 'agrave.smcp', 'aacute.smcp', 'acircumflex.smcp', 'atilde.smcp', 'adieresis.smcp', 'aring.smcp', 'amacron.smcp', 'abreve.smcp', 'aogonek.smcp', 'b.smcp', 'uni1E03.smcp', 'c.smcp', 'ccedilla.smcp', 'cacute.smcp', 'ccircumflex.smcp', 'cdotaccent.smcp', 'ccaron.smcp', 'd.smcp', 'dcaron.smcp', 'uni1E0B.smcp', 'e.smcp', 'egrave.smcp', 'eacute.smcp', 'ecircumflex.smcp', 'edieresis.smcp', 'emacron.smcp', 'edotaccent.smcp', 'eogonek.smcp', 'ecaron.smcp', 'f.smcp', 'uni1E1F.smcp', 'g.smcp', 'gcircumflex.smcp', 'gbreve.smcp', 'gdotaccent.smcp', 'gcommaaccent.smcp', 'h.smcp', 'hcircumflex.smcp', 'i.smcp', 'igrave.smcp', 'iacute.smcp', 'icircumflex.smcp', 'idieresis.smcp', 'itilde.smcp', 'imacron.smcp', 'iogonek.smcp', 'j.smcp', 'jcircumflex.smcp', 'k.smcp', 'kcommaaccent.smcp', 'l.smcp', 'lacute.smcp', 'lcommaaccent.smcp', 'lcaron.smcp', 'm.smcp', 'uni1E41.smcp', 'n.smcp', 'ntilde.smcp', 'nacute.smcp', 'ncommaaccent.smcp', 'ncaron.smcp', 'o.smcp', 'ograve.smcp', 'oacute.smcp', 'ocircumflex.smcp', 'otilde.smcp', 'odieresis.smcp', 'omacron.smcp', 'ohungarumlaut.smcp', 'p.smcp', 'uni1E57.smcp', 'q.smcp', 'r.smcp', 'racute.smcp', 'rcommaaccent.smcp', 'rcaron.smcp', 's.smcp', 'sacute.smcp', 'scircumflex.smcp', 'scedilla.smcp', 'scaron.smcp', 'uni1E61.smcp', 't.smcp', 'tcommaaccent.smcp', 'tcaron.smcp', 'uni1E6B.smcp', 'u.smcp', 'ugrave.smcp', 'uacute.smcp', 'ucircumflex.smcp', 'udieresis.smcp', 'utilde.smcp', 'umacron.smcp', 'ubreve.smcp', 'uring.smcp', 'uhungarumlaut.smcp', 'uogonek.smcp', 'v.smcp', 'w.smcp', 'wcircumflex.smcp', 'wgrave.smcp', 'wacute.smcp', 'wdieresis.smcp', 'x.smcp', 'y.smcp', 'yacute.smcp', 'ydieresis.smcp', 'ycircumflex.smcp', 'ygrave.smcp', 'z.smcp', 'zacute.smcp', 'zdotaccent.smcp', 'zcaron.smcp', 'ordfeminine.smcp', 'ordmasculine.smcp', 'germandbls.smcp', 'ae.smcp', 'eth.smcp', 'oslash.smcp', 'thorn.smcp', 'dcroat.smcp', 'hbar.smcp', 'lslash.smcp', 'eng.smcp', 'oe.smcp', 'tbar.smcp', 'a.superior', 'b.superior', 'c.superior', 'd.superior', 'e.superior', 'f.superior', 'g.superior', 'h.superior', 'i.superior', 'j.superior', 'k.superior', 'l.superior', 'm.superior', 'n.superior', 'o.superior', 'p.superior', 'q.superior', 'r.superior', 's.superior', 't.superior', 'u.superior', 'v.superior', 'w.superior', 'x.superior', 'y.superior', 'z.superior', 'pi', 'circumflex', 'caron', 'circumflex.smcp', 'caron.smcp', 'uni0338', 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'zero.denominator', 'one.denominator', 'two.denominator', 'three.denominator', 'four.denominator', 'five.denominator', 'six.denominator', 'seven.denominator', 'eight.denominator', 'nine.denominator', 'zero.numerator', 'one.numerator', 'two.numerator', 'three.numerator', 'four.numerator', 'five.numerator', 'six.numerator', 'seven.numerator', 'eight.numerator', 'nine.numerator', 'zero.oldstyle', 'one.oldstyle', 'two.oldstyle', 'three.oldstyle', 'four.oldstyle', 'five.oldstyle', 'six.oldstyle', 'seven.oldstyle', 'eight.oldstyle', 'nine.oldstyle', 'zero.smcp', 'one.smcp', 'two.smcp', 'three.smcp', 'four.smcp', 'five.smcp', 'six.smcp', 'seven.smcp', 'eight.smcp', 'nine.smcp', 'zero.tnum', 'one.tnum', 'two.tnum', 'three.tnum', 'four.tnum', 'five.tnum', 'six.tnum', 'seven.tnum', 'eight.tnum', 'nine.tnum', 'zero.tosf', 'one.tosf', 'two.tosf', 'three.tosf', 'four.tosf', 'five.tosf', 'six.tosf', 'seven.tosf', 'eight.tosf', 'nine.tosf', 'uni00B2', 'uni00B3', 'uni00B9', 'onequarter', 'onehalf', 'threequarters', 'uni2070', 'uni2074', 'uni2075', 'uni2076', 'uni2077', 'uni2078','uni2079', 'uni2080', 'uni2081', 'uni2082', 'uni2083', 'uni2084', 'uni2085', 'uni2086', 'uni2087', 'uni2088', 'uni2089', 'underscore', 'hyphen', 'endash', 'emdash', 'hyphen.alt', 'endash.alt', 'emdash.alt', 'hyphen.smcp', 'endash.smcp', 'emdash.smcp', 'parenleft', 'bracketleft', 'braceleft', 'quotesinglbase', 'quotedblbase', 'parenleft.alt', 'parenleft.smcp', 'quotesinglbase.smcp', 'quotedblbase.smcp', 'parenright', 'bracketright', 'braceright', 'parenright.alt', 'parenright.smcp', 'guillemotleft', 'quoteleft', 'quotedblleft', 'guilsinglleft', 'quoteleft.smcp', 'quotedblleft.smcp', 'guillemotright', 'quoteright', 'quotedblright', 'guilsinglright', 'quoteright.smcp', 'quotedblright.smcp', 'exclam', 'quotedbl', 'numbersign', 'percent', 'ampersand', 'quotesingle', 'asterisk', 'comma', 'period', 'slash', 'colon', 'semicolon', 'question', 'at', 'backslash', 'exclamdown', 'periodcentered', 'questiondown', 'dagger', 'daggerdbl', 'bullet', 'ellipsis', 'perthousand', 'at.alt', 'exclamdown.alt', 'questiondown.alt', 'ampersand.salt', 'exclam.smcp', 'quotedbl.smcp', 'numbersign.smcp', 'percent.smcp', 'ampersand.smcp', 'quotesingle.smcp', 'asterisk.smcp', 'question.smcp', 'at.smcp', 'exclamdown.smcp', 'periodcentered.smcp', 'questiondown.smcp', 'bullet.smcp', 'perthousand.smcp', 'plus', 'less', 'equal', 'greater', 'bar', 'asciitilde', 'logicalnot', 'plusminus', 'multiply', 'divide', 'fraction', 'partialdiff', 'Delta', 'product', 'summation', 'minus', 'radical', 'infinity', 'integral', 'approxequal', 'notequal', 'lessequal', 'greaterequal', 'dollar', 'cent', 'sterling', 'currency', 'yen', 'Euro', 'dollar.smcp', 'sterling.smcp', 'yen.smcp', 'Euro.smcp', 'asciicircum', 'grave', 'dieresis', 'macron', 'acute', 'cedilla', 'breve', 'dotaccent', 'ring', 'ogonek', 'tilde', 'hungarumlaut', 'grave.smcp', 'dieresis.smcp', 'macron.smcp', 'acute.smcp', 'ring.smcp', 'tilde.smcp', 'brokenbar', 'section', 'copyright', 'registered', 'degree', 'paragraph', 'afii61352', 'trademark', 'estimated', 'lozenge', 'degree.smcp', 'space', '.notdef', 'uni000D', 'uni00AD', 'uni00AD.alt', 'uni00AD.smcp', 'onesuperior', 'threesuperior', 'twosuperior']
