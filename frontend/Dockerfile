FROM nginx:stable-alpine
# Kopioidaan HTML-tiedostot
COPY . /usr/share/nginx/html/
# Kopioidaan oma Nginx-konfiguraatio oletuksen tilalle
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80