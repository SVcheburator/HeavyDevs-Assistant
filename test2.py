def get_file_with_data(data):

    #return f'{data=}'.split('=')[0]

    data_name = [ k for k,v in locals().items() if v is data][0]

    return data_name

bla = 5

nn = get_file_with_data(bla)

print(nn)