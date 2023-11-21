import streamlit as st
import pymysql
import pandas as pd
import re
import department
# import employee
# import company
# import cmn
# Connect to the MySQL database

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    database="attrition"
)
cursor = conn.cursor()
st.set_page_config(
    page_title="Attrition Analysis",
    page_icon="📈",
)
if "flag" not in st.session_state:
    st.session_state.flag = False

# Function to fetch data from the database
def fetch_data():
    query = "SELECT * FROM emp_reg"
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    return df

if "user" not in st.session_state:
    st.session_state.user = None

def is_valid_email(email):
    # Regular expression to validate email address
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def is_valid_phone(phone):
    # Regular expression to validate phone number
    pattern = r'^[0-9]{10}$'
    return re.match(pattern, phone)

returns=["Invalid password. Password must be at least 8 characters long.","Invalid password. Password must include at least 1 special character (-@$!%*?&).","Invalid password. Password must include at least 1 capital letter.","Invalid password. Password must include at least 1 number."]

def is_valid_password(password):
    if len(password) < 8:
        return 2
    if not re.search(r'[-@$!%*?&]', password):
        return 3
    if not any(char.isupper() for char in password):
        return 4
    if not any(char.isdigit() for char in password):
        return 5

    return 1



def create_emp():
    st.subheader("Sign Up to Create an Employee Account now!")
    email = st.text_input("Enter your email")
    password=st.text_input("Enter your password",type="password")
    conpassword=st.text_input("Confirm your password",type="password")
    if(password==None or conpassword==None):
        st.markdown("Passwords can't be empty")
    elif(password==conpassword and password):    
        name=st.text_input("Enter your name")
        
        companyid=st.text_input("Enter your company ID")
        
        if(companyid is not None):
            cursor.execute(f"SELECT department_name FROM  department where cmpid=%s",(companyid,))
            data = cursor.fetchall()
            depts=[row[0] for row in data]
            sel = st.selectbox("Choose an option:", depts)
            if(depts is not None):
                cursor.execute(f"SELECT dept_id FROM department WHERE department_name='{sel}'")
                result = cursor.fetchone()
                if result:
                    dept_id = result[0]
                else:
                    # Handle the case where no matching record is found
                    dept_id=None
                    st.warning("No matching department found.")
            else:
                st.markdown("No departments are registered")
            # dept_id=1
            
            role=st.text_input("Enter your role")

            query = f"SELECT COUNT(*) FROM emp_reg"
            cursor.execute(query)
            row_count = cursor.fetchone()[0]
            while True:
                if dept_id is not None:
                    id=dept_id+str(row_count)
                    exis=cursor.execute("SELECT * from emp_reg where empid=%s",(id,))
                    if(exis>0):
                        row_count=row_count+1
                    else:
                        break
                
            if st.button("Sign Up"):
                if cursor.execute("SELECT * FROM emp_reg WHERE    email=%s", (email,)):
                    st.error("Email already exists. Please choose a  different one.")
                elif(not is_valid_email(email)):
                    st.error("Invalid email")
                # elif not is_valid_password(password):
                #     st.error("Invalid password. Password must be at least   8 characters long and include at least 1 special  character (-@$!%*?&), 1 capital letter, and 1 number.")
                elif(is_valid_password(password)!=1):
                    st.error(returns[is_valid_password(password)-2])
                else:
                    # Insert the new user into the Users table
                    query = f"SELECT COUNT(*) FROM emp_Reg"
                    cursor.execute(query)
                    row_count = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO emp_reg(empid,empname,dept_id,role,companyid,email,password) VALUES(%s, %s,  %s, %s, %s, %s, %s)",(id,name,dept_id,role,companyid,email, password))  
                    # You may modify the AreaID as per your requirement
                    conn.commit()
                    st.success("Account created! You can now sign in.")
    elif(password!=conpassword and password):
        st.markdown("Your passwords didnot match")


