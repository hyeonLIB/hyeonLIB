from IPython.display import HTML
from base64 import b64encode

def play(filename):
    html = ''
    video = open(filename,'rb').read()
    src = 'data:video/mp4;base64,' + b64encode(video).decode()
    html += '<center><video width=1000 controls autoplay loop><source src="%s" type="video/mp4"></video></center>' % src 
    return HTML(html)

play('../skeleton_demo_walking.mp4')