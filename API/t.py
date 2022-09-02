import StorageAPI

server = StorageAPI.API()

filename = 'Data-1.jpeg'

server.PutFile(filename,filename='test.jpeg')
