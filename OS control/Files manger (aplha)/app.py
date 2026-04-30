import streamlit as st
import test2 as core   # 🔥 tera backend

st.set_page_config(page_title="AI File Manager", layout="wide")

st.title("📂 AI File Manager")
st.write("Automatically classify & organize your files")

# -------------------------------
# USER INPUT
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    hours = st.selectbox("Select Time Range (Hours)", [1, 5, 12, 24])

with col2:
    base_path = st.text_input(
        "Destination Folder",
        value=r"D:\games\AI File_manager"
    )

st.write("### 📂 Destination Folder")

st.caption("💡 Example paths:")
st.write("> Destination Folder -> D:\games\AI File_manager")
# st.code(r"D:\games\AI File_manager")
# st.code(r"C:\Users\DHRUV\Documents\Sorted Files")

# -------------------------------
# RUN BUTTON
# -------------------------------
if st.button("🚀 Run"):

    progress = st.progress(0)
    status = st.empty()

    # -------------------------------
    # STEP 1: SCAN FILES
    # -------------------------------
    status.info("📂 Scanning files...")
    progress.progress(10)

    files = core.get_recent_files(hours)

    if not files:
        status.warning("⚠️ No recent files found")
        st.stop()

    st.success(f"✅ Found {len(files)} files")

    # -------------------------------
    # STEP 2: MODEL LOADING
    # -------------------------------
    status.info("🤖 Loading AI model... (may take few seconds)")
    progress.progress(40)

    mapping = {idx: file for idx, file in enumerate(files)}

    # 🔥 spinner for heavy model
    with st.spinner("Running AI model..."):
        res = core.model_check(mapping)

    st.write("### 🧠 File Analysis")

    for path, val in res.items():

        if path == "None":
            st.warning("⚠️ No valid files detected by model")
            continue

        file_name = core.os.path.basename(path)
        subject_code = val[0]
        subject_name = val[1]

        st.markdown(f"""
    📄 **File:** `{file_name}`  
    📂 **Original Path:** `{path}`  

    🤖 **Model Prediction:**  
    - Subject: **{subject_name}**  
    - Code: **{subject_code}**
    """)

    st.divider()

    # -------------------------------
    # STEP 3: MOVE FILES
    # -------------------------------
    status.info("📦 Moving files...")
    progress.progress(75)

    logs = core.move_all_files(res, base_path)

    # -------------------------------
    # STEP 4: SHOW LOGS
    # -------------------------------
    progress.progress(100)
    status.success("🎉 Process Completed!")

    st.write("### 📦 Operation Logs")

    for log in logs:
        if "✅" in log:
            st.success(log)
        elif "⚠️" in log:
            st.warning(log)
        else:
            st.error(log)