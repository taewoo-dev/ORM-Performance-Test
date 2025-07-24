#!/bin/bash

# ORM Performance Test - Server Shutdown Script
# 실행 중인 모든 ORM 서버를 종료합니다.

echo "🛑 Stopping ORM Performance Test Servers..."

# PID 파일에서 프로세스 종료
if [ -f .sqlalchemy.pid ]; then
    SQLALCHEMY_PID=$(cat .sqlalchemy.pid)
    if kill -0 $SQLALCHEMY_PID 2>/dev/null; then
        echo "Stopping SQLAlchemy server (PID: $SQLALCHEMY_PID)..."
        kill $SQLALCHEMY_PID
    fi
    rm .sqlalchemy.pid
fi

if [ -f .tortoise.pid ]; then
    TORTOISE_PID=$(cat .tortoise.pid)
    if kill -0 $TORTOISE_PID 2>/dev/null; then
        echo "Stopping Tortoise server (PID: $TORTOISE_PID)..."
        kill $TORTOISE_PID
    fi
    rm .tortoise.pid
fi

if [ -f .edgedb.pid ]; then
    EDGEDB_PID=$(cat .edgedb.pid)
    if kill -0 $EDGEDB_PID 2>/dev/null; then
        echo "Stopping EdgeDB server (PID: $EDGEDB_PID)..."
        kill $EDGEDB_PID
    fi
    rm .edgedb.pid
fi

# 포트별로도 확인하여 종료
echo "Checking for remaining processes on ports 8001-8003..."
for port in 8001 8002 8003; do
    PID=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "Killing process on port $port (PID: $PID)..."
        kill $PID 2>/dev/null
    fi
done

# 대기 후 강제 종료 확인
sleep 2

for port in 8001 8002 8003; do
    PID=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "Force killing process on port $port (PID: $PID)..."
        kill -9 $PID 2>/dev/null
    fi
done

echo "✅ All servers stopped!"

# 데이터베이스 파일 정리 (선택사항)
read -p "Do you want to clean up test databases? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleaning up test databases..."
    rm -f test_*.db
    echo "✅ Database files cleaned up!"
fi 