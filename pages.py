import os
import ast
from datetime import date
import random
import HTML

SERVER_FILE = 'server_data.dict'

def Date():
    return str(date.today().strftime("%B %d, %Y"))

def RandomName(l=8):
    a = 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
    end = ''
    for i in range(l):
        end += random.choice(a)
    return end

def IsImage(file):
    exts = ['jpg','jpeg','JPG','JPEG','png','PNG']
    ext = file.split('.')[-1]
    if(ext in exts):
        return True
    return False

def Clean(path):
    while('//') in path:
        path = path.replace('//','/')
    if(path.endswith('/') and len(path)>1):
        path = path[:-1]
    if(path[0] == '/'):
        path = path[1:]
    return path

def ServerData():
    with open(SERVER_FILE,'r') as f:
        data = f.read()
    return ast.literal_eval(data)

def Save(data):
    with open(SERVER_FILE,'w') as f:
        f.write(str(data))

def Generate(path):
    parser = HTML.Parser('main.html')
    # 0 - auto
    # 1 - title path
    # 2 - auto
    # 3 - File
    # 4 - Folder
    # 5 - auto
    # 6 - home
    # 7 - not home
    # 8 - auto

    file_variables = {
        'SHORT_FILENAME':'',
        'FILENAME':'',
        'DISPLAY':'',
        'FILE_SIZE':'',
        'FILE_UPLOADED':'',
        'FILE_DOWNLOADED':'',
        'FILE_LINK':''
    }
    folder_variables = {
        'FOLDERNAME':'',
        'FOLDER_LINK':''
    }
    path_var = {
        'PATH':'',
        'LINK':''
    }
    last = ''
    for i in path.split('/'):
        if(i != ''):
            link = last+'/'+i
            if(link[0] != '/'):
                link = '/'+link
            path_var['LINK'] = link
            path_var['PATH'] = i
            parser.Add(1,path_var)
            if(i != '/'):
                last = last+'/'+i

    parser.Add(0)
    parser.Add(2)
    parser.Add(5)
    parser.Add(8)

    if(path == '/'):
        parser.Add(6,{'REMOVE_PATH':'/remove/'+path})
    else:
        parser.Add(7,{'REMOVE_PATH':'/remove/'+path})

    list_path = 'Data/'+path
    data = ServerData()

    for i in os.listdir(list_path):
        file = Clean(list_path+'/'+i)
        if(os.path.isfile(file)):
            server_path = Clean(path+'/'+i)
            try:
                data[server_path]
            except:
                data[server_path] = {'uploaded':'N/A','last':'N/A'}
            short_name,display = short(i)
            file_variables['DISPLAY']           = display
            file_variables['FILENAME']          = server_path
            file_variables['SHORT_FILENAME']    = short_name
            file_variables['FILE_SIZE']         = Size(file)
            file_variables['FILE_UPLOADED']     = data[server_path]['uploaded']
            file_variables['FILE_DOWNLOADED']   = data[server_path]['last']
            file_variables['FILE_LINK']         = '/download/'+server_path
            file_variables['DEL_LINK']          = '/delete/'+server_path
            parser.Add(3,file_variables)
        else:
            folder_variables['FOLDERNAME']      = i
            folder_variables['FOLDER_LINK']     = '/'+Clean(path+'/'+i)
            parser.Add(4,folder_variables)

    return parser.Generate()

def short(filename):
    no_ext = '.'.join(x for x in filename.split('.')[:-1])
    end = filename
    if(len(no_ext) > 9):
        ext = filename.split('.')[-1]
        end = str(no_ext[:7])+'..'+ext

    end1 = filename
    if(len(no_ext) > 20):
        ext = filename.split('.')[-1]
        end1 = str(no_ext[:18])+'..'+ext
    return end,end1

def Top(path):
    path = Clean(path)
    top = '''
    <!DOCTYPE html>
    <html>
      <head>
        <link rel="stylesheet" href="/sitedata/main.css">
        <script src="/sitedata/main.js"></script>
      </head>
      <body>
      <div id="blur-section">
        <div class="top-section">
          <a href="/">
            <img class="logo" src="/sitedata/logo.png">
          </a>
          <div class="top-path">'''
    link = ''
    for i in path.split('/'):
        link = link+'/'+i
        top += '/<a style="text-decoration:none;" href="'+link+'"><span class="folder">'+i+'</span></a>'
    top = top[:-11]+'</span></a>'

    top += '''</div>
        </div>
        <br>
        <div class="contents">'''
    return top




