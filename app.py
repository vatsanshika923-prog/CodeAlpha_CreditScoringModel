import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Credit Scoring Model",
    page_icon="💳",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main{
    background-color:#f8f9fa;
}

h1,h2,h3{
    color:#1f4e79;
}

.stButton>button{
    background:#1f77b4;
    color:white;
    border-radius:8px;
    width:100%;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#125d98;
}

.pred-good{
    padding:20px;
    border-radius:10px;
    background:#d4edda;
    color:#155724;
    font-size:22px;
    font-weight:bold;
}

.pred-bad{
    padding:20px;
    border-radius:10px;
    background:#f8d7da;
    color:#721c24;
    font-size:22px;
    font-weight:bold;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

st.title("💳 Credit Scoring Model")
st.write("Predict whether a customer is **Creditworthy** using the trained Random Forest model.")

# ---------------- LOAD MODEL ---------------- #

@st.cache_resource
def load_model():
    model = joblib.load("models/best_model.pkl")
    return model

model = load_model()

# ---------------- COLUMN NAMES ---------------- #

column_names = [
    "Checking_Account",
    "Duration",
    "Credit_History",
    "Purpose",
    "Credit_Amount",
    "Savings_Account",
    "Employment",
    "Installment_Rate",
    "Personal_Status_Sex",
    "Other_Debtors",
    "Residence_Since",
    "Property",
    "Age",
    "Other_Installment_Plans",
    "Housing",
    "Existing_Credits",
    "Job",
    "Dependents",
    "Telephone",
    "Foreign_Worker",
    "Risk"
]
# ---------------- LOAD DATASET ---------------- #

@st.cache_data
def load_dataset():

    df = pd.read_csv(
        "dataset/german.data",
        sep=" ",
        header=None,
        names=column_names
    )

    return df


df = load_dataset()


# ---------------- RECREATE LABEL ENCODERS ---------------- #

categorical_cols = df.select_dtypes(include="object").columns

encoders = {}

for col in categorical_cols:

    le = LabelEncoder()

    le.fit(df[col])

    encoders[col] = le


# ---------------- SIDEBAR ---------------- #

st.sidebar.title("Navigation")

st.sidebar.info(
"""
### CodeAlpha Internship

**Project**
Credit Scoring Model

**Algorithm**
Random Forest

**Developer**
Anshika Vats
"""
)

st.sidebar.markdown("---")

st.sidebar.success("Model Loaded Successfully")


# ---------------- INPUT SECTION ---------------- #

st.header("Customer Information")

col1, col2 = st.columns(2)

with col1:

    checking_account = st.selectbox(
        "Checking Account",
        encoders["Checking_Account"].classes_
    )

    duration = st.number_input(
        "Loan Duration (Months)",
        min_value=1,
        max_value=100,
        value=24
    )

    credit_history = st.selectbox(
        "Credit History",
        encoders["Credit_History"].classes_
    )

    purpose = st.selectbox(
        "Purpose",
        encoders["Purpose"].classes_
    )

    credit_amount = st.number_input(
        "Credit Amount",
        min_value=100,
        max_value=50000,
        value=3000
    )

    savings_account = st.selectbox(
        "Savings Account",
        encoders["Savings_Account"].classes_
    )

    employment = st.selectbox(
        "Employment",
        encoders["Employment"].classes_
    )

    installment_rate = st.slider(
        "Installment Rate",
        1,
        4,
        2
    )

    personal_status = st.selectbox(
        "Personal Status & Sex",
        encoders["Personal_Status_Sex"].classes_
    )

    other_debtors = st.selectbox(
        "Other Debtors",
        encoders["Other_Debtors"].classes_
    )
    with col2:

     residence_since = st.slider(
     "Residence Since (Years)",
     min_value=1,
     max_value=4,
     value=2
)

    property_type = st.selectbox(
        "Property",
        encoders["Property"].classes_
    )

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    other_installment = st.selectbox(
        "Other Installment Plans",
        encoders["Other_Installment_Plans"].classes_
    )

    housing = st.selectbox(
        "Housing",
        encoders["Housing"].classes_
    )

    existing_credits = st.slider(
        "Existing Credits",
        1,
        4,
        1
    )

    job = st.selectbox(
        "Job",
        encoders["Job"].classes_
    )

    dependents = st.slider(
        "Dependents",
        1,
        2,
        1
    )

    telephone = st.selectbox(
        "Telephone",
        encoders["Telephone"].classes_
    )

    foreign_worker = st.selectbox(
        "Foreign Worker",
        encoders["Foreign_Worker"].classes_
    )

st.markdown("<br>", unsafe_allow_html=True)

predict = st.button("Predict Credit Risk")

if predict:

    try:

        input_data = [
            encoders["Checking_Account"].transform([checking_account])[0],
            duration,
            encoders["Credit_History"].transform([credit_history])[0],
            encoders["Purpose"].transform([purpose])[0],
            credit_amount,
            encoders["Savings_Account"].transform([savings_account])[0],
            encoders["Employment"].transform([employment])[0],
            installment_rate,
            encoders["Personal_Status_Sex"].transform([personal_status])[0],
            encoders["Other_Debtors"].transform([other_debtors])[0],
            residence_since,
            encoders["Property"].transform([property_type])[0],
            age,
            encoders["Other_Installment_Plans"].transform([other_installment])[0],
            encoders["Housing"].transform([housing])[0],
            existing_credits,
            encoders["Job"].transform([job])[0],
            dependents,
            encoders["Telephone"].transform([telephone])[0],
            encoders["Foreign_Worker"].transform([foreign_worker])[0]
        ]

        input_df = pd.DataFrame([input_data], columns=[
            "Checking_Account",
            "Duration",
            "Credit_History",
            "Purpose",
            "Credit_Amount",
            "Savings_Account",
            "Employment",
            "Installment_Rate",
            "Personal_Status_Sex",
            "Other_Debtors",
            "Residence_Since",
            "Property",
            "Age",
            "Other_Installment_Plans",
            "Housing",
            "Existing_Credits",
            "Job",
            "Dependents",
            "Telephone",
            "Foreign_Worker"
        ])

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]

        st.markdown("---")
        st.subheader("Prediction Result")

        if prediction == 1:
            st.markdown(
                '<div class="pred-good">✅ Customer is Creditworthy</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="pred-bad">❌ Customer is High Credit Risk</div>',
                unsafe_allow_html=True
            )

        st.markdown("### Prediction Probability")

        good = probability[1] * 100
        bad = probability[0] * 100

        st.progress(float(good / 100))

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Creditworthy Probability",
                f"{good:.2f}%"
            )

        with c2:
            st.metric(
                "Risk Probability",
                f"{bad:.2f}%"
            )

    except Exception as e:
        st.error(f"Prediction Error: {e}")

st.markdown("---")

st.markdown(
"""
<center>

Developed by **Anshika Vats**

CodeAlpha Machine Learning Internship

Random Forest Credit Scoring Model

</center>
""",
unsafe_allow_html=True
)