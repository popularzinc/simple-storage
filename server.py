from flask import *
import os
import pages
from pages import Save,ServerData,Clean,Date,RandomName
import shutil
import zipfile

app = Flask(__name__)

HOME_FOLDER = 'Data'

ips = ['192.168.1.14','192.168.1.7','47.133.111.74','192.168.1.2']

@app.before_request
def bfr():
    if(request.remote_addr not in ips):
        print(request.remote_addr + " Blocked")
        return 'BLOCKED'

def Upload(path,request):
    try:
        folder = request.form['folder']
        os.mkdir(Clean(HOME_FOLDER+'/'+path+'/'+folder))
        print(Clean(path+'/'+folder))
        return redirect('/'+Clean(path+'/'+folder))
    except:
        pass
    try:
        files = request.files.getlist("files")
        data = ServerData()

        for file in files:
            data[Clean(path+'/'+file.filename)] = {'uploaded':Date(),'last':'Never'}
            file.save('Data/'+path+'/'+file.filename)
        Save(data)
        return True
    except:
        return False


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        return Upload('',request)
    return pages.Generate('/')

@app.route('/<path:path>', methods=['GET', 'POST'])
def root(path=None):
    if request.method == 'POST':
        return Upload(path,request)
    return pages.Generate(path)

@app.route('/delete', methods=['GET', 'POST'])
def delete_multi():
    if request.method == 'POST':
        for i in request.form.getlist('files'):
            file = HOME_FOLDER+'/'+i
            if(os.path.isfile(file)):
                os.remove(file)
            else:
                shutil.rmtree(file)
    return ' '

@app.route('/delete/<path:path>')
def delete(path=None):
    os.remove(HOME_FOLDER+'/'+path)
    data = ServerData()
    del data[Clean(path)]
    Save(data)
    ## recreate link to redirect to
    r = ''
    for i in path.split('/')[:-1]:
        r += i+'/'
    r = r[:-1]
    ##
    return redirect('/'+r)

@app.route('/remove/<path:path>')
def remove(path=None):
    shutil.rmtree(HOME_FOLDER+'/'+path)
    r = ''
    for i in path.split('/')[:-1]:
        r += i+'/'
    r = r[:-1]
    return redirect('/'+r)

@app.route('/downloads/<path>', methods=['GET', 'POST'])
def download_multis(path=None):
    if(not os.path.isfile('Zip/'+path+'.zip')):
        return redirect('/')
    @after_this_request
    def remove_file(response):
        os.remove('Zip/'+path+'.zip')
        return response
    return send_file('Zip/'+path+'.zip',as_attachment=True,download_name='files.zip')

@app.route('/downloads', methods=['GET', 'POST'])
def download_multi():
    if request.method == 'POST':
        name = RandomName()
        data = ServerData()
        with zipfile.ZipFile('Zip/'+name+'.zip', 'w') as zipF:
            for i in request.form.getlist('files'):
                filename = i
                if('/' in i):
                    filename = i.split('/')[-1]
                zipF.write(HOME_FOLDER+'/'+i, arcname=filename,compress_type=zipfile.ZIP_DEFLATED)
                data[Clean(i)]['last'] = Date()
        Save(data)
        # redirecting in javascript
        return '/downloads/'+name
    else:
        return redirect('/')

@app.route('/download/<path:path>')
def download_file(path=None):
    data = ServerData()
    data[Clean(path)]['last'] = Date()
    Save(data)
    return send_file('Data/'+path,as_attachment=True)

@app.route('/sitedata/<path>')
def get_data(path=None):
    return send_file('SiteData/'+path,as_attachment=True)

@app.route('/api/<path:path>',methods=['POST','GET'])
def api(path=None):
    print('API Request: '+str(request.remote_addr))
    print(' - '+path)
    print()
    try:
        if(request.method == 'POST'):
            p = path[6:].strip()
            if(Upload(p,request)):
                return 'True'
            else:
                return 'error'
            return ' '
        else:
            if(path.startswith('list')):
                folder = HOME_FOLDER
                list = {}
                list['files'] = []
                list['folders'] = []
                if('/' in path):
                    folder = HOME_FOLDER+''.join('/'+x for x in path.split('/')[1:])
                for i in os.listdir(folder):
                    if(os.path.isfile(folder+'/'+i)):
                        list['files'].append(i)
                    else:
                        list['folders'].append(i)
                return list
            elif path.startswith('download'):
                file = HOME_FOLDER+''.join('/'+x for x in path.split('/')[1:])
                if(os.path.isfile(file)):
                    return send_file(file,as_attachment=True)
                else:
                    return 'None'
    except Exception as e:
        print(e)
        return 'ERROR'

app.secret_key = os.urandom(24)
app.run(host='0.0.0.0',port=5554)
