import streamlit as st
import time
import pandas as pd
import paho.mqtt.client as mqtt

# --- KONFIGURASI MQTT ---
MQTT_BROKER = "localhost" # Jika jalankan di luar docker
MQTT_PORT = 1883
MQTT_TOPIC = "simulasi/distribusi"

st.set_page_config(page_title="Simulasi Sistem Terdistribusi ITK", layout="wide")

st.title("🌐 Simulasi Interaktif Model Komunikasi")
st.markdown("Implementasi menggunakan **Python** dan **Mosquitto MQTT Broker**.")

# --- SIDEBAR INTERAKSI ---
st.sidebar.header("Konfigurasi Parameter")
latency = st.sidebar.slider("Simulasi Network Latency (detik)", 0.1, 2.0, 0.5)
msg_count = st.sidebar.number_input("Jumlah Pesan", 1, 10, 5)

# --- LOGIKA MQTT (PUBLISH-SUBSCRIBE) ---
def on_message(client, userdata, message):
    st.session_state.received_msgs.append(f"📥 Sub: Menerima '{str(message.payload.decode())}'")

if 'received_msgs' not in st.session_state:
    st.session_state.received_msgs = []

# --- TAMPILAN TAB ---
tab1, tab2, tab3 = st.tabs(["Request-Response", "Publish-Subscribe (MQTT)", "Analisis Perbandingan"])

with tab1:
    st.header("Model: Request-Response (Synchronous)")
    st.write("Analogi: HTTP Request. Client menunggu balasan penuh dari Server.")
    
    if st.button("Jalankan Req-Res"):
        start = time.time()
        for i in range(msg_count):
            st.write(f"📤 **Client:** Mengirim Request #{i+1}")
            time.sleep(latency) # Simulasi pengolahan server
            st.write(f"✅ **Server:** Mengirim Response #{i+1}")
        duration = time.time() - start
        st.session_state.req_res_time = duration
        st.success(f"Selesai dalam {duration:.2f} detik")

with tab2:
    st.header("Model: Publish-Subscribe (Asynchronous)")
    st.write("Analogi: MQTT Broker. Publisher mengirim pesan tanpa menunggu penerima.")
    
    if st.button("Jalankan MQTT Pub/Sub"):
        try:
            client = mqtt.Client()
            client.connect("broker", 1883, 60) # Nama 'broker' sesuai di docker-compose
            
            start = time.time()
            for i in range(msg_count):
                msg = f"Data Event #{i+1}"
                client.publish(MQTT_TOPIC, msg)
                st.write(f"📣 **Pub:** Broadcast '{msg}' ke Broker")
                time.sleep(0.1) # Asinkron: Publisher tidak menunggu lama
            
            duration = time.time() - start
            st.session_state.pub_sub_time = duration
            st.info("Pesan telah dikirim ke Broker secara non-blocking.")
        except:
            st.error("Gagal terhubung ke Mosquitto Broker. Pastikan Docker Compose sudah berjalan.")

with tab3:
    st.header("Mekanisme Perbandingan Metrik")
    if 'req_res_time' in st.session_state and 'pub_sub_time' in st.session_state:
        df = pd.DataFrame({
            'Model': ['Request-Response', 'Pub-Sub (MQTT)'],
            'Total Time (s)': [st.session_state.req_res_time, st.session_state.pub_sub_time]
        })
        st.bar_chart(df.set_index('Model'))
        st.write("**Hasil Analisis:** Model Pub-Sub (MQTT) jauh lebih efisien dalam penggunaan waktu karena tidak terjadi *blocking* pada sisi pengirim.")