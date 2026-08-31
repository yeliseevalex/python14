import sqlalchemy
from requests import Session
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


# engine = create_engine("sqlite:///example.sqlite")
#
# conn = engine.connect()
#
# metadata = sqlalchemy.MetaData()

# Student = sqlalchemy.Table(
#     "Student", metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(50), nullable=False),
#     Column("major", String(255), default="Math"),
#     Column("pass", Boolean, default=False)
# )

# metadata.create_all(engine)

# query = sqlalchemy.insert(Student).values({
#     "id": 1,
#     "name": "Bob",
#     "major": "English",
#     "pass": True
# })
# conn.execute(query)
# conn.commit()

# query_select = Student.select()
# output = conn.execute(query_select)
# print(output.fetchall())


# query = sqlalchemy.insert(Student)
# values_list = [
#     {"id": 2, "name": "Alice", "major": "Science", "pass": False},
#     {"id": 3, "name": "John", "major": "English", "pass": False},
#     {"id": 4, "name": "Ben", "major": "Math", "pass": True},
# ]
#
# conn.execute(query, values_list)
# conn.commit()

# query = Student.select().where(Student.columns.major == "English")
# output = conn.execute(query)
# print(output.fetchall())

# query = Student.update().values({"pass": True}).where(Student.columns.name == "Alice")
# conn.execute(query)
# conn.commit()

# query = Student.delete().where(Student.columns.name == "Ben")
# conn.execute(query)
# conn.commit()

# Divisions = sqlalchemy.Table(
#     "Divisions", metadata,
#     Column("division", String(10), primary_key=True),
#     Column("name", String(255)),
#     Column("Country", String(255))
# )
#
# Matches = sqlalchemy.Table(
#     "Matches", metadata,
#     Column("id", Integer, primary_key=True),
#     Column("div", String(10)),
#     Column("home_team", String(255)),
#     Column("away_team", String(255)),
#     Column("home_score", Integer),
#     Column("away_score", Integer)
# )
#
# metadata.create_all(engine)

# query = Divisions.insert()
# values_list = [
#     {"division": "E1", "name": "Premier League", "Country": "England"},
#     {"division": "D1", "name": "Bundesliga", "Country": "Germany"},
# ]
# conn.execute(query, values_list)
# conn.commit()



# query = Matches.insert()
# values_list = [
#     {"div": "E1", "home_team": "Liverpool", "away_team": "Norwich", "home_score": 2, "away_score": 0},
#     {"div": "E1", "home_team": "Newcastle", "away_team": "West Brom", "home_score": 3, "away_score": 2},
#     {"div": "D1", "home_team": "Bayern", "away_team": "Dortmund", "home_score": 2, "away_score": 1},
# ]
# conn.execute(query, values_list)
# conn.commit()


# query_join = sqlalchemy.join(Matches, Divisions, Matches.c.div == Divisions.c.division)
# query_select = sqlalchemy.select(Matches, Divisions).select_from(query_join)
# result = conn.execute(query_select)
# for match in result.fetchall():
#     print(match)

# query_select = sqlalchemy.select(
#     Divisions.c.division,
#     Divisions.c.name,
#     Divisions.c.Country,
#     Matches.c.home_team,
#     Matches.c.away_team,
#     Matches.c.home_score,
#     Matches.c.away_score
# ).select_from(query_join)
#
# result = conn.execute(query_select).fetchall()
# for match in result:
#     print(match)

# Base = declarative_base()
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     email = Column(String)
#
#     def __repr__(self):
#         return f"<User(id={self.id}, username={self.username}, email={self.email})>"
#
# engine = create_engine("sqlite:///example.db")
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# new_user = User(username="Bob", email="bob@gmail.com")
# session.add(new_user)
# session.commit()

#
# user = session.query(User).filter_by(username="Bob").first()
# user.email = "newBob@gmail.com"
# session.commit()
# session.delete(user)
# session.commit()


