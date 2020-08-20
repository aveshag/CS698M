
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import glob
import json
import csv
import os


path = input()   # take test directory path
filename_list = os.listdir(path)





signature = ['WriteProcessMemory', 'bind', 'NtWriteFile', 'CreateProcessInternalW', 'RegQueryValueExA', 'FindWindowW', 
             'ControlService', 'ExitWindowsEx', 'CreateServiceA', 'EnumServicesStatusW', 'WriteConsoleA', 'NtOpenProcess', 
             'NtSetContextThread', 'LdrGetProcedureAddress', 'GlobalMemoryStatusEx', 'GetAdaptersAddresses', 
             'IsDebuggerPresent', 'NtQuerySystemInformation', 'CreateServiceW', 'NtResumeThread', 'RegSetValueExW', 
             'NtGetContextThread', 'GetDiskFreeSpaceExW', 'MoveFileWithProgressW', 'FindWindowExA', 'CryptGenKey', 
             'RegQueryValueExW', 'CryptExportKey', 'InternetOpenA', 'LdrLoadDll', 'FindWindowA', 'NtProtectVirtualMemory', 
             'NtTerminateProcess', 'NtUnmapViewOfSection', 'ShellExecuteExW', 'GetComputerNameW', 'NtWriteVirtualMemory', 
             'GetComputerNameA', 'Process32NextW', 'SetWindowsHookExA', 'EnumServicesStatusA', 'RegSetValueExA', 
             'ReadProcessMemory', 'InternetOpenW', 'NtLoadDriver', 'DeviceIoControl', 'IWbemServices_ExecMethod', 
             'CreateRemoteThread', '__exception__', 'SetFileAttributesW', 'accept', 'WriteConsoleW', 
             'NtAllocateVirtualMemory', 'NtMapViewOfSection', 'NtCreateFile', 'listen', 'SetWindowsHookExW', 
             'LookupPrivilegeValueW']

# dictionary for efficienty access feature value
signature_dict = {}
count = 0
for sign in signature:
    signature_dict[sign] = count
    count += 1

summary = ['regkey_opened', 'dll_loaded', 'directory_created', 'file_opened', 'file_written', 'mutex', 
            'file_created', 'directory_enumerated', 'wmi_query', 'directory_removed', 'regkey_read', 
            'file_moved', 'regkey_deleted', 'file_read', 'file_failed', 'file_copied', 'connects_ip', 'resolves_host', 
            'connects_host', 'file_exists', 'regkey_written', 'file_deleted', 'file_recreated']

# dictionary for efficienty access feature value
summary_dict = {}
count = 0
for su in summary:
    summary_dict[su] = count
    count += 1

features = ["FileName"]      # first column is file name (HASH)
features += ['NoOfStrings']
features += ['virustotal']
features += signature
features += summary

df = pd.DataFrame(columns = features, dtype = int) 

for en, file in enumerate(filename_list):
    
    values = []
    
    print(str(en+1) + '. Name:', file[:-5])    # print file name and serial number 
    
    values += [file[:-5]]
    
    values_sign = [0 for i in range(len(signature))]
    
    values_sum = [0 for i in range(len(summary))]
    
    if path[-1] != '/':
        path += '/'

    with open(path + file, 'r') as f:

        json_data = json.load(f)
        
        try:
            values += [len(json_data['strings'])]   # count number of strings
            
        except:
            
            values += [0]
        
        try:
            values += [json_data['virustotal']['positives']]    # count virus total result
            
        except:
            
            values += [0]
        
        try:
            n = len(json_data['signatures'])
            for i in range(n):
                try:
                    p = len(json_data['signatures'][i]['marks'])
                    for j in range(p):
                        try:
                            values_sign[signature_dict[json_data['signatures'][i]['marks'][j]['call']['api']]] = 1
                        except:
                            pass
                except:
                    pass
        except:
            pass
        
        try:
            
            sum_att = list(json_data['behavior']['summary'].keys())

            for att in sum_att:
                try:
                    values_sum[summary_dict[att]] = len(json_data['behavior']['summary'][att])
                except:
                    pass
        except:
            pass
        
    values += values_sign
    values += values_sum      
    
    f.close()
    
    row = pd.Series(values, index = df.columns)    # append a row in dataframe
    df = df.append(row, ignore_index = True)

df.to_csv('data_test.csv', index = False)      # create data file for testing



ts_data = pd.read_csv('data_test.csv')      # loadding data file

feature_name = list(ts_data.columns.values)

test_data = ts_data.values      
X_test = test_data[:,1:]

filenames = test_data[:,0]       # extract file name (column 1)

# print('Dimensions of the Test Data:',test_data.shape)
# print(ts_data)




filename = 'model.sav' 
 
loaded_model = pickle.load(open(filename, 'rb'))     # load trained model

y_pred = loaded_model.predict(X_test)

pred_label = []

for i in y_pred:
    if i == 0:
        pred_label += ['B']     # 0 as Benign
    else:
        pred_label += ['M']     # 1 as Malware

output = pd.DataFrame(list(zip(filenames, pred_label)), columns = ['File_Hash', 'Predicted Label']) 
output.to_csv('dynamic.csv', index = False) 



