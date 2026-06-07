# FreeriderTR MTB Engineering Rules DSL
# This file defines deterministic rules for the compatibility and risk engines.

[COMPATIBILITY]
RULE fork_travel_limit:
    IF fork.travel > frame.max_travel + 20
    THEN set_status(INCOMPATIBLE)
    REASON "Fork travel exceeds frame safe limits by over 20mm, causing extreme geometry distortion."

RULE wheel_size_mismatch:
    IF fork.wheel_size != frame.front_wheel_size
    THEN set_status(INCOMPATIBLE)
    REASON "Fork wheel size does not match frame specification."

RULE rear_wheel_mullet:
    IF rear_wheel.size == 27.5 AND frame.rear_wheel_size == 29 AND frame.mullet_compatible == false
    THEN set_status(HIGH_RISK)
    REASON "Running a 27.5 rear wheel on a dedicated 29er frame significantly drops the bottom bracket, increasing pedal strike risk."

RULE boost_mismatch:
    IF wheel.is_boost != fork.is_boost
    THEN set_status(INCOMPATIBLE)
    REASON "Boost spacing mismatch between wheel and fork/frame."

RULE drivetrain_speed_mismatch:
    IF shifter.speeds != cassette.speeds OR derailleur.speeds != cassette.speeds
    THEN set_status(INCOMPATIBLE)
    REASON "Drivetrain components speed count mismatch."

[RISK]
RULE extreme_rotor_trail:
    IF front_rotor.size >= 220 AND frame.category == "Trail"
    THEN add_risk("Overkill Braking", LOW)
    REASON "220mm rotors on a trail bike are overkill and add unnecessary unsprung weight."

RULE dh_fork_on_enduro:
    IF fork.type == "Dual Crown" AND frame.category == "Enduro"
    THEN add_risk("Headtube Overstress", HIGH)
    REASON "Dual crown forks put excessive leverage on enduro frame headtubes, risking catastrophic failure."

[WEAR]
RULE metallic_pads_wet:
    IF brakes.pad_type == "Resin" AND rider.riding_conditions == "Wet/Mud"
    THEN add_wear_factor("Brake Pads", 2.5)
    REASON "Resin pads wear extremely quickly in wet/muddy conditions."
