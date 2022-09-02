import requests
import ast

class Exception(Exception):
    def __init__(self,data):
        self.data = data

    class ConnectionError(Exception):
        def __init__(self,data):
            self.data = data
        class Unknown(Exception):
            def __init__(self,data):
                self.data = data

    class ServerError(Exception):
        def __init__(self,data):
            self.data = data

        class Unknown(Exception):
            def __init__(self,data):
                self.data = data


    class FileError(Exception):
        def __init__(self,data):
            self.data = data
        class Unknown(Exception):
            def __init__(self,data):
                self.data = data

class File:
    def __init__(self,data,filename):
        self.data = data
        self.filename = filename

    def save(self,filename=''):
        if(filename == ''):
            filename = self.filename
        try:
            with open(filename,'wb') as f:
                f.write(self.data)
        except TypeError:
            raise Exception.FileError('Failed writing to file')
        except Exception as e:
            raise Exception.FileError.Unknown('Unknown File Error: '+str(e))
        return True

class API:
    def __init__(self):
        self.server = 'http://192.168.1.14:5554'

    def request(self,data,type='get',files=''):
        if(type == 'get' or type == 'GET'):
            try:
                response = requests.get(self.server+data)
                response.encoding = 'utf-8'
                if(response.text == 'ERROR'):
                    raise Exception.ServerError.Unknown('Unkown Server Error')
            except requests.exceptions.ConnectionError:
                raise Exception.ConnectionError('Could not connect to server: '+str(self.server))
            except Exception as e:
                raise Exception.ConnectionError.Unknown('Unkown error from GET request: '+str(e))

        elif(type == 'post' or type == 'POST'):
            try:
                response = requests.post(self.server+data, files=files)
                response.encoding = 'utf-8'
                if(response.text == 'ERROR'):
                    raise Exception.ServerError.Unknown('Unkown Server Error')
                elif(response.text == 'error'):
                    raise Exception.ServerError('Error uploading file')
            except requests.exceptions.ConnectionError:
                raise Exception.ConnectionError('Could not connect to server: '+str(self.server))
            except Exception as e:
                raise Exception.ConnectionError.Unknown('Unkown error from POST request: '+str(e))
        return response

    def GetList(self, dir='/'):
        if(dir!='/'):
            if(dir[0] != '/'):
                dir = '/'+dir
        else:
            dir = ''
        response = self.request('/api/list'+dir)

        return ast.literal_eval(response.text)

    def GetFile(self,file):
        if(file[0] != '/'):
            file = '/'+file
        response = self.request('/api/download'+file)
        if(response.text == 'None'):
            raise Exception.ServerError('No such file: '+str(file[1:]))
        else:
            data = response.content
            file = File(data,file[1:])
            return file

    def PutFile(self,file,path='/',filename=''):
        local_file = file
        if(filename == ''):
            filename = file
        if(file[0] != '/'):
            file = '/'+file
        if(path[0] != '/'):
            path = '/'+path
        try:
            f = open(local_file,'rb')
        except:
            raise ValueError('Not Such File: '+str(local_file))
        if(path == '/'):
            path = ''

        response = self.request('/api/upload'+path,type='POST',files={'files':(filename,open(local_file, 'rb'))})
        return response
