@echo off
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing dependencies...
pip install flask==2.0.1
pip install flask-sqlalchemy==2.5.1
pip install flask-jwt-extended==4.3.1
pip install flask-migrate==3.1.0
pip install flask-cors==3.0.10
pip install pymysql==1.0.2
pip install bcrypt==3.2.0
pip install python-dotenv==0.19.0
pip install Pillow==8.3.2
pip install redis==3.5.3
pip install gunicorn==20.1.0
pip install alembic==1.7.1

echo Setting up database...
python -m flask db init
python -m flask db migrate
python -m flask db upgrade

echo Starting server...
python -m flask run --host=0.0.0.0 --port=5000