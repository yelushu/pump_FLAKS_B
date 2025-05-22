# 使用官方Python基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt ./

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制项目所有文件到容器
COPY . .

# 暴露Flask默认端口
EXPOSE 5000

# 设置环境变量（关闭Flask调试模式可改为production）
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# 启动Flask应用
CMD ["python", "run.py"]