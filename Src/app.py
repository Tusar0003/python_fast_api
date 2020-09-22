import pyodbc
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import Item


fast_api = FastAPI()

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '(LocalDb)\demo'
database = 'TestDB'
username = 'sa'
password = '0147896325'

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Server=' + server + ';'
                      'DATABASE=' + database + ';'
                      'UID=' + username + ';'
                      'PWD=' + password + ';'
                      'Trusted_Connection=yes')

cursor = conn.cursor()


@fast_api.get("/")
async def read_root():
    # return "<h1>Welcome to API Project</h1><p></p>"
    return '<h1>Welcome to API Project</h1>'


@fast_api.get('/api/v1/resources/info/all')
async def get_all_user_info():
    result = cursor.execute('Select * from TestDB.dbo.UserInfo')
    row_headers = [col[0] for col in result.description]  # this will extract row headers
    rv = result.fetchall()
    data = [dict(zip(row_headers, row)) for row in rv]

    # print(data)

    return JSONResponse(content=data)


@fast_api.get('/api/v1/resources/single/info/')
async def get_single_user_info(name: str):
    user_info = cursor.execute('Select * From UserInfo Where Name=?', name)
    row_headers = [col[0] for col in user_info.description]  # this will extract row headers
    rv = user_info.fetchall()
    data = [dict(zip(row_headers, row)) for row in rv]

    # print(data)

    return JSONResponse(content=data)


@fast_api.post('/api/v1/resources/add/user/info')
async def add_user_info(name: str, profession: str, mobile: str):
    cursor.execute('Insert into UserInfo (Name, Profession, Mobile) '
                   'Values (?,?,?)', name, profession, mobile)
    cursor.commit()

    # print(cursor.rowcount)

    if (cursor.rowcount == 1):
        return {'message': 'Successful'}
    else:
        return {'message': 'Data insertion failed!'}


@fast_api.post('/api/v1/resources/add/item')
async def add_item(item: Item):
    cursor.execute('Insert into Item (Name, Description, Price) '
                   'Values (?,?,?)', item.name, item.description, item.price)
    cursor.commit()

    # print(cursor.rowcount)

    if (cursor.rowcount == 1):
        return {'message': 'Successful'}
    else:
        return {'message': 'Data insertion failed!'}
