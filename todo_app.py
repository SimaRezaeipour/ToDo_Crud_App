import streamlit as st 
import pandas as pd 
from db_fnx import create_table, add_data, view_all_data, view_unique_task, get_task, edit_task_data, delete_data
import plotly.express as px




def main():
	st.title("ToDo App")
	menu = ["Create","Read","Update","Delete"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()
	if choice == "Create":
		st.subheader("Add Items")
		col1,col2 = st.beta_columns(2)
		with col1:
			task = st.text_area("Task To Do")
		with col2:
			task_status = st.selectbox("Status",["ToDo","Doing","Done"])
			task_due_date = st.date_input("Due Date")
		if st.button("Add Task"):
			add_data(task,task_status,task_due_date)
			st.success("Succesfully Added Data: {}".format(task))

	elif choice == "Read":
		st.subheader("View Items")
		result = view_all_data()
		with st.beta_expander("View All Data"):
			df = pd.DataFrame(result, columns = ['Task','Status','Date'])
			st.dataframe(df)
		with st.beta_expander("Task Status"):
			task_df = df['Status'].value_counts().to_frame()
			task_df = task_df.reset_index()
			st.dataframe(task_df)
			p1 = px.pie(task_df,names = 'index', values = "Status")
			st.plotly_chart(p1)

	elif choice == "Update":
		st.subheader("Edit/Update items")
		result = view_all_data()
		with st.beta_expander("Current Data"):
			df = pd.DataFrame(result, columns = ['Task','Status','Date'])
			st.dataframe(df)

		list_of_task = [i[0] for i in view_unique_task()]
		selected_task = st.selectbox("task to Edit",list_of_task)
		selected_result = get_task(selected_task)
		if selected_task:
			task = selected_result[0][0]
			task_status = selected_result[0][1]
			task_due_date = selected_result[0][2]
			col1,col2 = st.beta_columns(2)
			with col1:
				new_task = st.text_area("Task To Do",task)
			with col2:
				new_task_status = st.selectbox(task_status,["ToDo","Doing","Done"])
				new_task_due_date = st.date_input(task_due_date)
			if st.button("Update Task"):
				edit_task_data(new_task, new_task_status, new_task_due_date,task,task_status,task_due_date)
				st.success("Succesfully Updated:: {} To Data:: {}".format(task,new_task))

			result2 = view_all_data()
			with st.beta_expander("Updated Data"):
				df2 = pd.DataFrame(result2, columns = ['Task','Status','Date'])
				st.dataframe(df2)

	else:
		st.subheader("Delete Items")
		result = view_all_data()
		with st.beta_expander("Current Data"):
			df = pd.DataFrame(result, columns = ['Task','Status','Date'])
			st.dataframe(df)
		list_of_task = [i[0] for i in view_unique_task()]
		selected_task = st.selectbox("task to delete",list_of_task)
		st.warning("Do you want to delete the {} ?".format(selected_task))
		if st.button("Delete Task"):
			delete_data(selected_task)
			st.success("Task has been Succesfully deleted")
		result2 = view_all_data()
		with st.beta_expander("Updated Data"):
			df2 = pd.DataFrame(result2, columns = ['Task','Status','Date'])
			st.dataframe(df2)

if __name__=='__main__':
	main()