def create_comp():
    st.subheader("Sign Up to Create a Company Account now!")
    email = st.text_input("Enter company email")
    password=st.text_input("Enter your password",type="password")
    conpassword=st.text_input("Confirm your password",type="password")
    if(password==conpassword and password):
        cmpname=st.text_input("Enter name of the company")
        products=st.text_input("Enter the products of your company")
        query = f"SELECT COUNT(*) FROM emp_reg"
        cursor.execute(query)
        row_count = cursor.fetchone()[0]
        if(len(cmpname)>5):
            k=cmpname[:5]
        else:
            k=cmpname
        while True:
            id=k+str(row_count)
            exis = cursor.execute(f"SELECT * from company where cmpid=%s",(id,))
            if(exis>0):
                row_count=row_count+1
            else:
                break
        if st.button("Sign Up"):
            if not is_valid_email(email):
                st.error("Invalid email address. Please enter a valid email.")
            elif cursor.execute("SELECT * FROM emp_reg WHERE    email=%s", (email,)):
                st.error("Username already exists. Please choose a  different one.")
            elif(is_valid_password(password)!=1):
                    st.error(returns[is_valid_password(password)-2])
            else:
                # Insert the new user into the Users table
                query = f"SELECT COUNT(*) FROM emp_Reg"
                cursor.execute(query)
                row_count = cursor.fetchone()[0]
                cursor.execute("INSERT INTO company VALUES(%s, %s, %s, %s, %s)",(id,cmpname,products,email,password))  
                # You may modify the AreaID as per your requirement
                conn.commit()
                st.success("Account created! You can now sign in.")
    elif(password!=conpassword and password):
        st.markdown("Passwords didnot match")    



def create_dept():
    st.subheader("Signup for department")
    cmpid=st.text_input("Enter your company ID")
    email=st.text_input("Enter the mail ID of the department")
    password=st.text_input("Enter the password",type="password")
    conpassword=st.text_input("Confirm your password",type="password")
    k=cursor.execute(f"SELECT * FROM company where cmpid=%s",(cmpid,))
    if(password==conpassword and password and k>0):
        
        dept_name=st.text_input("Enter the name of the department")
        rsp=st.text_input("Enter the responsibility of the department")
        
        query = f"SELECT COUNT(*) FROM department"
        cursor.execute(query)
        row_count = cursor.fetchone()[0]
        while True:
            id=cmpid+str(row_count)
            exis = cursor.execute(f"SELECT * from department where dept_id=%s",(id,))
            if(exis>0):
                row_count=row_count+1
            else:
                break
        if st.button("Sign Up"):
            if not is_valid_email(email):
                st.error("Invalid email address. Please enter a valid email.")
            elif cursor.execute("SELECT * FROM emp_reg WHERE    email=%s", (email,)):
                st.error("Username already exists. Please choose a  different one.")
            elif(is_valid_password(password)!=1):
                st.error(returns[is_valid_password(password)-2])
                st.markdown("Password is strong")
            else:
                # Insert the new user into the Users table
                query = f"SELECT COUNT(*) FROM emp_Reg"
                cursor.execute(query)
                row_count = cursor.fetchone()[0]
                cursor.execute("INSERT INTO department VALUES(%s, %s, %s, %s,%s,%s)",(id,dept_name,rsp,cmpid,email,password))  
                # You may modify the AreaID as per your requirement
                conn.commit()
                st.success("Account created! You can now sign in.")
    elif(password!=conpassword or not password):
        st.markdown("Enter proper passwords")
    else:
        st.markdown("No companies present as of your company ID")  

def employee(empid):
    st.subheader("Employee Page")
    sel=st.selectbox("Select one",["Profile","Resign","Show resignations of your department"])
    if(sel=="Resign"):
        feedback(empid)
    elif(sel=="Profile"):
        cursor.execute("SELECT * FROM emp_reg where empid=%s",(empid,))
        prof=cursor.fetchall()[0]
        cursor.execute("SELECT companyname from company where cmpid=%s",(prof[4]))
        cmpname=cursor.fetchall()[0]
        cursor.execute("SELECT department_name from department where dept_id=%s",(prof[2]))
        dep=cursor.fetchall()[0]
        if(prof and cmpname and dep):
            st.write("Employee name : ",prof[1])
            st.write("Employee ID : ",prof[0])        
            st.write("Department Name : ",dep[0])
            st.write("Role : ",prof[3])
            st.write("Company ID : ",prof[4])
            st.write("Department Mail ID : ",prof[5])
        else:
            st.error("profile not found")
        # pass
    else:
        k=1
        cursor.execute("SELECT empname, role, email FROM emp_reg INNER JOIN feedbacks ON emp_reg.empid = feedbacks.empid and emp_reg.dept_id=feedbacks.dept_id")
        emp=(cursor.fetchall())
        st.subheader("Resignation Data:")
        for emps in emp:
            if(emps):
                st.write(f"**Employee number {k}**")
                st.write("Name : ",emps[0])
                st.write("Role : ",emps[1])
                st.write("Email : ",emps[2])
                k=k+1
                print()
            else:
                st.error("No employees have resigned from your department")
    
