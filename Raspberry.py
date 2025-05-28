
from machine import Pin, ADC, PWM
import utime


rain_sensor_analog = ADC(Pin(27))
rain_sensor_digital = Pin(16, Pin.IN)
buzzer = PWM(Pin(15))


low_landslide_threshold = 55
moderate_landslide_threshold = 65
soil_wet_threshold = 30000

def figure_out_landslide_chance(rain_percentage, soil_status, rain_detected):
    """Figure out the chance of a landslide happening based on what the sensors are telling us."""
    if rain_detected == "rain detected" and soil_status == "wet":
        if rain_percentage >= moderate_landslide_threshold:
            return "High chance of landslide"
        elif rain_percentage >= low_landslide_threshold:
            return "Moderate chance of landslide"
        else:
            return "Low chance of landslide"
    return "No chance of landslide"

def control_buzzer(landslide_chance):
    """Control the buzzer based on how likely a landslide is."""
    if landslide_chance == "High chance of landslide":
        buzzer.duty_u16(65535)  # Full volume
        buzzer.freq(1000)  # High pitch
    elif landslide_chance == "Moderate chance of landslide":
        buzzer.duty_u16(32768)  # Medium volume
        buzzer.freq(1000)  # High pitch
    elif landslide_chance == "Low chance of landslide":
        buzzer.duty_u16(16384)  # Low volume
        buzzer.freq(500)  # Lower pitch
    else:
        buzzer.duty_u16(0)  # Turn off the buzzer

def get_sensor_readings():
    """Grab the latest data from our sensors."""
    raw_rain_value = rain_sensor_analog.read_u16()
    rain_percentage = 100 - (raw_rain_value / 65535) * 100
    soil_status = "wet" if raw_rain_value > soil_wet_threshold else "dry"
    rain_detected = "rain detected" if rain_sensor_digital.value() == 0 else "no rain"
    temperature = 23 + (utime.ticks_us() % 1000) / 1000.0  # Simulating temperature
    return rain_percentage, soil_status, rain_detected, temperature

def main_program():
    try:
        while True:
            
            rain_percentage, soil_status, rain_detected, temperature = get_sensor_readings()

            
            landslide_chance = figure_out_landslide_chance(rain_percentage, soil_status, rain_detected)

            
            control_buzzer(landslide_chance)

            
            print(f"Rain Sensor Status: {rain_detected}")
            print(f"Rain Percentage: {rain_percentage:.2f}%")
            print(f"Current Temperature: {temperature:.2f}°C")
            print(f"Landslide Chance: {landslide_chance}")
            print("------------------------------")

            
            utime.sleep(2)

    except KeyboardInterrupt:
        print("Someone stopped the program manually.")
    finally:
        buzzer.duty_u16(0)
        print("Buzzer has been turned off.")


if __name__ == "__main__":
    main_program()
