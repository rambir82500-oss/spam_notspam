
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import joblib

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="Smart Spam Detector",
#     page_icon="📩",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------------- CUSTOM CSS ----------------
# st.markdown("""
# <style>
# .stApp {
#     background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 55%, #e0f2fe 100%);
# }

# .block-container {
#     padding-top: 2rem;
#     padding-bottom: 2rem;
#     max-width: 1250px;
# }

# .hero {
#     background: linear-gradient(120deg, #312e81, #4f46e5, #0891b2);
#     padding: 35px;
#     border-radius: 22px;
#     color: white;
#     margin-bottom: 25px;
#     box-shadow: 0 12px 30px rgba(79,70,229,0.20);
# }

# .hero h1 {
#     color: white;
#     font-size: 38px;
#     margin-bottom: 8px;
# }

# .hero p {
#     color: #e0e7ff;
#     font-size: 16px;
# }

# .section-title {
#     color: #1e1b4b;
#     font-size: 24px;
#     font-weight: 750;
#     margin-top: 15px;
#     margin-bottom: 12px;
# }

# div[data-testid="stVerticalBlockBorderWrapper"] {
#     background: rgba(255,255,255,0.88);
#     border: 1px solid #e0e7ff;
#     border-radius: 18px;
#     padding: 15px;
#     box-shadow: 0 5px 20px rgba(30,41,59,0.05);
# }

# div.stButton > button {
#     background: linear-gradient(90deg, #4f46e5, #0891b2);
#     color: white;
#     border: none;
#     border-radius: 12px;
#     padding: 12px 22px;
#     font-weight: 700;
#     min-height: 48px;
#     transition: 0.2s;
# }

# div.stButton > button:hover {
#     color: white;
#     border: 1px solid #4f46e5;
#     box-shadow: 0 5px 16px rgba(79,70,229,0.25);
# }

# textarea {
#     border-radius: 12px !important;
# }

# [data-testid="stMetric"] {
#     background: white;
#     border: 1px solid #e0e7ff;
#     padding: 18px;
#     border-radius: 16px;
#     box-shadow: 0 4px 15px rgba(30,41,59,0.05);
# }

# footer {
#     visibility: hidden;
# }

# #MainMenu {
#     visibility: hidden;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- LOAD MODEL ----------------
# @st.cache_resource
# def load_models():
#     model = joblib.load("spam_detector.pkl")
#     vectorizer = joblib.load("vectorizer.pkl")
#     return model, vectorizer

# try:
#     model, vectorizer = load_models()
# except Exception as e:
#     st.error(f"Model loading error: {e}")
#     st.info("Check that both .pkl files are in the same folder as app.py.")
#     st.stop()

# # ---------------- SESSION HISTORY ----------------
# if "history" not in st.session_state:
#     st.session_state.history = []

# # ---------------- SIDEBAR ----------------
# with st.sidebar:
#     st.markdown("## 📩 Smart Detector")
#     st.caption("Machine Learning Project")
#     st.divider()

#     page = st.radio(
#         "NAVIGATION",
#         ["🏠 Home", "📊 Dashboard", "📋 History", "ℹ️ About"]
#     )

#     st.divider()
#     st.markdown("### 🛡️ Message Security")
#     st.write("Check suspicious messages with your trained ML model.")
#     st.caption("Built with Python + Streamlit")

# # ---------------- HERO HEADER ----------------
# st.markdown("""
# <div class="hero">
#     <h1>📩 Smart Spam Detector</h1>
#     <p>Intelligent message classification powered by Machine Learning.</p>
#     <p>✨ Simple • Fast • Interactive</p>
# </div>
# """, unsafe_allow_html=True)

# # ---------------- HOME PAGE ----------------
# if page == "🏠 Home":

#     st.markdown('<div class="section-title">🔍 Analyze Your Message</div>',
#                 unsafe_allow_html=True)

#     left, right = st.columns([1.6, 1])

#     with left:
#         with st.container(border=True):
#             st.markdown("### ✉️ Message Input")
#             message = st.text_area(
#                 "Enter your SMS or message below",
#                 placeholder="Example: Congratulations! You have won a free prize. Click here...",
#                 height=180,
#                 label_visibility="collapsed"
#             )

#             check = st.button(
#                 "🚀 Analyze Message",
#                 use_container_width=True
#             )

