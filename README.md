Stack:
    Logic:
        Preset light timings
        Include values for time to effect Light timings
        Trainer:
            Read from Data to decide values for timing
    Data: # Not implemented, see Simulation
        Lights
        Detect cars and an data point to lights
    Control:
        Change lights based on timings file
        Ensure safe operation of lights is maintained
    Simulation: # Replaces Data until properly configured
        Display light status
        Display car locaitons
        DATA:
            Spawn cars from surrounding lights (static lights) with paths through the dynamic light
            
