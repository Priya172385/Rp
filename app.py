import streamlit as st
st.title("🌡 Temperature Converter")
temp = st.number_input("Temperature")
unit = st.radio("Convert to", ["Celsius","Fahrenheit"])
if st.button("Convert"):
    if unit=="Celsius":
        st.write(f"{(temp-32)*5/9:.2f} °C")
    else:
        st.write(f"{temp*9/5 + 32:.2f} °F")