#             if check:
#                 if not message.strip():
#                     st.warning("Please enter a message first.")
#                 else:
#                     features = vectorizer.transform([message])
#                     prediction = model.predict(features)[0]

#                     # Assumes training labels: 1 = Spam, 0 = Not Spam
#                     spam_label = 1
#                     result = (
#                         "Spam" if prediction == spam_label
#                         else "Not Spam"
#                     )

#                     st.session_state.history.append({
#                         "Message": message,
#                         "Prediction": result
#                     })

#                     st.session_state.last_result = result
#                     st.session_state.last_message = message

#                     if hasattr(model, "predict_proba"):
#                         probs = model.predict_proba(features)[0]
#                         classes = list(model.classes_)
#                         if spam_label in classes:
#                             st.session_state.last_probability = (
#                                 float(probs[classes.index(spam_label)]) * 100
#                             )
#                         else:
#                             st.session_state.last_probability = None
#                     else:
#                         st.session_state.last_probability = None

#             if "last_result" in st.session_state:
#                 st.divider()
#                 if st.session_state.last_result == "Spam":
#                     st.error("🚨 SPAM MESSAGE DETECTED")
#                     st.write("⚠️ Be careful. Avoid unknown links and requests for personal details.")
#                 else:
#                     st.success("✅ MESSAGE CLASSIFIED AS NOT SPAM")
#                     st.write("This message was classified as not spam by the model.")

#                 probability = st.session_state.get("last_probability")
#                 if probability is not None:
#                     st.progress(
#                         min(1.0, max(0.0, probability / 100)),
#                         text=f"Spam probability: {probability:.1f}%"
#                     )

#     with right:
#         with st.container(border=True):
#             st.markdown("### 💡 How It Works")
#             st.markdown("""
#             **01 — Enter Message**  
#             Paste the SMS you want to check.

#             **02 — AI Analysis**  
#             The trained model analyzes the text.

#             **03 — Get Result**  
#             View the predicted message category.

#             **04 — Track Results**  
#             Explore charts and your prediction history.
#             """)
#             st.divider()
#             st.markdown("### 🔐 Safety Tips")
#             st.write("• Never share OTPs or passwords.")
#             st.write("• Avoid suspicious links.")
#             st.write("• Verify unexpected prize messages.")

#     st.markdown('<div class="section-title">📈 Your Activity</div>',
#                 unsafe_allow_html=True)

#     total = len(st.session_state.history)
#     spam = sum(
#         row["Prediction"] == "Spam"
#         for row in st.session_state.history
#     )
#     safe = total - spam

#     c1, c2, c3 = st.columns(3)
#     c1.metric("📨 Total Checked", total)
#     c2.metric("🚨 Spam Messages", spam)
#     c3.metric("✅ Not Spam", safe)

# # ---------------- DASHBOARD ----------------
# elif page == "📊 Dashboard":

#     st.markdown('<div class="section-title">📊 Analytics Dashboard</div>',
#                 unsafe_allow_html=True)

#     history = st.session_state.history

#     if not history:
#         st.info("Analyze some messages on the Home page to generate charts.")
#     else:
#         df = pd.DataFrame(history)
#         total = len(df)
#         spam = int((df["Prediction"] == "Spam").sum())
#         safe = int((df["Prediction"] == "Not Spam").sum())

#         a, b, c = st.columns(3)
#         a.metric("Total Messages", total)
#         b.metric("Spam Detected", spam)
#         c.metric("Not Spam", safe)

#         col1, col2 = st.columns(2)

#         with col1:
#             with st.container(border=True):
#                 st.markdown("### 📊 Message Comparison")
#                 fig, ax = plt.subplots(figsize=(6, 4))
#                 bars = ax.bar(
#                     ["Spam", "Not Spam"],
#                     [spam, safe],
#                     color=["#ef4444", "#10b981"],
#                     width=0.55
#                 )
#                 ax.set_ylabel("Number of Messages")
#                 ax.set_ylim(bottom=0)
#                 ax.spines[["top", "right"]].set_visible(False)
#                 ax.bar_label(bars, padding=3)
#                 fig.tight_layout()
#                 st.pyplot(fig)
#                 plt.close(fig)

#         with col2:
#             with st.container(border=True):
#                 st.markdown("### 🍩 Classification Share")
#                 fig, ax = plt.subplots(figsize=(6, 4))

