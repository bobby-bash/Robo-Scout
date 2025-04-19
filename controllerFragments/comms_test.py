import requests
import time

delay = 1 # sec

# main functino for testing the comms module
def main():
    print("Testing comms module")
    robot_url = "http://parrot-robot3.local"
    #robot_url = "192.168.70.203"

    for i in range(1,11):
        json = {"dtype": "pallet", 
                "power": i % 2
                }
        x = requests.post(robot_url, data=json)
        time.sleep(delay)
    
    return 0    
    

# call main function on start
if __name__ == '__main__':
    main()
