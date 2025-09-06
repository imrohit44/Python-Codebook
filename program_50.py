import asyncio
import multiprocessing
import time

async def worker_task(task_id):
    await asyncio.sleep(1)
    return f"Task {task_id} on process {multiprocessing.current_process().name} done."

def run_asyncio_tasks(tasks_to_run):
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(worker_task(task_id)) for task_id in tasks_to_run]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    return results

if __name__ == "__main__":
    num_processes = 4
    num_tasks = 12

    task_groups = [[] for _ in range(num_processes)]
    for i in range(num_tasks):
        task_groups[i % num_processes].append(i + 1)
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        all_results = pool.map(run_asyncio_tasks, task_groups)

    print("--- All results gathered ---")
    for group_results in all_results:
        for result in group_results:
            print(result)