FROM redis:alpine

# Copy redis.conf file into the container
COPY ./redis.conf /data/config/redis/redis.conf

RUN mkdir -p /var/log/redis && \
    mkdir -p /var/lib/redis && \
    chown -R redis:redis /var/log/redis && \
    chown -R redis:redis /var/lib/redis

CMD ["redis-server", "/data/config/redis/redis.conf"]
