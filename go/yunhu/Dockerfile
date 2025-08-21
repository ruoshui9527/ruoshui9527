# 使用官方的 Go 镜像作为基础镜像
FROM golang:1.21.1-alpine

# 设置工作目录
WORKDIR /app

# 将本地文件拷贝到容器中的工作目录
COPY . .
ENV GOPROXY=https://goproxy.cn
# 构建 Go 程序
RUN go build -o main
# 暴露程序运行的端口
EXPOSE 8080

# 设置容器启动时运行的命令
CMD ["./main"]