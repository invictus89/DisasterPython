class format_Config:
    fileMaxByte = 1024 * 1024 * 100 #100MB

    server_format = '[%(asctime)19s] [%(levelname)8s] [%(processName)12s] - %(message)s'
    serverLog = {
        'filename':'./log/serverLog.log'
        #'maxBytes':fileMaxByte,
        #'backupCount':10,
        #'encoding':'utf-8'
    }

    detect_format = '[%(asctime)19s] [%(levelname)8s] [%(processName)12s] - %(message)s'
    detectLog = {
        'filename':'./log/detectLog.log',
        'maxBytes':fileMaxByte,
        'backupCount':10,
        'encoding':'utf-8'
    }

    proc_format = '[%(asctime)19s] [%(levelname)8s] [%(processName)12s] - %(message)s'
    procLog = {
        'filename':'./log/processLog.log',
        #'maxBytes':fileMaxByte,
        #'backupCount':10,
        #'encoding':'utf-8'
    }

    stream_format  = '[         Time ] ==> %(asctime)s\n'
    stream_format += '[ Notice_Level ] ==> %(levelname)s\n'
    stream_format += '[ Process_Name ] ==> %(processName)s : %(process)d\n'
    stream_format += '[    File_Name ] ==> %(filename)s:%(lineno)s\n'
    stream_format += '[      Message ] ==> %(message)s\n'
