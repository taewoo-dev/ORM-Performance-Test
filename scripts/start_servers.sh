#!/bin/bash

# ORM Performance Test - Server Startup Script
# 각 ORM별 FastAPI 서버를 동시에 실행합니다.

echo "🚀 Starting ORM Performance Test Servers..."

# Poetry shell 확인
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry not found. Please install Poetry first."
    exit 1
fi

# 백그라운드에서 각 서버 실행
echo "Starting SQLAlchemy server on port 8001..."
poetry run gunicorn apps.sqlalchemy_app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001 --daemon &
SQLALCHEMY_PID=$!

echo "Starting Tortoise ORM server on port 8002..."
poetry run gunicorn apps.tortoise_app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8002 --daemon &
TORTOISE_PID=$!

echo "Starting EdgeDB server on port 8003..."
poetry run gunicorn apps.edgedb_app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003 --daemon &
EDGEDB_PID=$!

# PID 저장
echo $SQLALCHEMY_PID > .sqlalchemy.pid
echo $TORTOISE_PID > .tortoise.pid  
echo $EDGEDB_PID > .edgedb.pid

echo ""
echo "🏃‍♂️ All servers started!"
echo "SQLAlchemy: http://localhost:8001 (PID: $SQLALCHEMY_PID)"
echo "Tortoise:   http://localhost:8002 (PID: $TORTOISE_PID)"
echo "EdgeDB:     http://localhost:8003 (PID: $EDGEDB_PID)"
echo ""
echo "Health checks:"

# 서버 시작 대기
sleep 5

# Health check
echo "Checking server status..."
for port in 8001 8002 8003; do
    if curl -s "http://localhost:$port/health" > /dev/null; then
        echo "✅ Server on port $port is healthy"
    else
        echo "❌ Server on port $port is not responding"
    fi
done

echo ""
echo "📝 To stop all servers, run: ./scripts/stop_servers.sh"
echo "📊 To run performance tests: poetry run python tests/locust_tests/run_performance_test.py"
echo ""
echo "Press Ctrl+C to stop monitoring (servers will continue running in background)"

# 서버 모니터링 (optional)
trap 'echo "Monitoring stopped. Servers are still running."; exit 0' INT
while true; do
    sleep 30
    echo "$(date): Servers still running..."
done 