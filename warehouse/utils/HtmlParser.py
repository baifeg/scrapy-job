#coding=utf-8

from html.parser import HTMLParser
 
class IframeHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.qixinLink = ""
 
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            if len(attrs) == 0: pass
            else:
                try:
                    if attrs.index(('class', 'more')) != -1:
                        for (variable, value)  in attrs:
                            if variable == "href":
                                self.qixinLink = value
                except ValueError:
                    pass

