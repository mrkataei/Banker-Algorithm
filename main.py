class BankerAlgorithm:
    def __init__(self, allocated, max_demand, available):
        self.allocated = allocated
        self.max_demand = max_demand
        self.available = available
        self.num_processes = len(allocated)
        self.num_resources = len(available)

    def is_safe_state(self):
        work = self.available[:]
        finish = [False] * self.num_processes
        need = [[self.max_demand[i][j] - self.allocated[i][j] for j in range(self.num_resources)] for i in range(self.num_processes)]

        while True:
            found = False
            for i in range(self.num_processes):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(self.num_resources)):
                    work = [work[j] + self.allocated[i][j] for j in range(self.num_resources)]
                    finish[i] = True
                    found = True

            if not found:
                break

        return all(finish)

    def request_resources(self, process_id, request):
        if any(request[j] > self.max_demand[process_id][j] - self.allocated[process_id][j] for j in range(self.num_resources)):
            raise ValueError("Request exceeds maximum demand.")

        if any(request[j] > self.available[j] for j in range(self.num_resources)):
            raise ValueError("Request exceeds available resources.")

        if any(request[j] > self.allocated[process_id][j] for j in range(self.num_resources)):
            raise ValueError("Request exceeds the allocated resources for the process.")

        for j in range(self.num_resources):
            self.available[j] -= request[j]
            self.allocated[process_id][j] += request[j]

        if not self.is_safe_state():
            # Rollback the resource allocation if the state is not safe
            for j in range(self.num_resources):
                self.available[j] += request[j]
                self.allocated[process_id][j] -= request[j]
            raise ValueError("Request results in an unsafe state.")

    def release_resources(self, process_id, release):
        if any(release[j] > self.allocated[process_id][j] for j in range(self.num_resources)):
            raise ValueError("Release exceeds the allocated resources for the process.")

        for j in range(self.num_resources):
            self.available[j] += release[j]
            self.allocated[process_id][j] -= release[j]


allocated = [[1, 2, 2], [1, 0, 3], [1, 2, 1], [0, 2, 1], [0, 2, 2]]
max_demand = [[3, 3, 2], [1, 2, 3], [1, 3, 1], [0, 3, 1], [0, 3, 3]]
available = [1, 2, 2]

banker = BankerAlgorithm(allocated, max_demand, available)

# Example of resource request
try:
    banker.request_resources(1, [0, 1, 0])
    print("Resource request granted.")
except ValueError as e:
    print("Resource request denied:", str(e))

# Example of resource release
banker.release_resources(0, [0, 1, 0])
print("Resources released.")

# Check if the state is safe
if banker.is_safe_state():
    print("The system is in a safe state.")
else:
    print("The system is in an unsafe state.")
