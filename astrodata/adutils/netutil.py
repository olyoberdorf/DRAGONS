import urllib2
import urllib
import os
import tempfile

import cookielib 
import urlparse
from astrodata.adutils import gemLog
log = gemLog.getGeminiLog()
        
def urlfetch(url, store = None, clobber = False):
    purl = urlparse.urlparse(url)
    host = "hbffits3.hi.gemini.edu" #@@CONFIG: FITSSTORE RETRIEVAL HOST
    npurl = urlparse.ParseResult(purl.scheme,
                                 host,
                                 purl.path,
                                 purl.params,
                                 purl.query,
                                 purl.fragment)
    
    url = npurl.geturl()
    log.info("nu20: adutils.urlfetch asked to get ", url)

    jar = cookielib.CookieJar()


 
    ck = cookielib.Cookie(  version=0, name='gemini_fits_authorization', 
                            value='good_to_go', port=None, 
                            port_specified=False, domain=host, 
                            domain_specified=True, 
                            domain_initial_dot=False, 
                            path='/', path_specified=True, 
                            secure=False, expires=None, 
                            discard=True, comment=None, comment_url=None, 
                            rest={'HttpOnly': None}, rfc2109=False)
    jar.set_cookie(ck)
    
    handler = urllib2.HTTPCookieProcessor(jar)
    opener = urllib2.build_opener(handler)
    # for index, cookie in enumerate(jar):
        # print "nu40:",index, ":", cookie
       
    #res = urllib2.urlopen(req)
    #c = urllib.urlencode( {'gemini_fits_authorization':'value'})
    c = urllib.urlencode( {'gemini_fits_authorization':'value'})
    
    try:
        res = opener.open(url, c)
    except urllib2.HTTPError, error:
        #print "ERROR"
        #print error.read()
        raise 
    #for index, cookie in enumerate(jar):
    #    print index, ":", cookie

    CHUNK = 65536
    if store:
        outname = os.path.join(store, os.path.basename(url))
    else:
        outf = tempfile.NamedTemporaryFile("w", prefix = "uftmp", suffix=".fits", dir =".")
        outname = outf.name
        outf.close()

    if os.path.exists(outname):
        if not clobber:
            raise "File Already Exists:" + outname
        else:
            log.warning("File exists, clobber == True, will overwrite/update")
    f = open(outname,"w")
    #print "netutil: downloading",url
    log.debug("netutil: downloading +",url)
    while True:
        chunk = res.read(CHUNK)
        if chunk == "":
            break
        f.write(chunk)
    #print "netutil: retrieved", url
    #print "netutil:     to",outname
    
    f.close()
    res.close()
    
    return outname
