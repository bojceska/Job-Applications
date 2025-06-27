#jobtrackerapp.py
import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Job Application Tracker")

if "applications" not in st.session_state:
    st.session_state.applications = []

with st.form["Add new application"]:
    company = st.text_input("Company")
    role = st.text_input("Role")
    date_applied = st.date_input("Date Applied")
    status = st.selectbox("Status",["Applied", "Interviewing", "Offer", "Rejected", "Awaiting Response","Withdrawn"])
    notes = st.text_area("Notes")
    link = st.text_input("Job Link")
    submitted = st.form_submit_button("Add Job")

    if submitted:
        new_entry= {
            "Company": company,
            "Role": role,
            "Date Applied": date_applied,
            "Status": status,
            "Notes": notes,
            "Link": link
        }
        st.session_state.applications.append(new_entry)
        st.success(f"Added job at {company}")

if st.session_state.applications:
    df = pd.DataFrame(st.session_state.applications)
    status_filter = st.selectbox("Filter by Status", ["All"] + df["Status"].unique().tolist())
    if status_filter != "All":
        df = df[df["Status"] == status_filter]
        st.dataframe(df)

        csv = df.to_csv(index = False).econde('uts-8')
        st.download_button("Download CSV", csv, "job_applications.csv", "text/csv")

    else:
        st.info("No job applications yet. Add one")
             