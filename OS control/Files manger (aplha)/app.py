import streamlit as st
import time

st.set_page_config(page_title="AI File Manager", layout="wide")

st.title("📂 AI File Manager")
st.write("Automatically classify & organize your files")

# -------------------------------
# USER INPUT
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    hours = st.selectbox("Select Time Range (Hours)", [1, 5, 12, 24], key="hours")

with col2:
    base_path = st.text_input(
        "Destination Folder",
        value=r"D:\games\AI File_manager",
        key="path"
    )

st.caption("💡 Example: D:\\games\\AI File_manager")

# -------------------------------
# SINGLE RUN BUTTON
# -------------------------------
if st.button("🚀 Run", key="run_main"):

    status = st.empty()
    progress = st.progress(0)

    # -------------------------------
    # FAKE LOADING ANIMATION
    # -------------------------------
    messages = [
        "🤖 Initializing model...",
        "📦 Loading weights...",
        "⚙️ Setting up environment...",
        "🧠 Almost ready..."
    ]

    for i, msg in enumerate(messages):
        status.info(msg)
        progress.progress((i + 1) * 10)
        time.sleep(0.5)

    # -------------------------------
    # REAL IMPORT (HEAVY)
    # -------------------------------
    with st.spinner("🚀 Finalizing model..."):
        import test2 as core

    progress.progress(40)

    # -------------------------------
    # STEP 1: SCAN FILES
    # -------------------------------
    status.info("📂 Scanning files...")
    files = core.get_recent_files(hours)

    if not files:
        status.warning("⚠️ No recent files found")
        st.stop()

    st.success(f"✅ Found {len(files)} files")

    # -------------------------------
    # STEP 2: MODEL
    # -------------------------------
    status.info("🤖 Running AI model...")
    mapping = {idx: file for idx, file in enumerate(files)}

    with st.spinner("Processing files..."):
        res = core.model_check(mapping)

    # -------------------------------
    # DISPLAY OUTPUT (CLEAN)
    # -------------------------------
    st.write("### 🧠 File Analysis")

    for path, val in res.items():

        if path == "None":
            st.warning("⚠️ No valid files detected")
            continue

        file_name = core.os.path.basename(path)

        with st.container(border=True):
            st.write(f"📄 **{file_name}**")
            st.caption(path)
            st.success(f"Subject: {val[1]}")
            st.info(f"Code: {val[0]}")

    # -------------------------------
    # STEP 3: MOVE FILES
    # -------------------------------
    status.info("📦 Moving files...")
    progress.progress(80)

    logs = core.move_all_files(res, base_path)

    # -------------------------------
    # STEP 4: LOGS
    # -------------------------------
    st.write("### 📦 Operation Logs")

    for log in logs:
        if "✅" in log:
            st.success(log)
        elif "⚠️" in log:
            st.warning(log)
        else:
            st.error(log)

    progress.progress(100)
    status.success("🎉 Process Completed!")