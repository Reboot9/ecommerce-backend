FROM redis:7.0-alpine

# Copy custom redis.conf to the container
COPY config/redis/redis.conf /etc/redis/redis.conf

# Start Redis server with custom configuration
CMD ["redis-server", "/etc/redis/redis.conf"]