#                 if total > 0:
#                     ax.pie(
#                         [spam, safe],
#                         labels=["Spam", "Not Spam"],
#                         colors=["#ef4444", "#10b981"],
#                         autopct="%1.1f%%",
#                         startangle=90,
#                         wedgeprops={
#                             "width": 0.42,
#                             "edgecolor": "white"
#                         }
#                     )
#                 ax.axis("equal")
#                 fig.tight_layout()
#                 st.pyplot(fig)
#                 plt.close(fig)

#         st.caption("Charts are based on messages checked in this session.")

# # ---------------- HISTORY ----------------
# elif page == "📋 History":

#     st.markdown('<div class="section-title">📋 Prediction History</div>',
#                 unsafe_allow_html=True)

#     if st.session_state.history:
#         df = pd.DataFrame(st.session_state.history)

#         search = st.text_input("🔎 Search messages")
#         if search:
#             df = df[
#                 df["Message"].str.contains(
#                     search, case=False, na=False
#                 )
#             ]

#         st.dataframe(df, use_container_width=True, hide_index=True)

#         csv = df.to_csv(index=False).encode("utf-8")
#         st.download_button(
#             "⬇️ Download CSV Report",
#             data=csv,
#             file_name="spam_detection_history.csv",
#             mime="text/csv"
#         )

#         if st.button("🗑️ Clear All History"):
#             st.session_state.history = []
#             st.session_state.pop("last_result", None)
#             st.session_state.pop("last_message", None)
#             st.session_state.pop("last_probability", None)
#             st.rerun()
#     else:
#         st.info("No messages analyzed yet. Go to Home to get started.")

# # ---------------- ABOUT ----------------
# elif page == "ℹ️ About":

#     st.markdown('<div class="section-title">ℹ️ About This Project</div>',
#                 unsafe_allow_html=True)

#     with st.container(border=True):
#         st.markdown("### 🤖 Machine Learning Spam Detection")
#         st.write(
#             "This application uses a pre-trained machine learning model "
#             "and a text vectorizer to classify messages."
#         )

#         st.markdown("#### 🧰 Technologies Used")
#         st.markdown("""
#         - **Python** — Core programming language
#         - **Streamlit** — Web application interface
#         - **Scikit-learn** — Machine learning tools
#         - **Joblib** — Loading saved model files
#         - **Matplotlib** — Data visualizations
#         - **Pandas** — Prediction history and CSV export
#         """)

#         st.warning(
#             "Predictions depend on the training data and model quality. "
#             "A message marked Not Spam is not guaranteed to be safe."
#         )

# # ---------------- FOOTER ----------------
# st.divider()
# st.markdown(
#     "<center style='color:#64748b;'>"
#     "📩 Smart Spam Detector | Built with Python & Streamlit"
#     "</center>",
#     unsafe_allow_html=True
# )


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Spam Detector",
    page_icon="📩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DARK THEME CSS ----------------
