# jobtrackerapp.py
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Job Tracker", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Add Job", "Job List", "Analytics", "Chatbot"])

# Initialize session state
if "applications" not in st.session_state:
    st.session_state.applications = []

# Page: Add Job
if page == "Add Job":
    st.title("Add a New Job Application")
    with st.form("Add new application"):
        company = st.text_input("Company")
        role = st.text_input("Role")
        date_applied = st.date_input("Date Applied", value=datetime.today())
        status = st.selectbox("Status", ["Applied", "Interviewing", "Offer", "Rejected", "Awaiting Response", "Withdrawn"])
        notes = st.text_area("Notes")
        link = st.text_input("Job Link")
        submitted = st.form_submit_button("Add Job")

        if submitted:
            new_entry = {
                "Company": company,
                "Role": role,
                "Date Applied": date_applied,
                "Status": status,
                "Notes": notes,
                "Link": link
            }
            st.session_state.applications.append(new_entry)
            st.success(f"Added job at {company}")

# Page: Job List
elif page == "Job List":
    st.title("List of Job Applications")
    if st.session_state.applications:
        df = pd.DataFrame(st.session_state.applications)
        status_filter = st.selectbox("Filter by Status", ["All"] + df["Status"].unique().tolist())

        if status_filter != "All":
            df = df[df["Status"] == status_filter]

        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "job_applications.csv", "text/csv")
    else:
        st.info("No job applications yet. Add one on the 'Add Job' page.")

# Page: Analytics
elif page == "Analytics":
    st.title("Job Application Analytics")

    if st.session_state.applications:
        df = pd.DataFrame(st.session_state.applications)

        # Count applications per status
        status_counts = df["Status"].value_counts().to_dict()

        # Define all possible statuses to ensure all are shown
        all_statuses = ["Applied", "Interviewing", "Offer", "Rejected", "Awaiting Response", "Withdrawn"]
        
        # Create cards in columns
        cols = st.columns(3)  # 3 cards per row
        for i, status in enumerate(all_statuses):
            count = status_counts.get(status, 0)
            with cols[i % 3]:
                st.metric(label=status, value=count)

    else:
        st.info("No data to show. Add job applications first.")


# Page: Chatbot
elif page == "Chatbot":
    st.title("Job Tracker Assistant 🤖")
    st.info("Chatbot feature coming soon! You could integrate a chatbot like OpenAI Assistant here.")
