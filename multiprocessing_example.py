import multiprocessing
from multiprocessing import Queue
from collections import defaultdict
import time
from docx import Document  # Імплементуємо Document з бібліотеки python-docx

def search_keywords_in_files(file_paths, keywords, queue):
    local_results = defaultdict(list)
    for file_path in file_paths:
        try:
            doc = Document(file_path)
            content = '\n'.join([para.text for para in doc.paragraphs])
            for keyword in keywords:
                if keyword in content:
                    local_results[keyword].append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    queue.put(local_results)

def multiprocessing_search(file_paths, keywords):
    num_processes = min(4, len(file_paths)) 
    processes = []
    queue = Queue()
    results = defaultdict(list)

    # Розподіл на частини для кожного процесу
    chunk_size = len(file_paths) // num_processes + (len(file_paths) % num_processes > 0)
    chunks = [file_paths[i:i + chunk_size] for i in range(0, len(file_paths), chunk_size)]

    for chunk in chunks:
        process = multiprocessing.Process(target=search_keywords_in_files, args=(chunk, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Результати за всіма процесами
    while not queue.empty():
        local_results = queue.get()
        for keyword, files in local_results.items():
            results[keyword].extend(files)

    return results

if __name__ == '__main__':
    # Приклад використання
    file_paths = [r'C:\Projects\GOAL_WOOLF_GOIT_NEO.docx', r'C:\Projects\GOAL_WOOLF_GOIT_NEO_1.docx', r'C:\Projects\GOAL_WOOLF_GOIT_NEO_2.docx']  # для прикладу, можна замінити іншими реальними шляхами
    keywords = ['Dear', 'University']
    start_time = time.time()
    results = multiprocessing_search(file_paths, keywords)
    end_time = time.time()

    print(f"Multiprocessing search results: {results}")
    print(f"Time taken: {end_time - start_time} seconds")
