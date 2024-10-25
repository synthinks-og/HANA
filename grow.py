import requests
import time
from colorama import Fore, Style

print(Fore.CYAN + Style.BRIGHT + """ █████╗ ██████╗ ███████╗███╗   ███╗██╗██████╗ ███╗   ██╗""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """██╔══██╗██╔══██╗██╔════╝████╗ ████║██║██╔══██╗████╗  ██║""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """███████║██║  ██║█████╗  ██╔████╔██║██║██║  ██║██╔██╗ ██║""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """██╔══██║██║  ██║██╔══╝  ██║╚██╔╝██║██║██║  ██║██║╚██╗██║""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """██║  ██║██████╔╝██║     ██║ ╚═╝ ██║██║██████╔╝██║ ╚████║""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝     ╚═╝╚═╝╚═════╝ ╚═╝  ╚═══╝""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """t.me/dpangestuw31""" + Style.RESET_ALL)
print(Fore.CYAN + Style.BRIGHT + """Auto Grow for HANA Network""" + Style.RESET_ALL)

# Fungsi untuk memuat token dari file
def load_token_from_file():
    try:
        with open("token.txt", "r") as token_file:
            return token_file.read().strip()
    except FileNotFoundError:
        print(Fore.RED + Style.BRIGHT + "File 'token.txt' tidak ditemukan. Pastikan file tersebut ada." + Style.RESET_ALL)
        exit()

token = load_token_from_file()

url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

print(Fore.GREEN + Style.BRIGHT + "Masukkan Jumlah Grow: " + Style.RESET_ALL)
num_iterations = int(input())

for i in range(num_iterations):
    #print(f"Iteration {i + 1}/{num_iterations}")

    # 1. Mendapatkan status snapshot teratas
    query_get_top_status_snapshots = """
    query getTopStatusSnapshots($offset: Int, $limit: Int) {
      getTopStatusSnapshots(offset: $offset, limit: $limit) {
        user {
          id
          name
        }
      }
    }
    """
    variables_top_status = {"offset": 0, "limit": 100}
    requests.post(url, headers=headers, json={"query": query_get_top_status_snapshots, "variables": variables_top_status})

    mutation_issue_grow_action = """
    mutation issueGrowAction {
      issueGrowAction
    }
    """
    requests.post(url, headers=headers, json={"query": mutation_issue_grow_action})

    mutation_commit_grow_action = """
    mutation commitGrowAction {
      commitGrowAction
    }
    """
    requests.post(url, headers=headers, json={"query": mutation_commit_grow_action})

    query_current_user = """
    query CurrentUser {
      currentUser {
        name
        totalPoint
      }
    }
    """
    response_current_user = requests.post(url, headers=headers, json={"query": query_current_user})

    if response_current_user.status_code == 200:
        current_user_data = response_current_user.json()
        user_name = current_user_data['data']['currentUser']['name']
        initial_total_point = current_user_data['data']['currentUser']['totalPoint']

        mutation_spin = """
        mutation commitSpinAction {
          commitSpinAction
        }
        """
        response_spin = requests.post(url, headers=headers, json={"query": mutation_spin})

        if response_spin.status_code == 200:
            response_current_user_latest = requests.post(url, headers=headers, json={"query": query_current_user})

            if response_current_user_latest.status_code == 200:
                latest_total_point = response_current_user_latest.json()['data']['currentUser']['totalPoint']
                
                print(Fore.GREEN + Style.BRIGHT + f"Name: {user_name} | Total Points: {latest_total_point}" + Style.RESET_ALL)

    # Tunggu sejenak sebelum iterasi berikutnya (opsional)
    time.sleep(2)  # Tunggu 2 detik sebelum iterasi berikutnya
