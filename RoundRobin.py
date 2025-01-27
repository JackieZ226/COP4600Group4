def round_robin():
    num_processes = int(input("Enter the number of processes: "))
    processes_info = []

    for i in range(num_processes):
        process_name = input(f"Enter the name of process {i + 1}: ")
        arrival_time = int(
            input(f"Enter the arrival time for process {process_name}: "))
        burst_time = int(
            input(f"Enter the burst time for process {process_name}: "))
        processes_info.append(
            {"job": process_name, "at": arrival_time, "bt": burst_time})

    time_quantum = int(input("Enter the time quantum: "))

    processes_info.sort(key=lambda x: (x["at"], x["job"]))

    solved_processes_info = []
    gantt_chart_info = []

    ready_queue = []
    current_time = processes_info[0]["at"]
    unfinished_jobs = processes_info[:]

    remaining_time = {process["job"]: process["bt"]
                      for process in processes_info}

    ready_queue.append(unfinished_jobs[0])

    while any(remaining_time.values()) and unfinished_jobs:
        if not ready_queue and unfinished_jobs:
            # Previously idle
            ready_queue.append(unfinished_jobs[0])
            current_time = ready_queue[0]["at"]

        process_to_execute = ready_queue[0]

        if remaining_time[process_to_execute["job"]] <= time_quantum:
            # Burst time less than or equal to time quantum, execute until finished
            remaining_t = remaining_time[process_to_execute["job"]]
            remaining_time[process_to_execute["job"]] -= remaining_t
            prev_current_time = current_time
            current_time += remaining_t

            gantt_chart_info.append({
                "job": process_to_execute["job"],
                "start": prev_current_time,
                "stop": current_time,
            })
        else:
            remaining_time[process_to_execute["job"]] -= time_quantum
            prev_current_time = current_time
            current_time += time_quantum

            gantt_chart_info.append({
                "job": process_to_execute["job"],
                "start": prev_current_time,
                "stop": current_time,
            })

        process_to_arrive_in_this_cycle = [
            p for p in processes_info if (
                p["at"] <= current_time and
                p != process_to_execute and
                p not in ready_queue and
                p in unfinished_jobs
            )
        ]

        # Push new processes to readyQueue
        ready_queue.extend(process_to_arrive_in_this_cycle)

        # Requeueing (move head/first item to tail/last)
        ready_queue.append(ready_queue.pop(0))

        # When the process finished executing
        if remaining_time[process_to_execute["job"]] == 0:
            unfinished_jobs.remove(process_to_execute)
            ready_queue.remove(process_to_execute)

            solved_processes_info.append({
                **process_to_execute,
                "ft": current_time,
                "tat": current_time - process_to_execute["at"],
                "wat": current_time - process_to_execute["at"] - process_to_execute["bt"],
            })

    # Sort the processes arrival time and then by job name
    solved_processes_info.sort(key=lambda x: (x["at"], x["job"]))

    return solved_processes_info, gantt_chart_info


solved_processes_info, gantt_chart_info = round_robin()

# Calculate averages
num_processes = len(solved_processes_info)
total_tat = sum(process["tat"] for process in solved_processes_info)
total_wat = sum(process["wat"] for process in solved_processes_info)
total_rt = sum(process["tat"] - process["bt"]
               for process in solved_processes_info)

average_tat = total_tat / num_processes
average_wat = total_wat / num_processes
average_rt = total_rt / num_processes

print("\nProcess\tTurnaround Time\tWaiting Time\tResponse Time")
for process in solved_processes_info:
    print(
        f"{process['job']}\t{process['tat']}\t\t{process['wat']}\t\t{process['tat'] - process['bt']}")

print(f"\nAverage Turnaround Time: {average_tat}")
print(f"Average Waiting Time: {average_wat}")
print(f"Average Response Time: {average_rt}")
