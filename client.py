import os
import shutil
import requests

BASE_URL = 'http://127.0.0.1:5000'
DOWNLOAD_FOLDER = 'downloaded_files'

def upload_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}  
            response = requests.post(f'{BASE_URL}/upload', files=files)
            print(response.json())
    except Exception as e:
        print(f"Ошибка: {e}")


def get_files():
    response = requests.get(f'{BASE_URL}/get_files')
    files = response.json().get('files', [])
    return files

def select_file(files):
    print("Available files:")
    for idx, filename in enumerate(files, start=1):
        print(f"{idx}. {filename}")

    selected_idx = int(input("Выберете (0, чтобы выйти): "))
    
    if selected_idx == 0:
        return None 
    else:
        selected_file = files[selected_idx - 1] 
        return selected_file

def choose_download_directory():
    download_dir = input("Введите путь, куда сохранить файл (0, чтобы выйти): ")
    
    if download_dir == '0':
        return None 
    else:
        return download_dir

def download_file(filename, download_dir):
    response = requests.get(f'{BASE_URL}/Загрузить/{filename}')
    download_path = os.path.join(download_dir, filename)
    
    with open(download_path, 'wb') as file:
        file.write(response.content)
    
    print(f'{filename} успешно загружено в {download_path}')

def view_file_data(filename):
    response = requests.get(f'{BASE_URL}/excel/{filename}')
    data = response.json().get('data', [])
    
    print(f"Данные в {filename}:")
    for row in data:
        print(row)

def write_to_file(filename, data):
    payload = {'data': data}
    response = requests.post(f'{BASE_URL}/excel/{filename}', json=payload)
    print(response.json())

def delete_row_from_file(filename, row_index):
    payload = {'Номер строки': row_index}
    response = requests.delete(f'{BASE_URL}/excel/{filename}', json=payload)
    print(response.json())

if __name__ == '__main__':
    while True:
        files = get_files()
        
        if not files:
            print("Нет файлов на сервере.")
            break  

        selected_file = select_file(files)

        if selected_file is None:
            break 

        print(f"Выбранный файл: {selected_file}")
        operation = input("Меню:\n1. Загрузить\n2. Просмотр\n3. Изменить\n4. Удалить строку\n5. Подгрузить\n0. Выход\nВыберете число: ")

        if operation == '0':
            break  
        elif operation == '1':  
            download_dir = choose_download_directory()
            
            if download_dir is None:
                break 
            else:
                download_file(selected_file, download_dir)
        elif operation == '2':  
            view_file_data(selected_file)
        elif operation == '3':  
            data = input("Введите данные через запятые: ").split(',')
            write_to_file(selected_file, data)
        elif operation == '4':  
            row_index = int(input("Введите номер строки, которую нужно удалить: "))
            delete_row_from_file(selected_file, row_index)
        elif operation == '5': 
            upload_file(input("Укажите путь к файлу, который надо подгрузить: "))
        else:
            print("Invalid operation number.")
