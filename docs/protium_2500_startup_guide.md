# Protium 2500 Fuel Cell Startup Guide

This guide provides a summary of the essential checks to be performed during the startup of the Protium 2500 fuel cell. It is a supplement to the official user guide, not a replacement. Always refer to the complete user guide for detailed instructions and safety information.

## Hydrogen (H2) System Checks

**CAUTION:** Hydrogen is a highly flammable gas. Handle with extreme care in a well-ventilated area.

*   **Gas Supply:** Use only high purity (99.999%) dry Hydrogen gas.
*   **Pressure Regulation:** Ensure the Hydrogen gas supply is regulated to **0.5-0.7 bar (7.2-10 psig)**.
    *   **Insufficient pressure** can cause cell flooding and performance drops.
    *   **Excessive pressure** can rupture the fuel cell membrane, leading to dangerous leaks and irreversible damage.
*   **Flow Rate:** The pressure regulator must be capable of providing a flow rate of more than **35 L/min**.
*   **Connections:**
    *   Connect the Hydrogen supply to **both** H2 gas inlet connectors.
    *   Ensure all gas tubing and connectors are firm and secure.
*   **Purge Tubing:**
    *   Verify that the two Hydrogen gas purge tubes are securely connected to the H2 gas outlet connectors.
    *   **CRITICAL:** Channel the purge tubing **far away** from the oxidant blower inlets to prevent purged Hydrogen from mixing with the air intake, which could cause a fire.
*   **Leak Check:** The system performs automated stack leakage checks during startup. Monitor the DAQ GUI for any warnings related to "FC Sealing Compromised".

## Electrical System Checks

**CAUTION:** Improper electrical connections can result in equipment damage and electric shock.

*   **External Power Supply:**
    *   Connect a **15-90V, 375W** external power supply.
    *   It is recommended to use a 15-48V power supply to ensure the fuel cell output voltage is always higher, allowing it to power its own Balance-of-Plant (BOP).
    *   Ensure the external power supply is **OFF** during initial setup.
*   **Load Connection:**
    *   Connect your load to the XT-90 load connector.
    *   **Verify correct polarity.**
    *   It is advisable to have an ON/OFF switch for your load and to keep it **OFF** during startup.
*   **Cabling:**
    *   Securely connect the Power/Signal, Stack power output (+ve), and Stack power output (-ve) extension cables between the fuel cell and the Electronic Controller.
    *   Connect the P2 sensor cable from the fuel cell to the P2 sensor port on the controller.
*   **DAQ GUI:**
    *   Connect the Radio modem receiver to a PC and launch the Spectronik DAQ GUI.
    *   Establish communication by selecting the correct COM Port and setting the Baud Rate to 57600.
*   **Startup Sequence:**
    1.  Turn **ON** the external power supply. Wait 5 seconds. The Status LED will blink.
    2.  Click **START** in the DAQ GUI. A "Low H2 Supply" message will appear.
    3.  Turn **ON** the Hydrogen gas supply.
    4.  The system will perform purges and diagnostic checks.
    5.  Once the system enters the "Running Phase" (indicated in the GUI and by a solid white Status LED), it is ready to power your application.
    6.  Turn **ON** your load. Do not draw power beyond 2500W or pull the fuel cell voltage below 48V.
