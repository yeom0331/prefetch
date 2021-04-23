import os.path
import csv
from datetime import datetime, timedelta
from compressed_pf import *

def dt_from_win32_ts(timestamp):
    WIN32_EPOCH = datetime(1601, 1, 1)
    return WIN32_EPOCH + timedelta(microseconds=timestamp // 10, hours=9)

path = "C:/Users/lg/PycharmProjects/prefetch_csv"
filename_list = os.listdir(path)

f = open('prefetch.csv', 'w', encoding='utf-8', newline='') #open csv
wr = csv.writer(f)
wr.writerow(["Filename", "File_Size", "Created_Time", "Modified_Time", "Last_Run_Time", "Run_Count", "Data"])

for filename in filename_list:
    if filename.endswith('.pf'):
        #data = decompress(path + "/" + filename) 압축이 안 풀렸을 때
        file = open(filename, 'rb')
        data = bytearray(file.read())  # 압축이 풀렸을 경우
        prefetch_version = struct.unpack_from("<L", data)[0]
        #Windows 10 / Windows 8.1
        if prefetch_version == 30 or prefetch_version == 26: #check version
            file_size = struct.unpack_from("<L", data[12:])[0]
            Last_Run_Time = dt_from_win32_ts(struct.unpack_from("<Q", data[0x80:])[0]).strftime('%Y:%m:%d %H:%M:%S.%f')
            Created_time = datetime.fromtimestamp(os.path.getctime(path + "/" + filename)).strftime(
                '%Y:%m:%d %H:%M:%S.%f')
            Modified_time = datetime.fromtimestamp(os.path.getmtime(path + "/" + filename)).strftime(
                '%Y:%m:%d %H:%M:%S.%f')
            Run_Count = struct.unpack_from("<L", data[0xD0:])[0]
            FileNameInfoOffset = struct.unpack_from("<L", data[0x64:])[0]
            FileNameInfoSize = struct.unpack_from("<L", data[0x68:])[0]
            load_file = binascii.hexlify(bytes(data[FileNameInfoOffset:FileNameInfoOffset + FileNameInfoSize])).decode("utf-8").split("0000")
            load_file = [i.replace("00", "") for i in load_file] # 00제거


            for i in load_file:
                if i == "00":
                    break
                try:
                    data = binascii.unhexlify(i).decode("utf-8")
                    wr.writerow([filename, file_size, Created_time, Modified_time, Last_Run_Time, Run_Count, data])
                except:
                    wr.writerow([filename, file_size, Created_time, Modified_time, Last_Run_Time, Run_Count, data])

        #Windows XP
        elif prefetch_version == 17:
            file_size = struct.unpack_from("<L", data[12:])[0]
            Last_Run_Time = dt_from_win32_ts(struct.unpack_from("<Q", data[0x78:])[0]).strftime('%Y:%m:%d %H:%M:%S.%f')
            Created_time = datetime.fromtimestamp(os.path.getctime(path + "/" + filename)).strftime(
                '%Y:%m:%d %H:%M:%S.%f')
            Modified_time = datetime.fromtimestamp(os.path.getmtime(path + "/" + filename)).strftime(
                '%Y:%m:%d %H:%M:%S.%f')
            Run_Count = struct.unpack_from("<L", data[0x90:])[0]
            FileNameInfoOffset = struct.unpack_from("<L", data[0x64:])[0]
            FileNameInfoSize = struct.unpack_from("<L", data[0x68:])[0]
            load_file = binascii.hexlify(bytes(data[FileNameInfoOffset:FileNameInfoOffset + FileNameInfoSize])).decode(
                "utf-8").split("0000")
            load_file = [i.replace("00", "") for i in load_file]  # 00제거

            for i in load_file:
                if i == "00":
                    break
                try:
                    data = binascii.unhexlify(i).decode("utf-8")
                    wr.writerow([filename, file_size, Created_time, Modified_time, Last_Run_Time, Run_Count, data])
                except:
                    wr.writerow([filename, file_size, Created_time, Modified_time, Last_Run_Time, Run_Count, data])

        #Windows 7
        elif prefetch_version == 23:
            file_size = struct.unpack_from("<L", data[12:])[0]
            Last_Run_Time = dt_from_win32_ts(struct.unpack_from("<Q", data[0x80:])[0]).strftime('%Y:%m:%d %H:%M:%S.%f')
            Created_time = datetime.fromtimestamp(os.path.getctime(path + "/" + filename)).strftime(
                '%Y:%m:%d %H:%M:%S.%f')
            Modified_time = datetime.fromtimestamp(os.path.getmtime(path + "/" + filename)).strftime(
                '%Y:%m:%d %H:%M:%S.%f')
            Run_Count = struct.unpack_from("<L", data[0x98:])[0]
            FileNameInfoOffset = struct.unpack_from("<L", data[0x64:])[0]
            FileNameInfoSize = struct.unpack_from("<L", data[0x68:])[0]
            load_file = binascii.hexlify(bytes(data[FileNameInfoOffset:FileNameInfoOffset + FileNameInfoSize])).decode(
                "utf-8").split("0000")
            load_file = [i.replace("00", "") for i in load_file]  # 00제거

            for i in load_file:
                if i == "00":
                    break
                try:
                    data = binascii.unhexlify(i).decode("utf-8")
                    wr.writerow([filename, file_size, Created_time, Modified_time, Last_Run_Time, Run_Count, data])
                except:
                    wr.writerow([filename, file_size, Created_time, Modified_time, Last_Run_Time, Run_Count, data])

f.close()