def _Generate(path):
    bottom = '''
    </div>
    <br><br><br>
    <input id="in" onchange="browsed()" type=file style="display:none;" multiple>
    <div id="dropzone" onclick="handleClick()" ondragleave="dragleaveHandler(event)" ondragover="dragoverHandler(event)" ondrop="dropHandler(event)" class="dropzone">
      <div class="upload-content">
        <img src="/sitedata/download.png" style="height:30px;width:30px;">
        <br>
        <span id="msg"><b>Drag here</b> or click to browse</span><br><br>
      </div>
    </div>
'''
    if(path == '/'):
        bottom += '''
        <div class="button-container">
          <div id="down" onclick="download()" class="bottom-buttons-disabled">Download Selected</div>
          <div id="del" onclick="remove()" class="bottom-buttons-disabled">Delete Selected</div>
          <div class="bottom-buttons-disabled">Delete Folder</div>
        </div>'''
    else:
        bottom += '''
        <div class="button-container">
          <div id="down" onclick="download()" class="bottom-buttons-disabled">Download Selected</div>
          <div id="del" onclick="remove()" class="bottom-buttons-disabled">Delete Selected</div>
          <a onclick="return confirm('Are you sure you want to delete this folder?');" style="text-decoration:none;" href="/remove/'''+path+'''">
            <div class="bottom-buttons-red">Delete Folder</div>
          </a>
        </div>'''

    bottom += '''
    <br>
        <form method=POST>
          <input name="folder" placeholder="New Folder.." class="new-folder-input" onkeypress="return event.charCode != 32" type=text>
        </form>
      </div>
    <div id="focused" class="focused">
      <div class="close" onclick="toggle()"><b>CLOSE</b></div>
      <div id="image" class="img-container"></div>
    </div>
  </body>
</html>
'''
    list_path = 'Data/'+path
    end = Top(path)
    for i in os.listdir(list_path):
        if(os.path.isfile(list_path+'/'+i)):
            end += AddFile(path,i)
        else:
            end += AddFolder(path,i)
    return end+bottom

def Size(file):
    s = os.path.getsize(file)
    return str(s)

def AddFile(path,file):
    display_name = file
    display_name2 = file
    no_ext = '.'.join(x for x in file.split('.')[:-1])
    if(no_ext == ''): # filename with no . in it
        no_ext = file
    if(len(no_ext)>9):
        ext = file.split('.')[-1]
        display_name = str(no_ext[:7])+'..'+ext
        if(no_ext == file):
            display_name = str(no_ext[:15])+'..'
    if(len(no_ext)>20):
        ext = file.split('.')[-1]
        display_name2 = str(no_ext[:16])+'..'+ext
        if(no_ext == file):
            display_name2 = str(no_ext[:20])+'..'
    data = ServerData()
    try:
        data[Clean(path+'/'+file)]
    except:
        data[Clean(path+'/'+file)] = {'uploaded':'N/A','last':'N/A'}
    end = ''
    end += '''
      <div onclick="clicked(this);" class="box">
        <div class="info">
          <div class="title">'''+display_name2+'''</div>
          <div class="details">
            File Size: '''+Size(Clean(path+'/'+file))+''' Bytes<br>
            Date uploaded: '''+data[Clean(path+'/'+file)]['uploaded']+'''<br>
            Last downloaded: '''+data[Clean(path+'/'+file)]['last']+'''<br>
          </div>'''
    if(IsImage(file)):
        end += '''<div onclick="toggle(this)" link="/download/'''+Clean(path+'/'+file)+'''" class="view-button">View</div>'''

    end += '''<a onclick="return confirm('Are you sure you want to delete '''+file+'''?');" style="text-decoration:none;" href="/delete/'''+Clean(path+'/'+file)+'''">
            <div class="delete-button">Delete</div>
          </a>
          <a style="text-decoration:none;" href="/download/'''+Clean(path+'/'+file)+'''">
            <div class="download-button">Download</div>
          </a>
        </div>
        <img class="icon" src="/sitedata/file.png">
        '''+display_name+'''
        <input name="checkboxes" class="selector" value="'''+Clean(path+'/'+file)+'''" type=checkbox>
      </div>'''
    return end

def AddFolder(path,folder):
    end = '''
      <a style="text-decoration:none;" href="/'''+Clean(path+'/'+folder)+'''">
      <div class="box">
        <img class="icon" src="/sitedata/folder.png">
        '''+folder+'''
      </div>
      </a>'''
    return end
