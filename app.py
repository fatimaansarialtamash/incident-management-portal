
import pandas as pd
import streamlit as st
import plotly.express as px

from database import (
    save_incident,
    get_all_incidents,
    get_incident_counts,
    generate_incident_id,
    update_incident_status,
    search_incident,
    get_incidents_by_priority
)

from datetime import datetime

st.set_page_config(
    page_title="Incident Management Portal",
    layout="wide"
)

st.title("🚨 Incident Management Portal")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Create Incident",
        "Search Incident",
        "Reports"
    ]
)

if page == "Dashboard":
    pass

elif page == "Create Incident":
    pass

elif page == "Search Incident":
    pass

elif page == "Reports":
    pass
total, open_count, progress_count, closed_count = get_incident_counts()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Incidents",
        total
    )

with col2:
    st.metric(
        "Open",
        open_count
    )

with col3:
    st.metric(
        "In Progress",
        progress_count
    )

with col4:
    st.metric(
        "Closed",
        closed_count
    )

st.divider()

incident_id = generate_incident_id()

st.text_input(
    "Incident ID",
    value=incident_id,
    disabled=True
)


title = st.text_input(
    "Incident Title"
)

description = st.text_area(
    "Description"
)

priority = st.selectbox(
    "Priority",
    ["Low", "Medium", "High"]
)

status = st.selectbox(
    "Status",
    ["Open", "In Progress", "Closed"]
)

assigned_to = st.text_input(
    "Assigned To"
)

st.subheader("🔍 Search Incident")

search_id = st.text_input(
    "Enter Incident ID"
)

if st.button("Search", key="search_btn"):

    incident = search_incident(search_id)

    if incident:

        st.success("Incident Found")

        st.write(f"Incident ID : {incident[0]}")
        st.write(f"Title : {incident[1]}")
        st.write(f"Description : {incident[2]}")
        st.write(f"Priority : {incident[3]}")
        st.write(f"Status : {incident[4]}")
        st.write(f"Assigned To : {incident[5]}")

    else:

        st.error(
            "Incident Not Found"
        )
        
if st.button(
    "Create Incident",
    key="create_btn"
):
    created_date = datetime.now().strftime(
        "%d-%b-%Y %H:%M"
    )

    save_incident(
        incident_id,
        title,
        description,
        priority,
        status,
        assigned_to,
        created_date
    )

    st.success(
        "Incident Created Successfully ✅"
    )

st.divider()

st.subheader("🎯 Filter Incidents By Priority")

selected_priority = st.selectbox(
    "Select Priority",
    ["All", "High", "Medium", "Low"]
)

if selected_priority == "All":
    incidents = get_all_incidents()
else:
    incidents = get_incidents_by_priority(
        selected_priority
    )

st.table(incidents)

st.divider()

st.subheader("📋 Incident Records")

st.divider()

st.subheader("📥 Export Incident Report")

if st.button(
    "Export to Excel",
    key="export_btn"
):

    incidents = get_all_incidents()

    df = pd.DataFrame(
        incidents,
        columns=[
            "Incident ID",
            "Title",
            "Description",
            "Priority",
            "Status",
            "Assigned To"
        ]
    )

    df.to_excel(
        "Incident_Report.xlsx",
        index=False
    )

    st.success(
        "Excel Report Generated ✅"
    )


st.divider()

st.subheader("📊 Incident Status Dashboard")

data = {
    "Status": [
        "Open",
        "In Progress",
        "Closed"
    ],
    "Count": [
        open_count,
        progress_count,
        closed_count
    ]
}

df = pd.DataFrame(data)

st.bar_chart(
    df.set_index("Status")
)

fig = px.pie(
    values=[
        open_count,
        progress_count,
        closed_count
    ],
    names=[
        "Open",
        "In Progress",
        "Closed"
    ],
    title="Incident Status Distribution"
)

st.plotly_chart(fig)

incidents = get_all_incidents()

if incidents:

    df_incidents = pd.DataFrame(
        incidents,
        columns=[
            "Incident ID",
            "Title",
            "Description",
            "Priority",
            "Status",
            "Assigned To",
            "Created Date"
        ]
    )

    st.table(df_incidents)

else:

    st.info(
        "No incidents available."
    )

st.divider()

st.subheader("🔄 Update Incident Status")

update_id = st.text_input(
    "Incident ID to Update"
)

new_status = st.selectbox(
    "Select New Status",
    ["Open", "In Progress", "Closed"]
)

if st.button(
    "Update Status",
    key="update_btn"
):

    update_incident_status(
        update_id,
        new_status
    )

    st.success(
        "Status Updated Successfully ✅"
    )