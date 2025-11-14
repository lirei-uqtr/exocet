import streamlit as st
from fuel_cell_controller import FuelCellController
import time

def main():
    st.title("Protium-2500 Fuel Cell Controller")

    if 'controller' not in st.session_state:
        st.session_state.controller = None

    port = st.text_input("Enter the COM port (e.g., COM7):", 'COM7')

    if st.button("Connect"):
        if st.session_state.controller is None:
            st.session_state.controller = FuelCellController(port)
            st.session_state.controller.connect()
            st.success(f"Connected to {port}")
        else:
            st.warning("Already connected.")

    if st.button("Disconnect"):
        if st.session_state.controller:
            st.session_state.controller.disconnect()
            st.session_state.controller = None
            st.info("Disconnected.")
        else:
            st.warning("Not connected.")

    if st.session_state.controller:
        st.sidebar.header("Commands")
        if st.sidebar.button("Start Fuel Cell"):
            st.session_state.controller.start_fuel_cell()
        if st.sidebar.button("End Fuel Cell"):
            st.session_state.controller.end_fuel_cell()
        if st.sidebar.button("Set Fans to Auto"):
            st.session_state.controller.set_fans_auto()
        if st.sidebar.button("Set Blowers to Auto"):
            st.session_state.controller.set_blowers_auto()
        if st.sidebar.button("Manual Purge"):
            st.session_state.controller.manual_purge()
        if st.sidebar.button("Get Firmware Version"):
            st.session_state.controller.get_version()

        st.sidebar.subheader("Fan Speed")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("-1%"):
                st.session_state.controller.decrease_fan_speed_1()
            if st.button("-5%"):
                st.session_state.controller.decrease_fan_speed_5()
        with col2:
            if st.button("+1%"):
                st.session_state.controller.increase_fan_speed_1()
            if st.button("+5%"):
                st.session_state.controller.increase_fan_speed_5()

        st.sidebar.subheader("Blower Intensity")
        col3, col4 = st.sidebar.columns(2)
        with col3:
            if st.button("-3%"):
                st.session_state.controller.decrease_blower_intensity_3()
        with col4:
            if st.button("+3%"):
                st.session_state.controller.increase_blower_intensity_3()

        st.header("Real-time Data")
        data_placeholder = st.empty()

        if 'latest_data' not in st.session_state:
            st.session_state.latest_data = {}
        if 'raw_messages' not in st.session_state:
            st.session_state.raw_messages = []

        while st.session_state.controller and st.session_state.controller.serial and st.session_state.controller.serial.is_open:
            while not st.session_state.controller.data_queue.empty():
                data = st.session_state.controller.data_queue.get()
                if "raw" in data:
                    st.session_state.raw_messages.append(data["raw"])
                else:
                    st.session_state.latest_data.update(data)
            
            with data_placeholder.container():
                st.metric("Data Queue Size", st.session_state.controller.data_queue.qsize())
                if st.session_state.latest_data:
                    st.json(st.session_state.latest_data)
                else:
                    st.text("Waiting for data...")
                
                st.subheader("Raw Messages")
                st.text_area("Messages from the fuel cell:", "\n".join(st.session_state.raw_messages), height=200)
            
            time.sleep(0.5)
            st.rerun()

if __name__ == "__main__":
    main()