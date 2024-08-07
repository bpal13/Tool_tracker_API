from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship, Session
from .database import Base, get_db


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    fullname = Column(String(50), nullable=False)
    password = Column(String(250), nullable=False)
    employee_id = Column(Integer, unique=True)
    registered = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_login = Column(TIMESTAMP(timezone=True))
    still_employed = Column(Boolean, server_default="TRUE")
    user_role = Column(Integer, ForeignKey("roles.id"))

    roles = relationship("Roles")

    def validate_employee_id(self, employee_id: int):
        pass

    def validate_username(self, username: str):
        pass

    def generate_password(self, password):
        pass

    
    def check_password(self, password):
        pass



class Tools(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(20))
    tool_id = Column(String(10), unique=True, nullable=False)
    tool_name = Column(String(50), nullable=False)
    tool_location = Column(String(50), nullable=False)
    tool_type = Column(String(50), nullable=False)
    tool_brand = Column(String(50), nullable=False)
    tool_serial = Column(String(50), nullable=False)
    tool_accuracy = Column(String(50), nullable=False)
    tool_range = Column(String(50), nullable=False)
    max_deviation = Column(String(50), nullable=False)
    visibility = Column(Boolean, server_default="TRUE") # DELETE LATER
    valid_until = Column(DateTime)
    notes = Column(String(255))

    issue_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    issued_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("Users")

    def validate_tool_id(self, tool_id):
        pass


class Calibrations(Base):
    __tablename__ = "calibrations"

    id = Column(Integer, primary_key=True, nullable=False)

    parent_id = Column(Integer, ForeignKey("tools.id", ondelete="CASCADE"), nullable=False)

    calibration_by = Column(String(100), nullable=False)
    calibration_date = Column(DateTime, nullable=False)
    next_calibration = Column(DateTime, nullable=False)
    rating = Column(String(30), nullable=False)
    temperature = Column(Integer, nullable=False)
    actual_deviation = Column(String(30), nullable=False)
    etalon = Column(String(100))
    KULSO_I_A = Column(Numeric(10,3))
    KULSO_II_A = Column(Numeric(10,3))
    KULSO_III_A = Column(Numeric(10,3))
    KULSO_I_B = Column(Numeric(10,3))
    KULSO_II_B = Column(Numeric(10,3))
    KULSO_III_B = Column(Numeric(10,3))
    KULSO_I_C = Column(Numeric(10,3))
    KULSO_II_C = Column(Numeric(10,3))
    KULSO_III_C = Column(Numeric(10,3))
    BELSO_I_A = Column(Numeric(10,3))
    BELSO_II_A = Column(Numeric(10,3))
    BELSO_III_A = Column(Numeric(10,3))
    BELSO_I_B = Column(Numeric(10,3))
    BELSO_II_B = Column(Numeric(10,3))
    BELSO_III_B = Column(Numeric(10,3))
    BELSO_I_C = Column(Numeric(10,3))
    BELSO_II_C = Column(Numeric(10,3))
    BELSO_III_C = Column(Numeric(10,3))
    hasab = Column(String(100))
    ring = Column(String(100))
    calib_notes = Column(String(255))


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)