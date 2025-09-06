import time
import concurrent.futures
import random

def process_task(task_id):
    """
    Simulates a task that takes some time to complete.
    Could be CPU-bound (complex calculation) or I/O-bound (network request/file read).
    """
    delay = random.uniform(0.5, 2.0)  # Simulate variable work time
    print(f"Task {task_id}: Starting work, expected delay {delay:.2f}s...")
    time.sleep(delay)  # Simulate I/O or CPU work
    result = f"Task {task_id} completed in {delay:.2f}s."
    print(f"Task {task_id}: Finished.")
    return result

def main():
    num_tasks = 10
    tasks_to_run = list(range(num_tasks))
    results = []

    print(f"Submitting {num_tasks} tasks to the thread pool...")

    # Use ThreadPoolExecutor for concurrent execution
    # max_workers specifies the maximum number of threads to use
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Map the process_task function to each task_id
        # submit() also works and gives more control over individual futures
        # but map() is simpler for applying a function to an iterable
        future_to_task_id = {executor.submit(process_task, task_id): task_id for task_id in tasks_to_run}

        # Iterate over completed futures as they finish
        for future in concurrent.futures.as_completed(future_to_task_id):
            task_id = future_to_task_id[future]
            try:
                result = future.result() # Get the result of the completed task
                results.append(result)
            except Exception as exc:
                print(f'Task {task_id} generated an exception: {exc}')

    print("\nAll tasks completed. Results:")
    for res in results:
        print(res)

if __name__ == "__main__":
    main()