def feedback(empid):
    time=st.number_input("Enter the time span which you have worked in the company in years")
    reason=st.text_area("Enter the reason for resignation",max_chars=400)
    fdbk=st.text_input("Feedback on management or work environment")
    suggestions=st.text_area("Provide some improvents needed")
    exp=st.slider("Ratings from 1 to 5 about the overall experience", min_value=1, max_value=5, step=1)
    # st.markdown(empid)
    cursor.execute("SELECT dept_id FROM emp_Reg where empid=%s",(empid,))
    result = cursor.fetchone()
    # st.write(result[0])
    if result is not None:
        dept_id = result[0]
    # Continue processing with dept_id
    else:
    # Handle the case where no rows were returned
        print("No matching records found.")

    if st.button("Apply for resignation"):
        if (time and reason and fdbk and suggestions and exp):
            cursor.execute("SELECT * FROM requesthr where empid=%s",(empid))
            rem=cursor.fetchall()
            if(rem):
                st.error("You have already applied for resignation")
            else:
                if result:
                    cursor.execute("INSERT INTO requesthr() values(%s,%s,%s,%s,%s,%s,%s)",(empid,dept_id,time,reason,fdbk,suggestions,exp))
                    conn.commit()
                    st.success("Applied for resignation successfully")
        else:
            st.error("Enter all the fields mandatorily")
    
def company(companyid):
    st.subheader("Welcome to Official Company page")
    sel=st.selectbox("Select one",["Profile","Market Attrition","View Resigned employees"])
    if(sel=="Profile"):
        cursor.execute("SELECT * FROM company where cmpid=%s",(companyid,))
        prof=cursor.fetchall()[0]
        st.write("Company name : ",prof[1])
        st.write("Company ID : ",prof[0])
        st.write("Products : ",prof[2])
        st.write("Official Mail ID : ",prof[3])
    elif(sel=="Market Attrition"):
        department.main()
    else:
        # st.write(companyid)
        cursor.execute(f"SELECT department_name FROM  department where cmpid=%s",(companyid,))
        data = cursor.fetchall()
        depts=[row[0] for row in data]
        sel = st.selectbox("Choose the department:", depts)
        if(depts is not None):
            cursor.execute(f"SELECT dept_id FROM department WHERE department_name='{sel}'")
            result = cursor.fetchone()
            if result:
                dept_id = result[0]
                k=1
                cursor.execute("SELECT empname, role, email FROM emp_reg INNER JOIN feedbacks ON emp_reg.empid = feedbacks.empid and  feedbacks.dept_id=%s",(dept_id,))
                emp=(cursor.fetchall())
                st.subheader("Resignation Data:")
                for emps in emp:
                    if(emps):
                        st.write(f"**Employee number {k}**")
                        st.write("Name : ",emps[0])
                        st.write("Role : ",emps[1])
                        st.write("Email : ",emps[2])
                        k=k+1
                        print()
                    else:
                        st.error("No employees have resigned from your department")
                
            else:
                # Handle the case where no matching record is found
                dept_id=None
                st.warning("No matching department found.")
            
        else:
            st.markdown("No departments are registered")
    
    

def delete_row(table_name, empid):
    cursor.execute(f"DELETE FROM {table_name} WHERE empid = %s", (empid,))
    conn.commit()




