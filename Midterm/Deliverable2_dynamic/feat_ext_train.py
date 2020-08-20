
# Extract feature for training and save them into data_train.csv

import numpy as np
import glob
import json
import pandas as pd

filename_list = glob.glob('train/*/*')




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

signature_dict = {}
count = 0
for sign in signature:
    signature_dict[sign] = count
    count += 1

summary = ['regkey_opened', 'dll_loaded', 'directory_created', 'file_opened', 'file_written', 'mutex', 
            'file_created', 'directory_enumerated', 'wmi_query', 'directory_removed', 'regkey_read', 
            'file_moved', 'regkey_deleted', 'file_read', 'file_failed', 'file_copied', 'connects_ip', 'resolves_host', 
            'connects_host', 'file_exists', 'regkey_written', 'file_deleted', 'file_recreated']

summary_dict = {}
count = 0
for su in summary:
    summary_dict[su] = count
    count += 1

features = ['Label']
features += ['NoOfStrings']
features += ['virustotal']
features += signature
features += summary

df = pd.DataFrame(columns = features, dtype = int) 

for en, file in enumerate(filename_list):

    filesplt = file.split('/')
    filetype = filesplt[1]
    
    
    print(filetype, en+1, 'Name:', filesplt[2])
    
    values = []
    
    values_sign = [0 for i in range(len(signature))]
    
    values_sum = [0 for i in range(len(summary))]
    
    if filetype == 'Benign':
        values += [0]
    else:
        values += [1]
    
    with open(file, 'r') as f:
        
        json_data = json.load(f)
        
        try:
            values += [len(json_data['strings'])]
            
        except:
            
            values += [0]
        
        try:
            values += [json_data['virustotal']['positives']]
            
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
 # len(json_data['behavior']['summary']['resolves_host'])           
        try:
            
            sum_att = list(json_data['behavior']['summary'].keys())
#             print(sum_att)
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
    
    row = pd.Series(values, index = df.columns)
    df = df.append(row, ignore_index = True)

df.to_csv('data_train.csv', index = False) 


