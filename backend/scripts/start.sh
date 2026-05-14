#!/bin/sh
set -e

echo ""
echo "---------------------------------------------------"
echo "🚀 [WEATHER-APP] SYSTEM INITIALIZATION STARTED"
echo "---------------------------------------------------"
echo ""

echo "🔍 Searching for database connectivity..."
echo "📍 Target: $DB_HOST on port 5432"

until nc -z "$DB_HOST" 5432; do
  echo "⚠️  [WAITING] Database is not reachable yet. Sleeping for 2 seconds..."
  sleep 2
done

echo "✅ Database connection established!"
echo ""

echo "🏗️ Booting up Spring Boot Application (Java 21)..."
echo "---------------------------------------------------"
echo ""

# Executa o Java
java -jar app.jar