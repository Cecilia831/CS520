from xml.sax.handler import ContentHandler
from xml.sax import parse
import os

class Dispatcher:
        def dispatch(self, prefix, name, attrs=None):
                mname = prefix + name.capitalize()
                dname = 'default' + prefix.capitalize()
                method = getattr(self, mname, None)
               
                if callable(method):
                        args = ()
                        
                else:
                        method = getattr(self, dname, None)
                        args = name,
                        
                if prefix == 'start': args += attrs,
                if callable(method): method(*args)               
        def startElement(self, name, attrs):
                self.dispatch('start', name, attrs)
                #print ("√")
        def endElement(self, name):
                self.dispatch('end', name)
                #print ('ç')
                
class WebsiteConstructor(Dispatcher, ContentHandler):
        passthrough = False

        def __init__(self, directory):
                self.directory = [directory]
                self.ensureDirectory()
        def ensureDirectory(self):
                path = os.path.join(*self.directory)
                print (path)
                print ('----')
                if not os.path.isdir(path): os.makedirs(path)

        def characters(self, chars):
                if self.passthrough: self.out.write(chars)

        def defaultStart(self, name, attrs):
                if self.passthrough:
                        self.out.write('<' + name)
                        for key, val in attrs.items():
                                self.out.write(' %s="%s"' %(key, val))
                        self.out.write('>')
                #print ('[')
        def defaultEnd(self, name):
                #print (']')
                if self.passthrough:
                        self.out.write('</%s>' % name)
                
        def startDirectory(self, attrs):
                print ('startDirectory')
                self.directory.append(attrs['name'])
                self.ensureDirectory()
                
        def endDirectory(self):
                print ('endDirectory')
                self.directory.pop()
                

        def startNote(self,attrs):
                print ('startNote')
                self.writeNoteHeader(attrs['from'])
                self.writeNoteHeader(attrs['to'])
                
               
        def endNote(self):
                print ('endNote')
                self.writeNoteFooter
               
        def startPage(self, attrs):
                print ('startPage')
                filename = os.path.join(*self.directory + [attrs['name']+'.html'])
                self.out = open(filename, 'w')
                self.writeHeader(attrs['title'])
                self.passthrough = True

        def endPage(self):
                print ('endPage')
                self.passthrough = False
                self.writeFooter()
                self.out.close()

        def writeHeader(self, title):
                self.out.write('<html>\n <head>\n   <title>')
                self.out.write(title)
                self.out.write('</title>\n </head>\n  <body>\n')

        def writeFooter(self):
                self.out.write('\n </body>\n</html>\n')

        def writeNoteHeader(self, title):
                self.out.write('<table>')
                self.out.write(title)
                self.out.write(',')

        def writeNoteFooter(self):
                self.out.write('</table>')
                
parse('website.xml',WebsiteConstructor('my_interests.html'))
