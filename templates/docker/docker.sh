#!/bin/bash

CONTAINER_NAME="{{ container_name }}"
IMAGE_NAME="{{ image_name }}"
DEFAULT_PORT=8000

# Help message
show_help() {
    echo "Usage: ./docker.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  build     - Build Docker image"
    echo "  start     - Start container"
    echo "  stop      - Stop container"
    echo "  clean     - Remove container and image"
    echo "  test      - Run tests against the server"
    echo ""
    echo "Options for start:"
    echo "  --port=PORT       - Set the port (default: $DEFAULT_PORT)"
    echo "  --transport=TYPE  - Set transport type: 'sse' or 'io' (default: sse)"
    echo ""
    echo "Examples:"
    echo "  ./docker.sh build"
    echo "  ./docker.sh start --port=8080 --transport=sse"
    echo "  ./docker.sh stop"
    echo "  ./docker.sh clean"
}

# Build the Docker image
build() {
    echo "Building $IMAGE_NAME..."
    docker build -t "$IMAGE_NAME" .
}

# Start the container
start() {
    local port=$DEFAULT_PORT
    local transport="sse"
    
    # Parse arguments
    for arg in "$@"; do
        case $arg in
            --port=*)
            port="${arg#*=}"
            ;;
            --transport=*)
            transport="${arg#*=}"
            ;;
        esac
    done
    
    # Validate transport
    if [[ "$transport" != "sse" && "$transport" != "io" ]]; then
        echo "Error: Transport type must be 'sse' or 'io'"
        exit 1
    fi
    
    echo "Starting $CONTAINER_NAME with $transport transport on port $port..."
    
    if [[ "$transport" == "sse" ]]; then
        docker run -d --name "$CONTAINER_NAME" -p "$port:8000" \
            -e TRANSPORT=sse \
            "$IMAGE_NAME"
    else
        # IO transport doesn't need port mapping
        docker run -d --name "$CONTAINER_NAME" \
            -e TRANSPORT=io \
            "$IMAGE_NAME"
    fi
}

# Stop the container
stop() {
    echo "Stopping $CONTAINER_NAME..."
    docker stop "$CONTAINER_NAME" || true
    docker rm "$CONTAINER_NAME" || true
}

# Clean up
clean() {
    stop
    echo "Removing $IMAGE_NAME..."
    docker rmi "$IMAGE_NAME" || true
}

# Test the server
test() {
    echo "Testing MCP server..."
    # Implement tests here
    echo "Not implemented yet"
}

# Main execution
if [[ $# -lt 1 ]]; then
    show_help
    exit 1
fi

command=$1
shift

case "$command" in
    build)
        build
        ;;
    start)
        start "$@"
        ;;
    stop)
        stop
        ;;
    clean)
        clean
        ;;
    test)
        test
        ;;
    *)
        show_help
        exit 1
        ;;
esac