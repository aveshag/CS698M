

# extract features for training
import os
import numpy as np
import glob
import pandas as pd

filename_list = glob.glob('train/*/*/')



apis = ['USER32.dll.SendMessageA', 'KERNEL32.dll.GetFileAttributesA', 'USER32.dll.wsprintfA', 
        'KERNEL32.dll.EncodePointer', 'ADVAPI32.dll.RegQueryValueExA', 'KERNEL32.dll.lstrcmpiA', 
        'KERNEL32.dll.IsProcessorFeaturePresent', 'KERNEL32.dll.SetFilePointerEx', 'KERNEL32.dll.LoadLibraryExW', 
        'KERNEL32.dll.DecodePointer', 'KERNEL32.dll.GetModuleHandleExW', 'KERNEL32.dll.FindFirstFileA', 
        'KERNEL32.dll.GetVersion', 'KERNEL32.dll.InitializeCriticalSectionAndSpinCount', 
        'KERNEL32.dll.DeleteFileA', 'KERNEL32.dll.lstrcpynA', 'KERNEL32.dll.ReadConsoleW', 
        'ADVAPI32.dll.RegOpenKeyExA', 'KERNEL32.dll.AreFileApisANSI', 'ADVAPI32.dll.RegSetValueExA', 
        'KERNEL32.dll.SetErrorMode', 'USER32.dll.DispatchMessageA', 'KERNEL32.dll.OutputDebugStringW', 
        'KERNEL32.dll.GetStartupInfoW', 'KERNEL32.dll.LocalFree', 'KERNEL32.dll.InitializeCriticalSection', 
        'KERNEL32.dll.DeleteFileW', 'KERNEL32.dll.VirtualAlloc', 'USER32.dll.EnableWindow', 
        'GDI32.dll.SelectObject', 'USER32.dll.GetWindowRect', 'USER32.dll.TranslateMessage', 
        'KERNEL32.dll.CreateDirectoryW', 'KERNEL32.dll.SetFileTime', 'USER32.dll.SetTimer', 
        'ole32.dll.CoTaskMemFree', 'KERNEL32.dll.GetCommandLineW', 'GDI32.dll.DeleteObject', 
        'KERNEL32.dll.VirtualFree', 'ole32.dll.CoUninitialize', 'KERNEL32.dll.GlobalFree', 
        'KERNEL32.dll.SetEvent', 'USER32.dll.EndDialog', 'GDI32.dll.GetDeviceCaps', 
        'KERNEL32.dll.InterlockedDecrement', 'USER32.dll.GetClientRect', 'USER32.dll.SetWindowPos', 
        'KERNEL32.dll.InterlockedIncrement']

sections = ['.ndata', '.idata', '.rdata', '.tls', 'BSS', '.edata', '.reloc', '.data', '.bss', 'UPX0', 'UPX1',
            'CODE', '.itext', '.text', '.rsrc', 'DATA', '.aspack', 'UPX2', '.text1', '.rdata1', '.BJFnt',
            '.init', '.svkp', '.itdata', '.pdata', '.data1', '.adata', '.iidata', '.petite', '.badata', 
            '_winzip_s', '/4', 'EPCL_TES', 'EPCL_INI', 'EPCL_SET', '.didata', 'EPCL_CON', 'EPCL_TEX', 
            '.sxdata', '.wixburn', '.gfids', 'EPCL_DAT', '.CRT']

feat_file_header = ["NumberOfSections", "TimeDateStamp", "NumberOfSymbols", "SizeOfOptionalHeader", 
                    "Characteristics"]

feat_optional_header = ["SizeOfCode", "SizeOfInitializedData", "SizeOfUninitializedData", "SizeOfImage",
                       "SizeOfHeaders", "DllCharacteristics", "SizeOfStackReserve", "SizeOfStackCommit", 
                        "SizeOfHeapReserve", "SizeOfHeapCommit","NumberOfRvaAndSizes"]
api_len = len(apis)
sec_len = len(sections)


features = ["Label"]
features += ["NoOfStrings"]
features += feat_file_header
features += feat_optional_header
features += sections
features += apis
features += ["NoOfAPIs"]

df = pd.DataFrame(columns = features, dtype = int) 
 

for j, file in enumerate(filename_list):

    values = []
    
    filedire = file.split("/")
    filetype = filedire[1]
    
    if filetype == 'Benign':
        values += [0]
    else:
        values += [1]
    
    print(filetype, j+1, 'Name:', filedire[2],)
    
    with open(file + "/String.txt", 'r', errors='replace') as f1:
          strings = f1.readlines()
    
    no_of_strings = len(strings)


    f1.close()

    value_file_header = []
    value_optional_header = []
    apis_value = [0 for i in range(api_len)]
    sections_value = [0 for i in range(sec_len)]
    NoOfAPIs = 0
    
    with open(file + "/Structure_Info.txt", 'r', errors='replace') as f2:
          lines = f2.readlines()
    
    i = 0
    
    while i < len(lines):

        if lines[i].find("[IMAGE_FILE_HEADER]") != -1:
            j = 0
            while j < len(feat_file_header):
                i += 1
                if lines[i].find(feat_file_header[j]) != -1:
                    j += 1
                    cols = lines[i].split()
                    value_file_header += [int(cols[3][2:], 16)]

        elif lines[i].find("[IMAGE_OPTIONAL_HEADER]") != -1:
            j = 0
            while j < len(feat_optional_header):
                i += 1
                if lines[i].find(feat_optional_header[j]) != -1:
                    j += 1
                    cols = lines[i].split()
                    value_optional_header += [int(cols[3][2:], 16)]

        elif lines[i].find("[IMAGE_SECTION_HEADER]") != -1:
            i += 1
            cols = lines[i].split()
            if len(cols) > 3:
                sec_name = cols[3]
                for k in range(sec_len):
                    if(sections[k] == sec_name):
                        sections_value[k] = 1
                        break

        elif lines[i].find(".dll.") != -1:
            NoOfAPIs += 1
            api_name = (lines[i].split())[0]
            for k in range(api_len):
                if(apis[k] == api_name):
                    apis_value[k] = 1
                    break

        i += 1
    
    if len(value_file_header) == 0:
        value_file_header += [0 for i in range(len(feat_file_header))]
    if len(value_optional_header) == 0:
        value_optional_header += [0 for i in range(len(feat_optional_header))]
    
    values += [no_of_strings]
    values += value_file_header
    values += value_optional_header
    values += sections_value
    values += apis_value
    values += [NoOfAPIs]
    
    row = pd.Series(values, index = df.columns)
    df = df.append(row, ignore_index=True)

    f2.close()
    
df.to_csv('data_train.csv', index=False) 