st.markdown("""
<style>
/* Main background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
.block-container {
    background: linear-gradient(135deg, #080d1b, #111827, #101b35) !important;
    color: #f8fafc !important;
}

[data-testid="stHeader"] {
    background: #080d1b !important;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

/* Hero section */
.hero {
    background: linear-gradient(120deg, #312e81, #4f46e5, #0891b2);
    padding: 35px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 12px 30px rgba(79,70,229,0.3);
}

.hero h1 {
    color: white !important;
    font-size: 38px;
}

.hero p {
    color: #e0e7ff !important;
    font-size: 16px;
}

/* Section titles */
.section-title {
    color: #c4b5fd !important;
    font-size: 24px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 12px;
}

/* Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111827 !important;
    border: 1px solid #374151 !important;
    border-radius: 18px;
    padding: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.25);
}

/* Metrics */
[data-testid="stMetric"] {
    background: #1f2937 !important;
    border: 1px solid #374151 !important;
    padding: 18px;
    border-radius: 16px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #f9fafb !important;
}

/* Text */
h1, h2, h3, h4, p, label,
.stMarkdown, .stCaption {
    color: #f3f4f6;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #0891b2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px;
    padding: 12px 22px;
    font-weight: 700;
    min-height: 48px;
}

div.stButton > button:hover {
    box-shadow: 0 5px 16px rgba(79,70,229,0.4);
    border: 1px solid #818cf8 !important;
}

/* Input fields */
textarea,
input,
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div {
    background-color: #111827 !important;
    color: #f9fafb !important;
    border-color: #4b5563 !important;
    border-radius: 10px !important;
}

textarea::placeholder,
input::placeholder {
    color: #9ca3af !important;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #0b1120 !important;
    color: white !important;
}

/* Dataframe and tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #111827 !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Progress bar */
[data-testid="stProgressBar"] {
    background: #374151 !important;
}

/* Hide Streamlit footer */
footer, #MainMenu {
    visibility: hidden;
}

hr {
    border-color: #374151 !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_models():
    model = joblib.load("spam_detector.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer


try:
    model, vectorizer = load_models()
except Exception as e:
    st.error(f"Model loading error: {e}")
    st.info("Check that both .pkl files are in the same folder as app.py.")
    st.stop()


# ---------------- SESSION HISTORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 📩 Smart Detector")
    st.caption("Machine Learning Project")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["🏠 Home", "📊 Dashboard", "📋 History", "ℹ️ About"]
    )

    st.divider()
    st.markdown("### 🛡️ Message Security")
    st.write("Check suspicious messages with your trained ML model.")
    st.caption("Built with Python + Streamlit")


# ---------------- HERO HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>📩 Smart Spam Detector</h1>
    <p>Intelligent message classification powered by Machine Learning.</p>
    <p>✨ Simple • Fast • Interactive</p>
</div>
""", unsafe_allow_html=True)