def approve(deptid):
    cursor.execute("SELECT * FROM requesthr where dept_id=%s",(deptid,))
    data = cursor.fetchall()
    if(data):
        for row in data:
                cursor.execute("SELECT empname,role,email FROM emp_reg where empid=%s",(row[0]))
                det=list(cursor.fetchone())
                st.write("Employee ID : ",row[0])
                st.write("Employee Name : ",det[0])
                st.write("Reason for resignation : ",row[3])
                st.write("Employee Email : ",det[2])
                st.write("Employee Role : ",det[1])
                # st.write(f"{det[2]}")
                # st.write(f"Employee ID :{row[0]}\n Name : {det[0]}")
                # st.write(f"Employee ID :{row[0]}\n Name :{det[0]}\n Reason : {row[3]}\n Email :{det[2]}\n Role :{det[1]} ")
                approve_button = st.button("Approve")
                deny_button = st.button("Deny")

                if approve_button:
                    cursor.execute("INSERT INTO feedbacks VALUES(%s,%s,%s,%s,%s,%s,%s)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                    # delete_row("requesthr", row[0])
                    # delete_row("emp_reg", row[0])
                    cursor.execute("DELETE FROM requesthr WHERE empid = %s",(row[0],))
                    cursor.execute("UPDATE emp_reg SET resgn=1 WHERE empid=%s",(row[0]))
                    conn.commit()
                    st.success(f"Approved: {row[0]}")

                elif deny_button:
                    delete_row("requesthr", row[0])
                    st.warning(f"Denied resignation for {row[1]}")
                print("\n\n")   
    else:
        st.error("No requests for resignation")  
           
def dept(deptid):
    st.subheader("Welcome to HR's page")
    sel=st.selectbox("Select one",["Profile","Market attrition","Approve resignation","View Resigned employees"])
    if(sel=="Profile"):
        cursor.execute("SELECT * FROM department where dept_id=%s",(deptid,))
        prof=cursor.fetchall()[0]
        st.write("Department name : ",prof[1])
        st.write("Department ID : ",prof[0])
        st.write("Responsibility : ",prof[2])
        st.write("Company ID : ",prof[3])
        st.write("Department Mail ID : ",prof[4])
    elif(sel=="Market attrition"):
        department.main()
    elif(sel=="Approve resignation"):
        approve(deptid)
    else:
        k=1
        cursor.execute("SELECT empname, role, email FROM emp_reg INNER JOIN feedbacks ON emp_reg.empid = feedbacks.empid and emp_reg.dept_id=feedbacks.dept_id")
        emp=(cursor.fetchall())
        st.subheader("Resignation Data:")
        for emps in emp:
            if(emps):
                st.write(f"**Employee number {k}**")
                st.write("Name : ",emps[0])
                st.write("Role : ",emps[1])
                st.write("Email : ",emps[2])
                k=k+1
                print()
            else:
                st.error("No employees have resigned from your department")

def resigned():
    st.subheader("You have already resigned from the company")

def signin(k):
    st.subheader("Sign In")
    mail = st.text_input(f"Enter {k} mail ID")
    password = st.text_input("Enter the password", type="password")
    
    if st.button("Sign In"):
        if k == "Company":
            try:
                cursor.execute("SELECT cmpid FROM company WHERE email=%s AND password=%s", (mail, password))
                kl = cursor.fetchone()[0]
                c=company
            except:
                st.error("Invalid username/password")

        elif k == "HR":
            try:
                cursor.execute("SELECT dept_id FROM department WHERE email=%s AND password=%s", (mail, password))
                kl= cursor.fetchone()[0]
                c=dept
            except:
                st.error("Invalid username/password")
        elif k == "Employee":
            try:
                cursor.execute("SELECT empid FROM emp_reg WHERE email=%s AND password=%s", (mail, password))
                kl = cursor.fetchone()[0]
                c=employee
            except:
                st.error("Invalid username/password")
        try:
            if kl:
                st.success(f"Sign in successful. Welcome")
                if(k=="Employee"):
                    cursor.execute("SELECT * FROM emp_reg where empid=%s and resgn=%s",(kl,1))
                    sn=cursor.fetchone()
                    if(sn):
                        c=resigned()
                    else:
                        pass
                c(kl)
                st.session_state.user=k
                st.session_state.user_name=kl
            else:
                st.error("Invalid username/password")
                st.session_state.flag=None
        except:
            pass
        # return k1


def main():
    st.header("Welcome to Attrition Analysis System")
    empid=None
    cmpid=None
    deptid=None
    if st.session_state.user:
        k=st.session_state.user
        kl=st.session_state.user_name
        
        if k=="Company":
            c=company
        elif k=="HR":
            c=dept
        elif k=="Employee":
            c=employee
            
        c(kl)
        with st.sidebar:
            if st.button("Logout", use_container_width=True):
                del st.session_state.user
                
    else:
        st.session_state.flag=False
        page_options = ["Sign Up", "Sign In"]
        sel = st.sidebar.selectbox("Select a page", page_options)
        s2 = st.sidebar.selectbox(f"Enter {sel} type:", ["Company", "HR", "Employee"])
        if sel:
            if sel=="Sign Up":
                if s2 == "Company":
                    create_comp()
                elif s2 == "HR":
                    create_dept()
                elif s2 == "Employee":
                    create_emp()
            elif sel=="Sign In":
                signin(s2)
    # employee("AGSol001")
    
if __name__ == "__main__":
    main()