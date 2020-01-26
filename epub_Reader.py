#problems Encountered
"""
Prob : PermissionError: [WinError 32] The process cannot access the file because it is being used by another process:
Sol : wrote renaming out of the function(solved)

prob : OSError: [WinError 17] The system cannot move the file to a different disk drive:
Sol : Haven't added the full path while renaming(solved)

prob : OSError: [WinError 123] The filename, directory name, or volume label syntax is incorrect
sol : Used replace to manuplate the file name (previously file name contained ' , : , / , : )  (solved)

prob : raise BadZipFile("File is not a zip file") zipfile.BadZipFile: File is not a zip file
Sol : (Unresolved)



"""
#===========================

import zipfile
from lxml import etree
import os
from os import path

def get_epub_info(fname):
    ns = {
        'n':'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg':'http://www.idpf.org/2007/opf',
        'dc':'http://purl.org/dc/elements/1.1/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]

    # repackage the data
    res = {}
    for s in ['title']:
        res[s] = p.xpath("dc:%s/text()"%(s),namespaces=ns)[0]    
    return res
bookpath = "Your Epub file path"         # Give the folder path where the epub files contains.
for book in os.listdir(bookpath):
        nama = bookpath + '/' + book
        name = get_epub_info(nama)
        title = name['title']
        print(title)
        # :, ?,\ and / and not allowed in file names, so replaced it with some other.
        newTitle = bookpath + '/' + title.replace(":","-").replace("?","").replace("\"","").replace("/","x").replace("'","")+ '.epub'
        #print(newTitle)
        os.rename(nama,newTitle)
