import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Lecturer Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

# 2. Database Connection & Data Fetching
conn = st.connection("db_connect", type="sql")

@st.cache_data(ttl=600)
def load_data():
    return conn.query("SELECT * FROM lecturers")

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("🎯 Filter Options")

if 'department' in df.columns:
    departments = st.sidebar.multiselect(
        "Select Department(s):",
        options=df['department'].unique(),
        default=df['department'].unique()
    )
    filtered_df = df[df['department'].isin(departments)]
else:
    filtered_df = df.copy()

# 4. Main Dashboard Header & Quick Metrics
st.title("🎓 Lecturer Insights Dashboard")
st.markdown("An interactive overview of academic staff distribution and metrics.")

# Core metric cards remain at the top for a quick baseline overview
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Lecturers", value=len(filtered_df))
with col2:
    if 'department' in df.columns:
        st.metric(label="Departments Represented", value=filtered_df['department'].nunique())
    else:
        st.metric(label="Data Columns", value=len(df.columns))
with col3:
    if 'years_of_experience' in filtered_df.columns:
        avg_exp = round(filtered_df['years_of_experience'].mean(), 1)
        st.metric(label="Avg. Experience (Years)", value=f"{avg_exp} yrs")
    else:
        st.metric(label="Status", value="Database Connected", delta="Live")

st.write("") # Add spacing

# 5. Defining the Tabs (Replaced vertical scrolling sections)
tab1, tab2, tab3 = st.tabs(["📋 Data Roster", "📊 Visual Analytics", "💡 Lecturer Spotlight"])

# --- TAB 1: DATA ROSTER ---
with tab1:
    st.subheader("Lecturer Roster")
    st.markdown("Use the column headers to sort, or use the search box to find specific entries.")
    st.dataframe(
        filtered_df, 
        use_container_width=True, 
        hide_index=True
    )

# --- TAB 2: VISUAL ANALYTICS ---
with tab2:
    st.subheader("Analytical Visualizations")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        if 'department' in filtered_df.columns:
            dept_counts = filtered_df['department'].value_counts().reset_index()
            dept_counts.columns = ['Department', 'Count']
            
            fig_bar = px.bar(
                dept_counts, 
                x='Department', 
                y='Count', 
                color='Department',
                title="Number of Lecturers per Department",
                template="plotly_dark"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Add a 'department' column to visualize departmental distribution.")

    with chart_col2:
        if 'years_of_experience' in filtered_df.columns and 'salary' in filtered_df.columns:
            fig_scatter = px.scatter(
                filtered_df,
                x='years_of_experience',
                y='salary',
                color='department' if 'department' in filtered_df.columns else None,
                hover_name='name' if 'name' in filtered_df.columns else None,
                title="Salary Progression by Experience Level",
                labels={'years_of_experience': 'Years of Experience', 'salary': 'Salary ($)'},
                template="plotly_dark"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Add numerical columns like 'years_of_experience' or 'salary' to unlock scatter analysis.")

# --- TAB 3: SPOTLIGHT ---
with tab3:
    st.subheader("Quick Search & Profile Spotlight")
    if 'name' in filtered_df.columns:
        selected_lecturer = st.selectbox("Pick a lecturer to spotlight:", filtered_df['name'].unique())
        
        # Grab rows for selected lecturer
        lecturer_info = filtered_df[filtered_df['name'] == selected_lecturer].iloc[0]
        
        st.info(f"**Spotlight Profile: {selected_lecturer}**")
        
        # Display the lecturer's details cleanly in a key-value metrics layout
        info_cols = st.columns(len(filtered_df.columns))
        for idx, (col_name, val) in enumerate(lecturer_info.items()):
            with info_cols[idx % len(info_cols)]:
                st.metric(label=col_name.title().replace("_", " "), value=str(val))
    else:
        st.caption("Tip: Ensure your database table has a 'name' column to unlock individual spotlight selectors.")
