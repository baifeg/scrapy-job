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

if __name__ == "__main__":
    html_code = """
    <a href="www.google.com" class="more"> google.com</a>
    <A Href="www.pythonclub.org"> PythonClub </a>
    <A HREF = "www.sina.com.cn"> Sina </a>
    """
    hp = IframeHtmlParser()
    hp.feed(html_code)
    hp.close()
    print(hp.qixinLink)