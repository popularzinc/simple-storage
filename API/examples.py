import StorageAPI

server = StorageAPI.API()

filename = 'test.txt'

## Get list of files and folders in directory
list = server.GetList(dir='/')

## Uploads file to server
server.PutFile(filename,filename='test2.txt')

## Downloads file and returns file object
file = server.GetFile('test2.txt')
file.save("downloaded.txt")
