# FROM kong:1.2rc1-centos
# COPY kong.yml /
# RUN cp /etc/kong/kong.conf.default /etc/kong/kong.conf

# FROM kong
# USER 0
# RUN mkdir -p /kong/declarative/
# COPY kong.yml /kong/declarative/
# RUN cp /etc/kong/kong.conf.default /etc/kong/kong.conf
# USER kong

FROM kong
USER root
COPY kong.yml /
USER kong
RUN cp /etc/kong/kong.conf.default /etc/kong/kong.conf


# FROM kong
# USER 0
# RUN mkdir -p /kong/declarative/
# COPY declarative/kong.yml /kong/declarative/
# RUN cp /etc/kong/kong.conf.default /etc/kong/kong.conf
# USER kong