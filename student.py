# student_management_unique.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------- In-Memory Database -------------------
if "students" not in st.session_state:
    st.session_state.students = []

# ------------------- Helper Functions -------------------
def add_student(name, age, gender, course):
    student_id = len(st.session_state.students) + 1
    st.session_state.students.append({
        "ID": student_id,
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Course": course
    })

def update_student(student_id, name, age, gender, course):
    for student in st.session_state.students:
        if student["ID"] == student_id:
            student.update({"Name": name, "Age": age, "Gender": gender, "Course": course})

def delete_student(student_id):
    st.session_state.students = [s for s in st.session_state.students if s["ID"] != student_id]

def search_students(query):
    return [s for s in st.session_state.students if query.lower() in s["Name"].lower() or query.lower() in s["Course"].lower()]

# ------------------- Streamlit App -------------------
st.set_page_config(page_title="🎓 Student Management System", layout="wide")
st.title("🎓 Interactive Student Management System")

menu = ["Add Student", "View Students", "Update Student", "Delete Student", "Search & Stats"]
choice = st.sidebar.selectbox("Menu", menu)

# ------------------- Add Student -------------------
if choice == "Add Student":
    st.subheader("Add a New Student")
    with st.form(key="add_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        course = st.text_input("Course")
        submitted = st.form_submit_button("Add Student")
        if submitted:
            if name and course:
                add_student(name, age, gender, course)
                st.success(f"Student {name} added successfully!")
            else:
                st.error("Please fill all fields.")

# ------------------- View Students -------------------
elif choice == "View Students":
    st.subheader("All Students")
    if st.session_state.students:
        df = pd.DataFrame(st.session_state.students)
        st.dataframe(df)
    else:
        st.info("No students found.")

# ------------------- Update Student -------------------
elif choice == "Update Student":
    st.subheader("Update Student Details")
    if st.session_state.students:
        student_list = [f"{s['ID']} - {s['Name']}" for s in st.session_state.students]
        selected = st.selectbox("Select Student to Update", student_list)
        student_id = int(selected.split(" - ")[0])
        student = next(s for s in st.session_state.students if s["ID"] == student_id)
        
        with st.form(key="update_form"):
            name = st.text_input("Name", student["Name"])
            age = st.number_input("Age", min_value=1, max_value=120, step=1, value=student["Age"])
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male","Female","Other"].index(student["Gender"]))
            course = st.text_input("Course", student["Course"])
            submitted = st.form_submit_button("Update Student")
            if submitted:
                update_student(student_id, name, age, gender, course)
                st.success(f"Student {name} updated successfully!")
    else:
        st.info("No students to update.")

# ------------------- Delete Student -------------------
elif choice == "Delete Student":
    st.subheader("Delete a Student")
    if st.session_state.students:
        student_list = [f"{s['ID']} - {s['Name']}" for s in st.session_state.students]
        selected = st.selectbox("Select Student to Delete", student_list)
        student_id = int(selected.split(" - ")[0])
        if st.button("Delete Student"):
            delete_student(student_id)
            st.warning(f"Student ID {student_id} deleted successfully!")
    else:
        st.info("No students to delete.")

# ------------------- Search & Statistics -------------------
elif choice == "Search & Stats":
    st.subheader("Search Students")
    query = st.text_input("Enter Name or Course to Search")
    if query:
        results = search_students(query)
        if results:
            st.success(f"Found {len(results)} result(s)")
            st.table(pd.DataFrame(results))
        else:
            st.warning("No matching students found.")

    st.subheader("Student Age Distribution")
    if st.session_state.students:
        ages = [s["Age"] for s in st.session_state.students]
        plt.figure(figsize=(6,4))
        plt.hist(ages, bins=range(0, 121, 5), color='skyblue', edgecolor='black')
        plt.xlabel("Age")
        plt.ylabel("Number of Students")
        plt.title("Age Distribution of Students")
        st.pyplot(plt)
    else:
        st.info("No students to visualize.")
