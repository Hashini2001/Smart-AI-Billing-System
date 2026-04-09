#!/usr/bin/env python
import RPi.GPIO as GPIO
from hx711 import HX711
import time

# Set up GPIO pins and load cell
def setup():
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    hx = HX711(dout_pin=20, pd_sck_pin=21)  

    # Tare the scale (zero it)
    err = hx.zero()
    if err:
        raise ValueError('Failed to tare the load cell. Check connections.')

    print("Tare complete. Load cell ready.")
    return hx

# Function to read raw data and calibrate using known weight
def calibrate_scale(hx):
    # Step 1: Read raw data (without weight) and tare
    input("Remove all weight from the scale and press Enter to tare the scale.")
    hx.zero()  # Tare again just in case
    print("Tare complete. Place a known weight on the scale.")

    # Step 2: Place known weight on the scale
    input("Place a known weight on the scale and press Enter.")
    raw_data = hx.get_data_mean()
    if raw_data:
        print(f"Mean value from the load cell: {raw_data}")
    else:
        raise ValueError("Failed to get a valid reading. Check connections.")

    # Step 3: Input known weight (in grams)
    known_weight = input("Enter the weight (in grams) you placed on the scale: ")
    try:
        known_weight_grams = float(known_weight)
    except ValueError:
        raise ValueError("Invalid input. Please enter a valid number for the weight.")

    # Step 4: Calculate scale ratio
    ratio = raw_data / known_weight_grams
    hx.set_scale_ratio(ratio)  # Set the scale ratio for future conversions
    print(f"Calibration complete. Scale ratio is {ratio:.5f}.")
    
    return hx

# Function to read the calibrated weight in grams
def read_weight(hx):
    print("Reading weight... Press Ctrl+C to stop.")
    while True:
        try:
            weight = hx.get_weight_mean(20)  # Get average weight in grams over 20 samples
            if weight:
                print(f"Weight on the scale: {weight:.2f} grams")
            else:
                print("Invalid reading. Check connections.")
        except (KeyboardInterrupt, SystemExit):
            print("Exiting...")
            break

    GPIO.cleanup()

# Main function to set up, calibrate, and read weight
if __name__ == "__main__":
    hx = setup()  # Set up the HX711 and load cell
    hx = calibrate_scale(hx)  # Calibrate the scale with a known weight
    read_weight(hx)  # Continuously read weight in grams
