# 使用官方 Python 3.7 镜像
FROM python:3.7-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt ./

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目所有文件到容器
COPY . .

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# 启动 Flask 项目
CMD ["python", "run.py"]