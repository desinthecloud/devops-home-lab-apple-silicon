# Use a multi-arch nginx image that works on Apple Silicon
FROM nginx:alpine

# Copy our custom page over the default nginx index
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

