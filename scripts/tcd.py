from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

html = urllib.request.urlopen('https://www.scss.tcd.ie/').read()
html1=text_from_html(html)
g=(html1.split(" "))

f= open("scss.txt","w")

for word in g:
    #print (str(word))
    if str(word)=="":
        continue
    print (str(word))
    f.write(str(word))
    f.write(" ")
