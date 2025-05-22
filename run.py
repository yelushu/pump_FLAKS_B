from app import create_app, db
from app.models import *  # 导入所有模型
from app.initial_data import init_db
import click

app = create_app()

@app.cli.command("init-db")#需要再命令行打flask init-db  才能出发数据库初始化
def init_database():
    """Initialize the database."""
    if input("这将删除所有数据！确认吗？(y/n): ").lower() != 'y':#防止数据库初始化
        return
    db.create_all()
    init_db()
    click.echo('Initialized the database.')

if __name__ == '__main__':
    # init_database()
    app.run(debug=True)