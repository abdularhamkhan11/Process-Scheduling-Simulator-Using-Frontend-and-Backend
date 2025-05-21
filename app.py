from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def fcfs(processes):
    processes.sort(key=lambda x: x['at'])
    time = 0
    timeline = []
    output = []

    for p in processes:
        if time < p['at']:
            time = p['at']
        start = time
        end = time + p['bt']
        time = end

        output.append({
            'id': p['id'],
            'at': p['at'],
            'bt': p['bt'],
            'ct': end,
            'tat': end - p['at'],
            'wt': start - p['at']
        })

        timeline.append({'id': p['id'], 'start': start, 'end': end})

    return {'timeline': timeline, 'output': output}

def sjf(processes):
    n = len(processes)
    time = 0
    completed = 0
    timeline = []
    output = []
    done = set()

    while completed < n:
        ready = [p for p in processes if p['at'] <= time and p['id'] not in done]
        if not ready:
            time += 1
            continue
        ready.sort(key=lambda x: x['bt'])
        p = ready[0]
        start = time
        end = time + p['bt']
        time = end
        done.add(p['id'])
        completed += 1

        output.append({
            'id': p['id'],
            'at': p['at'],
            'bt': p['bt'],
            'ct': end,
            'tat': end - p['at'],
            'wt': start - p['at']
        })

        timeline.append({'id': p['id'], 'start': start, 'end': end})

    return {'timeline': timeline, 'output': output}

def round_robin(processes, quantum):
    time = 0
    queue = []
    timeline = []
    output = []
    remaining = [p.copy() for p in processes]  # deep copy
    finished = set()

    while remaining or queue:
        for p in remaining[:]:
            if p['at'] <= time and p not in queue:
                queue.append(p)
                remaining.remove(p)

        if not queue:
            time += 1
            continue

        p = queue.pop(0)
        start = time
        exec_time = min(quantum, p['bt'])
        p['bt'] -= exec_time
        time += exec_time

        timeline.append({'id': p['id'], 'start': start, 'end': time})

        if p['bt'] > 0:
            # new arrival processes may come at current time, add before re-adding p
            for proc in remaining[:]:
                if proc['at'] <= time and proc not in queue:
                    queue.append(proc)
                    remaining.remove(proc)
            queue.append(p)
        else:
            ct = time
            tat = ct - p['at']
            wt = tat - (processes[p['id']-1]['bt'])
            output.append({
                'id': p['id'],
                'at': p['at'],
                'bt': processes[p['id']-1]['bt'],
                'ct': ct,
                'tat': tat,
                'wt': wt
            })
            finished.add(p['id'])

    # Sort output by process id
    output.sort(key=lambda x: x['id'])
    return {'timeline': timeline, 'output': output}

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    processes = data['processes']
    algorithm = data['algorithm']
    quantum = data.get('quantum', 2)

    if algorithm == 'FCFS':
        result = fcfs(processes)
    elif algorithm == 'SJF':
        result = sjf(processes)
    else:
        result = round_robin(processes, quantum)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
