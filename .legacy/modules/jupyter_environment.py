import requests

class jupyter_environment:
    
    def __init__(self, user, token):
        self.user = user
        self.token = token

    def get_status(self):
        with requests.get(f"https://uc2-jupyter.scc.kit.edu/jhub/hub/api/users/{self.user}",
                          headers = {"Authorization": f"token {self.token}"}) as response:
            response.raise_for_status()
            return(response.json())
    
    def start_server(self, cpu_cores = 1, gpu_cores = 0, runtime = 30, memory = 4):
        with requests.post(f"https://uc2-jupyter.scc.kit.edu/jhub/hub/api/users/{self.user}/server",
                   json = {"nprocs": [str(cpu_cores)], "gpu": [str(gpu_cores)], 
                           "runtime": ['{:1d}:{:02d}:00'.format(*divmod(runtime, 60))], 
                           "partition": ["single"], "memory": [f"{memory}G"], 
                           "basemoduleselect": ["jupyter/tensorflow"], "basemodule": ["jupyter/tensorflow"], 
                           "autoreservationstring": ["true"], "expertmodestring": ["false"], 
                           "reservation": [""], "reservationstring": ["#SBATCH --reservation=juypter_weekday_cpuonly"], 
                           "groupname": [""], "groupnamestring": [""], 
                           "lsdfstring": [""], "beeondstring": [""], 
                           "containermodestring": ["false"], "containermodedeactivate": [""],
                           "containermodeactivate": ["#"], "containerimage": [""], 
                           "containerimagestring": [""], "containername": [""], 
                           "containernameifvoid": ["1666099429318"], "containernamestring": [""], 
                           "enrootmounthomestring": [""], "enrootdefaultmountstring": [""], 
                           "enrootremaprootstring": [""]},
                  headers = {"Authorization": f"token {self.token}"}) as response:
            response.raise_for_status()
            return(response.content == b"")
    
    def stop_server(self):
        with requests.delete("https://uc2-jupyter.scc.kit.edu/jhub/hub/api/users/tu_zxobe27/servers/",
                     params = {"name": "tu_zxobe27", "server_name": "''"},
                  headers = {"Authorization": f"token {self.token}"}) as response:
            response.raise_for_status()
            return(response.content == b"")