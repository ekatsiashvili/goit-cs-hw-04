import threading
import os
import time
from docx import Document # Імплементуємо Document з бібліотеки python-docx

def search_in_files(file_paths, keywords):
    results = {keyword: [] for keyword in keywords}
    for file_path in file_paths:
        try:
            if file_path.endswith('.docx'):
                doc = Document(file_path)
                content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return results

def threaded_search(file_paths, keywords):
    def worker(files, results):
        result = search_in_files(files, keywords)
        for key, value in result.items():
            results[key].extend(value)

    threads = []
    results = {keyword: [] for keyword in keywords}
    num_threads = 4  # Ви можете змінити кількість потоків при необхідності
    chunk_size = max(1, len(file_paths) // num_threads)  # Забезпечте, що chunk_size не буде нульовим
    chunks = [file_paths[i:i + chunk_size] for i in range(0, len(file_paths), chunk_size)]
    
    for chunk in chunks:
        thread = threading.Thread(target=worker, args=(chunk, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    return results

# Приклад використання
file_paths = [r'C:\Projects\GOAL_WOOLF_GOIT_NEO.docx', r'C:\Projects\GOAL_WOOLF_GOIT_NEO_1.docx', r'C:\Projects\GOAL_WOOLF_GOIT_NEO_2.docx']  # для прикладу, можна замінити реальними шляхами
keywords = ['Dear', 'University']
start_time = time.time()
results = threaded_search(file_paths, keywords)
end_time = time.time()

print(f"Results: {results}")
print(f"Time taken: {end_time - start_time} seconds")