# ---------------- HOME PAGE ----------------
if page == "🏠 Home":

    st.markdown(
        '<div class="section-title">🔍 Analyze Your Message</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.6, 1])

    with left:
        with st.container(border=True):
            st.markdown("### ✉️ Message Input")

            message = st.text_area(
                "Enter your SMS or message below",
                placeholder="Example: Congratulations! You have won a free prize. Click here...",
                height=180,
                label_visibility="collapsed"
            )

            check = st.button(
                "🚀 Analyze Message",
                use_container_width=True
            )

            if check:
                if not message.strip():
                    st.warning("Please enter a message first.")
                else:
                    features = vectorizer.transform([message])
                    prediction = model.predict(features)[0]

                    # Assumes 1 = Spam and 0 = Not Spam
                    spam_label = 1

                    result = (
                        "Spam" if prediction == spam_label
                        else "Not Spam"
                    )

                    st.session_state.history.append({
                        "Message": message,
                        "Prediction": result
                    })

                    st.session_state.last_result = result
                    st.session_state.last_message = message

                    if hasattr(model, "predict_proba"):
                        probs = model.predict_proba(features)[0]
                        classes = list(model.classes_)

                        if spam_label in classes:
                            st.session_state.last_probability = (
                                float(probs[classes.index(spam_label)]) * 100
                            )
                        else:
                            st.session_state.last_probability = None
                    else:
                        st.session_state.last_probability = None

            if "last_result" in st.session_state:
                st.divider()

                if st.session_state.last_result == "Spam":
                    st.error("🚨 SPAM MESSAGE DETECTED")
                    st.write(
                        "⚠️ Be careful. Avoid unknown links and requests for personal details."
                    )
                else:
                    st.success("✅ MESSAGE CLASSIFIED AS NOT SPAM")
                    st.write(
                        "This message was classified as not spam by the model."
                    )

                probability = st.session_state.get("last_probability")

                if probability is not None:
                    st.progress(
                        min(1.0, max(0.0, probability / 100)),
                        text=f"Spam probability: {probability:.1f}%"
                    )

    with right:
        with st.container(border=True):
            st.markdown("### 💡 How It Works")

            st.markdown("""
            **01 — Enter Message**

            Paste the SMS you want to check.

            **02 — AI Analysis**

            The trained model analyzes the text.

            **03 — Get Result**

            View the predicted message category.

            **04 — Track Results**

            Explore charts and your prediction history.
            """)

            st.divider()
            st.markdown("### 🔐 Safety Tips")
            st.write("• Never share OTPs or passwords.")
            st.write("• Avoid suspicious links.")
            st.write("• Verify unexpected prize messages.")

    st.markdown(
        '<div class="section-title">📈 Your Activity</div>',
        unsafe_allow_html=True
    )

    total = len(st.session_state.history)

    spam = sum(
        row["Prediction"] == "Spam"
        for row in st.session_state.history
    )

    safe = total - spam

    c1, c2, c3 = st.columns(3)
    c1.metric("📨 Total Checked", total)
    c2.metric("🚨 Spam Messages", spam)
    c3.metric("✅ Not Spam", safe)


# ---------------- DASHBOARD ----------------
elif page == "📊 Dashboard":

    st.markdown(
        '<div class="section-title">📊 Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    history = st.session_state.history

    if not history:
        st.info("Analyze some messages on the Home page to generate charts.")

    else:
        df = pd.DataFrame(history)

        total = len(df)
        spam = int((df["Prediction"] == "Spam").sum())
        safe = int((df["Prediction"] == "Not Spam").sum())

        a, b, c = st.columns(3)
        a.metric("Total Messages", total)
        b.metric("Spam Detected", spam)
        c.metric("Not Spam", safe)

        col1, col2 = st.columns(2)

        # Bar chart
        with col1:
            with st.container(border=True):
                st.markdown("### 📊 Message Comparison")

                fig, ax = plt.subplots(
                    figsize=(6, 4),
                    facecolor="#111827"
                )
                ax.set_facecolor("#1f2937")
                ax.tick_params(colors="#f9fafb")
                ax.yaxis.label.set_color("#f9fafb")

                for spine in ax.spines.values():
                    spine.set_color("#6b7280")

                bars = ax.bar(
                    ["Spam", "Not Spam"],
                    [spam, safe],
                    color=["#ef4444", "#10b981"],
                    width=0.55
                )

                ax.set_ylabel("Number of Messages")
                ax.set_ylim(bottom=0)
                ax.spines[["top", "right"]].set_visible(False)

                ax.bar_label(
                    bars,
                    padding=3,
                    color="white"
                )

                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

        # Doughnut chart
        with col2:
            with st.container(border=True):
                st.markdown("### 🍩 Classification Share")

                fig, ax = plt.subplots(
                    figsize=(6, 4),
                    facecolor="#111827"
                )
                ax.set_facecolor("#1f2937")

                if total > 0:
                    ax.pie(
                        [spam, safe],
                        labels=["Spam", "Not Spam"],
                        colors=["#ef4444", "#10b981"],
                        autopct="%1.1f%%",
                        startangle=90,
                        wedgeprops={
                            "width": 0.42,
                            "edgecolor": "#1f2937"
                        },
                        textprops={"color": "#f9fafb"}
                    )

                ax.axis("equal")
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

        st.caption("Charts are based on messages checked in this session.")


# ---------------- HISTORY ----------------
elif page == "📋 History":

    st.markdown(
        '<div class="section-title">📋 Prediction History</div>',
        unsafe_allow_html=True
    )

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)

        search = st.text_input("🔎 Search messages")

        if search:
            df = df[
                df["Message"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV Report",
            data=csv,
            file_name="spam_detection_history.csv",
            mime="text/csv"
        )

        if st.button("🗑️ Clear All History"):
            st.session_state.history = []
            st.session_state.pop("last_result", None)
            st.session_state.pop("last_message", None)
            st.session_state.pop("last_probability", None)
            st.rerun()

    else:
        st.info("No messages analyzed yet. Go to Home to get started.")


# ---------------- ABOUT ----------------
elif page == "ℹ️ About":

    st.markdown(
        '<div class="section-title">ℹ️ About This Project</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown("### 🤖 Machine Learning Spam Detection")

        st.write(
            "This application uses a pre-trained machine learning model "
            "and a text vectorizer to classify messages."
        )

        st.markdown("#### 🧰 Technologies Used")

        st.markdown("""
        - **Python** — Core programming language
        - **Streamlit** — Web application interface
        - **Scikit-learn** — Machine learning tools
        - **Joblib** — Loading saved model files
        - **Matplotlib** — Data visualizations
        - **Pandas** — Prediction history and CSV export
        """)

        st.warning(
            "Predictions depend on the training data and model quality. "
            "A message marked Not Spam is not guaranteed to be safe."
        )


# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    "<center style='color:#9ca3af;'>"
    "📩 Smart Spam Detector | Built with Python & Streamlit"
    "</center>",
    unsafe_allow_html=True
)