# Base = declarative_base()
#
# class Table(Base):
#     __tablename__ = "tables"
#     id = Column(Integer, primary_key=True)
#     seats = Column(Integer, nullable=False)
#     reservations = relationship("Reservation", back_populates="table")
#
#     def __repr__(self):
#         return f"<Table(id={self.id}, seats={self.seats})>"
#
# class Reservation(Base):
#     __tablename__ = "reservations"
#     id = Column(Integer, primary_key=True)
#     table_id = Column(Integer, ForeignKey('tables.id'))
#     reserved_at = Column(DateTime, nullable=False)
#     duration_minutes = Column(Integer, default=60)
#     table = relationship("Table", back_populates="reservations")
#
#     def __repr__(self):
#         return f"<Reservation(Table{self.table_id} reserved at {self.reserved_at} duration {self.duration_minutes})>"
#
# engine = create_engine('sqlite:///restaurant.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
#
# def add_table(seats):
#     table = Table(seats=seats)
#     session.add(table)
#     session.commit()
#     print(f"Add table: {table}")
#
# def book_table(requested_seats, desire_time):
#     tables = session.query(Table).filter(Table.seats >= requested_seats)
#     for table in tables:
#         reservations = session.query(Reservation).filter_by(table_id=table.id).all()
#         conflict = False
#         for res in reservations:
#             res_start = res.reserved_at
#             res_end = res.reserved_at + timedelta(minutes=res.duration_minutes)
#
#             if not (desire_time <= res_start or desire_time >= res_end):
#                 conflict = True
#                 break
#
#         if not conflict:
#             reservations = Reservation(table=table, reserved_at=desire_time, duration_minutes=60)
#             session.add(reservations)
#             session.commit()
#             print(f"Add reservation: {reservations}")
#             return
#
#     print("Dont have empty tables")
#
#
#
# add_table(2)
# add_table(4)
#
# book_table(2, datetime(2026, 8, 29, 18, 0))
# book_table(3, datetime(2026, 8, 29, 18, 0))
# book_table(4, datetime(2026, 8, 29, 18, 30))
# book_table(2, datetime(2026, 8, 29, 18, 45))
# book_table(4, datetime(2026, 8, 29, 19, 30))
# book_table(7, datetime(2026, 8, 29, 20, 50))


Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group = Column(String,  nullable=False)
    grades = relationship("Grade", back_populates="student")

    def __repr__(self):
        return f"<Student(Name: {self.name} Group: {self.group})>"

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grades = relationship("Grade", back_populates="subject")

    def __repr__(self):
        return f"<Subject(Name: {self.name})>"

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    value = Column(Integer, nullable=False)
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")



engine = create_engine("sqlite:///school.db")
Base.metadata.create_all(engine)
Session1 = sessionmaker(bind=engine)
session = Session1()



def add_student(name, group):
    student = Student(name=name, group=group)
    session.add(student)
    session.commit()
    print(f"Add student: {student}")

def add_subject(name):
    subject = Subject(name=name)
    session.add(subject)
    session.commit()
    print(f"Add subject: {subject}")

# def give_grade(student_id, subject_id, value):
def give_grade(student_name, subject_name, value):
    student = session.query(Student).filter_by(name=student_name).first()
    subject = session.query(Subject).filter_by(name=subject_name).first()

    if not student or not subject:
        print("Student or Subject not found")
        return

    grade = Grade(student=student, subject=subject, value=value)
    session.add(grade)
    session.commit()
    print(f"Add grade {value} student {student_name} subject {subject_name}")

def student_average(student_name):
    student = session.query(Student).filter_by(name=student_name).first()
    if not student:
        print("Student not found")
        return

    grades = [g.value for g in student.grades]
    if grades:
        avg = sum(grades)/len(grades)
        print(f"Average {student_name}: {avg:.2f}")
    else:
        print(f"Average {student_name}: None")

def subject_average(subject_name):
    subject = session.query(Subject).filter_by(name=subject_name).first()
    if not subject:
        print("Subject not found")
        return

    grades = [g.value for g in subject.grades]
    if grades:
        avg = sum(grades) / len(grades)
        print(f"Average {subject_name}: {avg:.2f}")
    else:
        print(f"Average {subject_name}: None")

def list_honors():
    print("Students with avg grade (>= 90): ")
    students = session.query(Student).all()
    for student in students:
        grades = [g.value for g in student.grades]
        if grades:
            avg = sum(grades) / len(grades)
            if avg >= 90:
                print(f"{student} (Avg: {avg:.2f})")

def print_separator():
    print("\n" + "="*50)


add_student("Bob", "Python")
add_student("Alice", "Python")
add_student("John", "Python")
print_separator()

add_subject("Math")
add_subject("English")
add_subject("Programming")
print_separator()

give_grade("Bob", "Math", 95)
give_grade("Bob", "English", 60)
give_grade("Bob", "Programming", 100)
print_separator()

give_grade("Alice", "Math", 95)
give_grade("Alice", "English", 85)
give_grade("Alice", "Programming", 90)
print_separator()

give_grade("John", "Math", 85)
give_grade("John", "English", 95)
give_grade("John", "Programming", 90)
print_separator()

student_average("Bob")
student_average("Alice")
student_average("John")
print_separator()

list_honors()
















