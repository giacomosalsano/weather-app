#!/bin/sh
set -e

echo ""
echo "---------------------------------------------------"
echo "🚀 [WEATHER-APP] SYSTEM INITIALIZATION STARTED"
echo "---------------------------------------------------"
echo ""

echo "🔍 [1/3] Searching for database connectivity..."
echo "📍 Target: $DB_HOST on port 5432"

until nc -z "$DB_HOST" 5432; do
  echo "⚠️  [WAITING] Database is not reachable yet. Sleeping for 2 seconds..."
  sleep 2
done

echo "✅ [2/3] Database connection established!"
echo ""

echo "🏗️  [3/3] Booting up Spring Boot Application (Java 21)..."
echo "---------------------------------------------------"
echo ""

# Executa o Java
java -jar app.jar