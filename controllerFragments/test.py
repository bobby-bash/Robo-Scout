import requests
import time

# Set your ESP8266's IP address or hostname here
esp8266_ip = "http://parrot-robot3.local"

def test_all_speed_combinations():
    """
    Test all possible speed and direction combinations for two servo motors.
    """
    # Define speed values and directions for testing
    speeds = [90] * 10  # Example speed steps for PWM adjustments
    directions = ["clockwise", "counterclockwise"]
    #directions = ["clockwise"]
    servo2_speed = 0
    servo2_direction = "clockwise"

    # Iterate over each combination of speeds and directions for servo1 and servo2
    for servo1_speed in speeds:
        for servo1_direction in directions:
            # Calculate PWM values for each servo based on speed and direction
                    servo1_pwm = 90 + servo1_speed if servo1_direction == "clockwise" else 90 - servo1_speed
                    servo2_pwm = 90 + servo2_speed if servo2_direction == "clockwise" else 90 - servo2_speed

                    # Make sure PWM values are within 0-180
                    servo1_pwm = max(0, min(180, servo1_pwm))
                    servo2_pwm = max(0, min(180, servo2_pwm))

                    # Create payload to send to the ESP8266
                    payload = {
                            "dtype": "speed",
                            "servo1": str(servo1_pwm),
                            "servo2": str(servo2_pwm)
                            }

                    # Send request to ESP8266
                    response = requests.get(esp8266_ip, params=payload)

                    # Print results for this combination
                    print(f"Testing servo1 {servo1_direction} at speed {servo1_speed} (PWM: {servo1_pwm})")
                    print("Response Status Code:", response.status_code)
                    time.sleep(0.5)

if __name__ == "__main__":
    # Run the test for all speed and direction combinations
    print("Testing all speed and direction combinations for servos:")
    #test_all_speed_combinations()
    while True:
        payload = {
                "dtype": "speed",
                "servo1": str(0),
                "servo2": str(0)
                }

        # Send request to ESP8266
        response = requests.get(esp8266_ip, params=payload)
        time.sleep(0.5)




