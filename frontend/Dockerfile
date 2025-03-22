# 建置階段
FROM node:18-alpine as build

WORKDIR /app

# 複製 package.json 和 package-lock.json (如果存在)
COPY package*.json ./

# 安裝依賴
RUN npm install

# 複製源碼
COPY . .

# 建置靜態文件
RUN npm run build

# 生產階段
FROM nginx:alpine

# 將靜態文件複製到 Nginx 服務目錄
COPY --from=build /app/build /usr/share/nginx/html

# 複製自定義的 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

# 運行 nginx
CMD ["nginx", "-g", "daemon off;"]
