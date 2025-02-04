import os
import subprocess
import ctypes

class EasyMate:
    def __init__(self):
        if not self.is_admin():
            raise PermissionError("EasyMate requires administrative privileges to switch user accounts.")
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def list_users(self):
        try:
            users = subprocess.check_output("wmic useraccount get name", shell=True)
            users = users.decode().split('\n')[1:]
            users = [user.strip() for user in users if user.strip()]
            return users
        except Exception as e:
            print(f"Error listing users: {e}")
            return []
    
    def switch_user(self, username):
        try:
            # Lock the workstation
            ctypes.windll.user32.LockWorkStation()

            # Switch user
            command = f"runas /user:{username} explorer.exe"
            subprocess.Popen(command, shell=True)
            print(f"Switched to user: {username}")
        except Exception as e:
            print(f"Error switching user: {e}")

if __name__ == "__main__":
    easymate = EasyMate()
    print("Available users:")
    users = easymate.list_users()
    for idx, user in enumerate(users):
        print(f"{idx + 1}. {user}")

    choice = int(input("Enter the number of the user you want to switch to: ")) - 1
    if 0 <= choice < len(users):
        easymate.switch_user(users[choice])
    else:
        print("Invalid choice. Exiting.")