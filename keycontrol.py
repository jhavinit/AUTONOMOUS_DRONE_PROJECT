import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil

#- Importing Tkinter: sudo apt-get install python-tk
import Tkinter as tk


#-- Connect to the vehicle
print('Connecting...1')
vehicle = connect('udp:192.168.43.125:14550)

#-- Setup the commanded flying speed
gnd_speed = 5 # [m/s]

#-- Define arm and takeoff
def arm_and_takeoff(altitude):

   
   print("Arming motors")
   vehicle.mode = VehicleMode("GUIDED")
   vehicle.armed = True

   while not vehicle.armed: time.sleep(1)

   print("Taking Off")
   vehicle.simple_takeoff(altitude)

   while True:
      v_alt = vehicle.location.global_relative_frame.alt
      print(">> Altitude = %.1f m"%v_alt)
      if v_alt >= altitude - 1.0:
          print("Target altitude reached")
          break
      time.sleep(1)
      
 #-- Define the function for sending mavlink velocity command in body frame
def set_velocity_body(vehicle, vx, vy, vz):
    
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
    
    
#-- Key event function
def key(event):
    if event.char == event.keysym: #-- standard keys
        if event.keysym == 'r':
            print("r pressed >> Set the vehicle to LAND")
            vehicle.mode = VehicleMode("LAND")
            
    else: #-- non standard keys
        if event.keysym == 'Up':
            set_velocity_body(vehicle, gnd_speed, 0, 0)
        elif event.keysym == 'Down':
            set_velocity_body(vehicle,-gnd_speed, 0, 0)
        elif event.keysym == 'Left':
            set_velocity_body(vehicle, 0, -gnd_speed, 0)
        elif event.keysym == 'Right':
            set_velocity_body(vehicle, 0, gnd_speed, 0)
    
    
#---- MAIN FUNCTION
#- Takeoff
arm_and_takeoff(10)

    
#- Read the keyboard with tkinter
root = tk.Tk()
print(">> Control the drone with the arrow keys. Press r for RTL mode")
root.bind_all('<Key>', key)
root.mainloop()


vehicle.mode = VehicleMode("LAND")
print("land")
